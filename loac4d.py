#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function
import time
import os
import operator, serial, signal, sys
from datetime import datetime
 
class vgCmd:
  ReadObject = 0
  WriteObject = 1
  WriteString = 2
  WriteStringUnicode = 3
  WriteContrast = 4
  ReportObject = 5
  ReportEvent = 6
  ACK = 0x06
  NAK = 0x15
 
class vgObject:
  DipSwitch = 0
  Knob = 1
  RockerSwitch = 2
  RotarySwitch = 3
  Slider = 4
  TrackBar = 5
  WinButton = 6
  Meter = 7
  CoolGauge = 8
  CustomDigits = 9
  Form = 10
  Guage = 11
  Image = 12
  Keyboard = 13
  LED = 14
  LEDdigits = 15
  Meter = 16
  Strings = 17
  Thermomter = 18
  UserLED = 19
  Video = 20
  StaticText = 21
  Sound = 22
  Timer = 23
  Spectrum= 24

def vgWriteObject(id, index, value):
  global ser
  cmd = chr(vgCmd.WriteObject) + chr(id) + chr(index) + chr(int(value/256)) + chr(value%256)
  cks = reduce(operator.xor, (ord(s) for s in cmd), 0)
  cmd = cmd + chr(cks)
#  print "vg write"
#  print ":".join("{:02x}".format(ord(c)) for c in cmd)
  ser.write(cmd)
#  print "rsp"
  try: 
	rsp = ord(ser.read(1))
	# rsp=ser.read(1)
  except TypeError:
	print ("rsp is empty")
	rsp=-1
#  print "{:02x}".format(rsp)
  return rsp

# handle kill & ctrl-C
def handleSigTERM(signum, frame):
  global ser
  print ("kill signal")
  ser.close
  exit(0)
def handleCtrlC(signum, frame):
  global ser
  print ("Ctrl-C signal")
  ser.close
  exit(0)
 



#MAIN ?"
print("Debut du programme...")
signal.signal(signal.SIGTERM, handleSigTERM)
signal.signal(signal.SIGINT, handleCtrlC)
 
display_port = ("/dev/ttyUSB0")
# Open the serial port, close, & re-open again
ser = serial.Serial(port=display_port, baudrate=9600, timeout=5, parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
ser.close()
ser.open()

# send dummy characters until we get a NAK back, hopefully
# then the display sequencer will be in a stable state.
#time.sleep(1)
print("Sending dummy char until NAK back")
for i in range(1,10):
  rsp = vgWriteObject(vgObject.Form, 0, 0) # load Form 0
  if (rsp != vgCmd.NAK):
    break
  #print" "+str(i)+"..."
  time.sleep(1)
if (i > 9):
  print ("unable to open serial port, exiting")
  sys.exit(3)
print("Stable state ")

print ("load form 1")
vgWriteObject(vgObject.Form, 0, 0) # load Form 0

time.sleep(1)

#print "load form 0"
rsp=vgWriteObject(vgObject.Spectrum, 0,50) # load Form 0
time.sleep(1)




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


ser= serial.Serial("/dev/ttyUSB0",38400,parity=serial.PARITY_NONE)
ser.open()
   #  
debut=datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
FirstCar='$'
LastCar='*'
chaine=''
ser.write('$STOP£')
ser.write('$START10£')
x=0
y=0
    
while(1):

	now = datetime.now()
	print("While..."+str(i))
	if (now.second % 2):
		vgWriteObject(vgObject.LED, 0, 1)
	else:
		vgWriteObject(vgObject.LED, 0, 0)
	 
	vgWriteObject(vgObject.LEDdigits, 0, now.hour)
	vgWriteObject(vgObject.LEDdigits, 1, now.minute)
	vgWriteObject(vgObject.LEDdigits, 2, now.second)
	
	 

	monFichier= open(str(debut)+'.txt','a')
        chaine=ser.readline()
        print(chaine)
           
        
        now=datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")        
       
#LECTURE TRAME 2 LOAC N2
        chaine=ser.readline()
        granuloTab=chaine.split(',')
        print ("V2 :",end='')
        i=1
        while i < len(granuloTab)-1:
        	granuloTab[i]=i
                
        	val=int(granuloTab[i],16)
        	print (str(val)+' ',end='')
         	i=i+1
        
        print(chaine)


        time.sleep(5)
        print("")


ser.close()
   
    #for line in ser:
     #      print (line.rstrip('\n'))


    


















