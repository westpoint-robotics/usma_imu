#!/usr/bin/python
import time
import serial
import string
from os.path import expanduser

'''
udev rule settings for the CNS 5000 and flexpak6
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller", SYMLINK+="raw_imu"
SUBSYSTEM=="tty", ATTRS{idProduct}=="2303", ATTRS{idVendor}=="067b", ATTRS{product}=="USB-Serial Controller D", SYMLINK+="raw_gps"
SUBSYSTEM=="tty", ATTRS{idProduct}=="0100", ATTRS{idVendor}=="09d7", SYMLINK+="flex6_gps"
'''
dataDir = "/home/user1/Data/"



try:
    with open(dataDir+"cleaned_totalLog.csv", 'w') as cleanfile, open(dataDir+"totalLog.log","r") as totalLog:
        printable = set(string.printable)
        for line in totalLog:
            line=line.split('#')
            if (len(line))>1:
                print (line[1]+"\n")
            #outString = filter(lambda x: x in printable, line)
            #outString = ''.join([i if ord(i) < 128 else ' ' for i in line])
            #print(outString + "\n")
            #cleanfile.write(outString)
        

except (KeyboardInterrupt, SystemExit):
    ser.write('unlogall\r\n') # Send a message to CNS-5000 to stop sending logs
    ser.close()
    raise


