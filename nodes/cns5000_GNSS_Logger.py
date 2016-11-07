#!/usr/bin/python
import time
import serial
from os.path import expanduser

'''
udev rule settings for the CNS 5000 and flexpak6
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller", SYMLINK+="raw_imu"
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller D", SYMLINK+="raw_gps"
SUBSYSTEM=="tty", ATTRS{idProduct}=="0100", ATTRS{idVendor}=="09d7", SYMLINK+="flex6_gps"
'''
# TODO rename these devices. raw_gps is not accurate name, this the cns5000 ins device.
ser = serial.Serial(
    port='/dev/raw_gps',
    baudrate=115200, #8N1
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if (ser.isOpen()):
    ser.close()
ser.open()

# Send commands to CNS-5000 to start the logs
ser.write('unlogall\r\n')
ser.write('LOG COM1 INSPVAA ONTIME 0.2\r\n')
ser.write('LOG COM1 BESTPOSA ONTIME 1\r\n')
dataDir = "/home/user1/Data/"


try:
    with open(dataDir+"cns5000_INSPVAA.csv", 'w') as inspvafile, open(dataDir+"cns5000_BESTPOSA.csv", "w") as bestposfile, open(dataDir+"totalLog.log","w") as totalLog:

        outString = "hMessage,hPort,hSequence#,h%IdelTime,hTimeStatus,hWeek,hSeconds,hReceiverStatus, Reserved,RcvrSwVersion,GNSSweek,SecondsFromWeek,Latitude,Longitude,EllipsoidalHeight,VelocityNorth,VelocityEast,VelocityUp,Roll,Pitch,Azimuth,InertialStatus,Checksum\n"
        inspvafile.write(outString)
        print(outString)

        outString = "hMessage,hPort,hSequence#,h%IdelTime,hTimeStatus,hWeek,hSeconds,hReceiverStatus, Reserved,RcvrSwVersion,SolutionStatus,PosType,Latitude,Longitude,Height,Undulation,datum,latSdev,lonSdev,hgtSdev,BaseStationId,DiffAge,SolAge,NumSatTracked,NumSatUsed,NumL1SatUsed,NumSatMultiFreq,reserved,ExtSolStatus,SignalMask,SignalMask,CRC\n"
        bestposfile.write(outString)
        print(outString)

        while True: # Continue until keyboard interrupt

            while ser.inWaiting() > 0:                
                # While data is in the buffer
                kvh5000_output = ser.readline() # Read data a line of data from buffer
                totalLog.write(kvh5000_output)
                new_output=kvh5000_output.replace("*",",")
                new_output=kvh5000_output.replace(";",",")

                if (kvh5000_output.split(",")[0] == "#INSPVAA"): # check if this the INSPVA message                    
                    inspvafile.write(new_output) # Option to log data to file
                    print(new_output),            

                if (kvh5000_output.split(",")[0] == "#BESTPOSA"): # check if this the BESTGPSPOSA message
                    bestposfile.write(new_output) 
                    print(new_output),

except (KeyboardInterrupt, SystemExit):
    ser.write('unlogall\r\n') # Send a message to CNS-5000 to stop sending logs
    ser.close()
    raise


