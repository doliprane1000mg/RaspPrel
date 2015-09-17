#!/usr/bin/python

import SparqEE #version 1
import re
import signal
import sys
from datetime import datetime
    
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
    SparqEE.cmd_setup()
    SparqEE.cmd_connection()        #check cellular connection

   # SparqEE.at_cmgsMem()	
    sms=SparqEE.at_readAllSms()
    
    print("Printing sms:"+sms)
    retour=sms.split('\n')
    if( len(retour[2])>4):
    	numero=(retour[1].split(','))[2] 
	numero=numero[1:-1]#Remove quote
    	message=retour[2]
    	message= "RASPBERRY ACK SMS:"+"\n"+message+"\n"+"HEURE:"+str(datetime.now())

    
    	ret=SparqEE.at_sms(numero,message)
    	if(ret==0):
		SparqEE.at_delSms()
    SparqEE.cmd_cleanup()
    		    
except:
    SparqEE.debug_print( "***END (exception)***", SparqEE.debug["CRITICAL"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    print "Unexpected error:", sys.exc_info()[0]
    raise
