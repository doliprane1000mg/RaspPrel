#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function
import time
import os
import operator, serial, signal, sys
from datetime import datetime
import SparqEE #version 1
import re
import signal
import sys
import geniePi as gp 
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
def vgReadObject(id,index):
	global ser
	cmd= chr(vgCmd.ReadObject) + chr(id)+chr(index)
	cks=reduce(operator.xor,(ord(s) for s in cmd),0)
	cmd= cmd+chr(cks)
	ser.write(cmd)
	try:
	    rsp=ord(ser.read(1))
	except TypeError:
		print("rsp is empty")
		rsp=-1
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
#ser = serial.Serial(port=display_port, baudrate=9600, timeout=5, parity=serial.PARITY_NONE,
#  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS )
#ser.close()
#ser.open()

# send dummy characters until we get a NAK back, hopefully
# then the display sequencer will be in a stable state.
#time.sleep(1)
print("Sending dummy char until NAK back")
#for i in range(1,10):
 # rsp = vgWriteObject(vgObject.Form, 0, 0) # load Form 0
  #if (rsp != vgCmd.NAK):
   # break
  #print" "+str(i)+"..."
  #time.sleep(1)
#if (i > 9):
 # print ("unable to open serial port, exiting")
  #sys.exit(3)
#print("Stable state ")

#print ("load form 1")
#vgWriteObject(vgObject.Form, 0, 0) # load Form 0

#time.sleep(1)
#while(1):

#	rsp=vgReadObject(21,0)
#	print("rsp="+str(rsp))
#	print(ser.read(1))
#	time.sleep(1)
#print "load form 0"
#time.sleep(1)
#ser.close()

reply=gp.genieReplyStruct()
gp.genieSetup(display_port,9600)
print("GPLIBRARY LOADED")
go=True
num=""
sms=""
while (go):
	while gp.genieReplyAvail():
		gp.genieGetReply(reply)
		print(reply.cmd,reply.object,reply.index,reply.data)
		if(reply.object == 13) and (reply.index==1):
			if(reply.data==107):
				#num=''
				#num=num+"+"
				print("nouveau sms")
			if(reply.data==13):
				print(num)
			
			if(reply.data>47 and reply.data <58):
				num=num+chr(reply.data)
				#
		if(reply.object==13) and (reply.index==0):
			sms=sms+chr(reply.data)
		if(reply.object==6):
			go=False

			
	print("dodo")
	time.sleep(1)
	


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
print("ENVOIE AU N "+num+ " sms:"+sms)


    
# GLOBALS --------------------------------------------------------------------

SparqEE.glob_debug = 5              #Override global debug print level   

def debug(str):
    SparqEE.debug_print( str, SparqEE.debug["DEBUG"] )
    
def debug2(cmd, ret):
    debug(cmd)
    debug( "---> CMD RET --->: " + str(ret) )
    debug( "---> BUFFER  --->" + SparqEE.buffer )

#-----------------------------------------------------------------------------

try:
    SparqEE.cmd_setup()             #set-up shield GPIO
    SparqEE.cmd_power()             #power on
    SparqEE.cmd_connection()        #check cellular connection
		#	+12223334444
    #BASIC SMS
    ret = SparqEE.at_sms("+"+num, sms)
    debug2 ("STATUS", ret)
    
#-----------------------------------------------------------------------------

    SparqEE.debug_print( "***END***", SparqEE.debug["WARNING"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    
except:
    SparqEE.debug_print( "***END (exception)***", SparqEE.debug["CRITICAL"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    print ("Unexpected error:"), sys.exc_info()[0]
    raise
