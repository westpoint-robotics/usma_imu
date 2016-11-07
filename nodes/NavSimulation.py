#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
import time
from LatLongUTMconversion import LLtoUTM

datafolder = "/home/user1/Data/trial01/"

FLAG_inspvafile = True
FLAG_bestposfile = True
FLAG_flexPakfile = True
FLAG_xSensfile = True
inspvafile = "cns5000_INSPVAA.csv"
bestPosfile = "cns5000_BESTPOSA.csv"
flex6file = "flex6_gps.csv"
xsensfile = "mti700.csv"

i=0

# CNS-5000 INSPVAA Data Parsing ----------
fname = datafolder+inspvafile
if (os.path.isfile(fname) == False):
    FLAG_inspvafile = False
    print("File not found: " + fname)
else:
    print("Found file: " + fname)

inspvaArray = []   
cnsBestPosArray = [] 
if (FLAG_inspvafile):      
    with open(fname,'rb') as infile: #Read in data from this file
        content = infile.readlines()
        for row in content:
            if ('INSPVAA'in row): # remove unparsed bytes found when in SBAS mode.
                if ('\0' not in row) and ('#'==row[0]):
                    inspvaArray.append(row.split(','))
                else:
                    row=row.split('#')[-1].split(',') 
                    row[0]='#'+row[0]
                    inspvaArray.append(row) 

# CNS-5000 BESTPOSA Data Parsing ----------
fname = datafolder+bestPosfile
if (os.path.isfile(fname) == False):
    FLAG_bestposfile = False
    print("File not found: " + fname)
else:
    print("Found file: " + fname)

cnsBestPosArray = []
cnsBestPosArray = []
if (FLAG_bestposfile):
    with open(fname,'rb') as infile: #Read in data from this file
        content = infile.readlines()
        for row in content:
            if ('BESTGNSSPOSA'): # remove unparsed bytes found when in SBAS mode.
                if ('\0' not in row) and ('#'==row[0]):
                    cnsBestPosArray.append(row.split(','))
                else:
                    row=row.split('#')[-1].split(',') 
                    row[0]='#'+row[0]
                    cnsBestPosArray.append(row)    

# FlexPak6 BESTPOSA Data Parsing ---------------------
fname = datafolder+flex6file
if (os.path.isfile(fname) == False):
    FLAG_gpsArray = False
    print("File not found: " + fname)
else:
    print("Found file: " + fname)

flex6_gpsArray=[]
if (FLAG_gpsArray):
    with open(fname,'rb') as infile:
        content = infile.readlines()
        for row in content:
            if (('BESTPOSA'in row)):
                flex6_gpsArray.append(row.split(','))

# XSens MTI700 Data Parsing ----------
fname = datafolder+xsensfile
if (os.path.isfile(fname) == False):
    FLAG_xSensfile = False
    print("File not found: " + fname)
else:
    print("Found file: " + fname)

mti700Array = []
if (FLAG_xSensfile):
    with open(fname,'rb') as dictfile:        
        for line in dictfile:
            if 'Lat' in line:
                mti700Array.append(eval(line))

