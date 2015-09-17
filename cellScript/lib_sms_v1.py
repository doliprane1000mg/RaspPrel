#!/usr/bin/python

import SparqEE #version 1
import re
import signal
import sys

    
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
#    ret = SparqEE.at_sms(sys.argv[1], "Sms depuis raspberry pi")
 #   debug2 ("STATUS", ret)
    
#-----------------------------------------------------------------------------

  #  SparqEE.debug_print( "***END***", SparqEE.debug["WARNING"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    SparqEE.at_readSms()

		    
except:
    SparqEE.debug_print( "***END (exception)***", SparqEE.debug["CRITICAL"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    print "Unexpected error:", sys.exc_info()[0]
    raise
