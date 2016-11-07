#!/usr/bin/env python

import serial, string, math, time, calendar
import struct
import sys
import datetime

'''
udev rule settings for the CNS 5000 and flexpak6
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller", SYMLINK+="raw_imu"
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller D", SYMLINK+="raw_gps"
SUBSYSTEM=="tty", ATTRS{idProduct}=="0100", ATTRS{idVendor}=="09d7", SYMLINK+="flex6_gps"
'''

def wrapTo2PI(theta):
    '''Normalize an angle in radians to [0, 2*pi]
    '''
    return theta % (2.*math.pi)

def wrapToPI(theta):
    '''Normalize an angle in radians to [-pi, pi]
    '''
    return (wrapTo2PI(theta+math.pi) - math.pi)

def KVHCG5100shutdownhook():
    global KVH_IMU
    print "KVH CG-5100 IMU shutdown time!"
    print('Closing IMU Serial port')
    KVH_IMU.close() #Close KVH_IMU serial port
    
    
def CehckCRC(data):
    # in this function cehck CRC
    if (len(data)==36)&(data[0:4]=="\xfe\x81\xff\x55"):
        Acrc=struct.unpack(">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH",data[4:36])
        return sum(Acrc[0:30])==Acrc[30]
    else:
        return False
        
if __name__ == '__main__':
    global KVH_IMU
    global SerialData
    KVH_IMUport = '/dev/raw_imu'
    KVH_IMUrate = 115200
    CRC_error_limits   =10.0
    CRC_errorcounter=0

    try:
        #ReadCompass()
        #Setup Compass serial port
        KVH_IMU = serial.Serial(port=KVH_IMUport, baudrate=KVH_IMUrate, timeout=.5)       
        
        time.sleep(0.1)
        # readout all data, if any
        print("Test reading data from IMU. Got bytes %i" % KVH_IMU.inWaiting() ) # should got some data
        if (KVH_IMU.inWaiting() >0):
                #read out all datas, the response shuldbe OK
                data=KVH_IMU.read(KVH_IMU.inWaiting())
                if ("\xfe\x81\xff\x55" in data) :
                    print("Got Header from IMU") 
                else :
                    print("Got No Header from IMU data. Please check serial port!") 
                    print('[0]Received No IMU header from KVH CG-5100 IMU. Please check IMU serial port and IMU Power. Shutdown!') 
                    sys.exit()
        else:
                #send error, if no data in buffer
                print('[1]Received No data from KVH CG-5100 IMU. Please check IMU serial port and IMU Power. Shutdown!')
                sys.exit()
    except:
        print "Error:", sys.exc_info()[0]
        raise

    dataSynced=False
    data=""
    with open("cns5000_RawImu.csv", 'w') as outfile:
        outString = "Xangle, Yangle, Zangle,Xvelocity,Yvelocity,Zvelocity,Odometer,Status,Sequence\n"
        outfile.write(outString)
        print(outString)

        while True: # Continue until keyboard interrupt
            try:                     
                if (dataSynced) :
                    data = KVH_IMU.read(36)
                    DataTimeSec = datetime.datetime.now()
                else : # if not synced , look for header
                    data += KVH_IMU.read(KVH_IMU.inWaiting())
                    while (len(data)>=36):
                        if ("\xfe\x81\xff\x55" == data[0:4]):
                            if ( len(data)%36 >0 ): # still has unread data , so read them until we have full package
                                data += KVH_IMU.read(36-len(data)%36)
                                # we have 36*N data in buffer
                                # only keep the lastest data
                            data=data[len(data)-36:]
                            if (len(data)==36):
                                dataSynced=True
                                DataTimeSec = datetime.datetime.now()
                                break       
                        else :
                            data=data[1:] # drop 1 byte if not header
                            
                try:
                    if (dataSynced) :
                                if CehckCRC(data):

                                    fields=struct.unpack(">fffffffBB",data[4:34])
                                    # 1,2,3,4       : X angle, SPFP( Single-precision floating point) +/-0.66 radians
                                    # 5,6,7,8       : Y angle, SPFP( Single-precision floating point) +/-0.66 radians
                                    # 9,10,11,12    : Z angle, SPFP( Single-precision floating point) +/-0.66 radians
                                    # 13,14,15,16   : X velocity,  SPFP +/-1 m/sec Assumes 100 Hz TOV
                                    # 17,18,19,20   : Y velocity,  SPFP +/-1 m/sec Assumes 100 Hz TOV
                                    # 21,22,23,24   : Z velocity,  SPFP +/-1 m/sec Assumes 100 Hz TOV
                                    # 25,26,27,28   : Odometer pulses,  SPFP, 45 kHz
                                    # 29            : Status, DISC 1=valid;0=invalid , Value=119 == All sensor OK.
                                    # 30            : Sequence ,UINT8 0-127 Increments for each message and resets to 0 after 127

                                                                    
                                    # Note KVH CG5100 IMU use ENU system , same as ROS
                                    Ex =fields[0] # X angle +/-0.66 radians
                                    Ey =fields[1] # Y angle +/-0.66 radians
                                    Ez =fields[2] # Z angle +/-0.66 radians
                                    Vy=fields[3] # X velocity, +/-1 m/sec
                                    Vx=fields[4] # Y velocity, +/-1 m/sec
                                    Vz=fields[5] # Z velocity, +/-1 m/sec
                                    Odometer=fields[6]  # Odometer pulses
                                    Status  =fields[7]    # Status, Value=119 == All sensor OK.
                                    Sequence=fields[8] # Sequence UINT8 0-127 0 after 127


                                    outString=(",".join(str(field) for field in fields))+"\n"
                                    outfile.write(outString)
                                    print outString,
                                    
                                    # reset counter once you have good data
                                    CRC_errorcounter=0

                                else:
                                    print("[3] CRC error. Sentence was: %s" % ':'.join(x.encode('hex') for x in data))
                                    print("[3] CRC error, must re-sync") # 
                                    dataSynced=False
                                    CRC_errorcounter=CRC_errorcounter+1
                                    if (CRC_errorcounter>CRC_error_limits):
                                            CRC_errorcounter=0
                                            print('Too Much Back-to-Back CRC error ,Closing KVH IMU Serial port')
                                            KVH_IMU.close() #Close KVH_IMU serial port
                                            KVH_IMU = serial.Serial(port=KVH_IMUport, baudrate=KVH_IMUrate, timeout=.5)
                                            time.sleep(0.01)
                                            print('Try to re-open IMU Serial port')
                                            KVH_IMU.open() #Close KVH_IMU serial port

                except ValueError as e:
                    print("Value error, likely due to missing fields in the data messages.Sentence was: %s" % ':'.join(x.encode('hex') for x in data) )

            except (KeyboardInterrupt, SystemExit):
                print '\nkeyboardinterrupt caught (again)'
                print '\n...Program Stopped Manually!'
                print('Closing IMU Serial port')
                KVH_IMU.close() #Close KVH_IMU serial port
                raise

    print('Closing IMU Serial port')
    KVH_IMU.close() #Close KVH_IMU serial port