'''
plt.ion()
(zone,e,n)=LLtoUTM(23, 41.38231066666667,-73.97545914722222)  
plt.plot(e,n,'bx') #Survey Point on Stony2
for row in inspvaArray:
    (zone,easting,northing)=LLtoUTM(23, float(row[11]),float(row[12]))
    plt.plot(easting,northing,'b.')
    i = i + 1
    if (i < len(flex6_gpsArray)):
        (zone,e,n)=LLtoUTM(23, float(flex6_gpsArray[i][11]),float(flex6_gpsArray[i][12]))    
        plt.plot(e,n, 'g.')
    plt.pause(0.0015)

plt.pause(1000)
'''
initeast=-1
initnorth=-1
plt.ion() # This command enables interactive plotting
if(FLAG_inspvafile):
    strTime=inspvaArray[0][6]
    endTime=inspvaArray[-1][6]
    #print strTime,endTime,mti700Array[0]['GNSS']['ITOW']
    i =0
    j=0

    for row in inspvaArray:
        #Convert to UTM for meters and zero out location
        (zone,easting,northing)=LLtoUTM(23, float(row[12]),float(row[13]))
        if -1==initeast:
            initeast=easting
            initnorth=northing
        easting=easting-initeast
        northing=northing-initnorth
        plt.plot(easting,northing,'r.')

        if(FLAG_gpsArray):
            # Plot FlexPack 6 grids if its time to plot
            print row[6],flex6_gpsArray[i][6], len(flex6_gpsArray)
            while ((row[6] <= flex6_gpsArray[i][6]) and (i < len(flex6_gpsArray))):
                print flex6_gpsArray[i][6],"flex6"
                (zone,e,n)=LLtoUTM(23, float(flex6_gpsArray[i][11]),float(flex6_gpsArray[i][12]))    
                e=e-initeast
                n=n-initnorth
                plt.plot(e,n,'g.')
                #plt.pause(0.0001)
                i = i + 1
            

        if(FLAG_xSensfile):
            # Plot Xsens Mti700 grids if its time to plot
            mtiTime=(mti700Array[j]['GNSS']['ITOW'])/1000.0      
            while ((float(row[6]) >= mtiTime) and (j < len(mti700Array))):    
                mtiTime=(mti700Array[j]['GNSS']['ITOW'])/1000.0      
                #print mtiTime,"mti700"
                (zone,e,n)=LLtoUTM(23, float(mti700Array[j]['GNSS']['Lat']),float(mti700Array[j]['GNSS']['Lon']))    
                e=e-initeast
                n=n-initnorth
                plt.plot(e,n,'y.')
                j = j + 1
        
        #plt.pause(0.000001) # this line slows down animation

        '''
        if ('#BESTGNSSPOSA'not in row):
            plt.plot(easting,northing,'b.')
        else :
            plt.plot(easting,northing,'r.')
        #plt.pause(0.0015)'''

plt.waitforbuttonpress(timeout=-1)
'''

# CNS-5000 example output of INSPVAA
['#INSPVAA', 'COM1', '0', '68.5', 'FINESTEERING', '2946', '162546.600', '00080000', '54e2', '13742', '2946', '162546.600000000', '41.39124157925', '-73.95395726549', '15.4528', '-0.1844', '-0.0883', '0.1638', '0.000000000', '0.000000000', '0.000000000', 'INS_ALIGNING*e4d0fd5c\r\n']


# FlexPak6 example output:
#['#BESTPOSA', 'USB2', '0', '86.0', 'FINESTEERING', '1901', '422235.000', '00040000', '7145', '10985;SOL_COMPUTED', 'WAAS', '41.39489439713', '-73.95505065150', '48.9009', '-32.2000', 'WGS84', '1.4642', '1.0299', '2.9375', '"133"', '7.000', '0.000', '10', '7', '7', '7', '0', '06', '00', '03', '7beb228b\r\n']

# XSens example outpuit:
#{'GNSS': {'gDOP': 1.59, 'tDOP': 0.7000000000000001, 'gpsFix': 3, 'hour': 21, 'altMSL': 55, 'HeadAcc': 2762354, 'Lon': -73.9550379, 'pDOP': 1.43, 'month': 6, 'sec': 15, 'year': 2016, 'Hacc': 396, 'day': 16, 'nDOP': 0.64, 'vDOP': 1.1500000000000001, 'hDOP': 0.84, 'gspeed': 0, 'min': 17, 'altEllipsoid': 21, 'Sacc': 120, 'valid': 7, 'flags': 3, 'ITOW': 422252250, 'Vel_N': 0, 'Lat': 41.394883799999995, 'Vacc': 618, 'numSV': 10, 'tAcc': 1, 'Vel_E': 0, 'Vel_D': 0, 'eDOP': 0.55, 'nano': 249969158}, 'Timestamp': {'PacketCounter': 37220}}

'''

