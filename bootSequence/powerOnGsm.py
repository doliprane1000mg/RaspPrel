#!/usr/bin/python

import SparqEE #version 1
import re
import signal
import sys
from datetime import datetime

#-----------------------------------------------------------------------------

try:
    SparqEE.cmd_setup()                     #set-up shield GPIO
    SparqEE.cmd_power()                     #power on
    f=open("/home/pi/private/numTel","r")
    num=f.readline()
    while(num.startswith('#')):
    	num=f.readline()
    print("sending:"+num+ " size:"+str(len(num)))
    f.close()
    SparqEE.at_sms(num.strip(),"RASPBERRY STARTING AT\n "+str(datetime.now()))
    SparqEE.cmd_cleanup()    
    SparqEE.closeSerial()
#-----------------------------------------------------------------------------
    
except:
    SparqEE.cmd_cleanup()                   #clean-up shield GPIO
    SparqEE.closeSerial()
    print "Unexpected error:", sys.exc_info()[0]
    raise
