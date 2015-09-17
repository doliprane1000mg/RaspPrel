#!/usr/bin/python

import SparqEE #version 1
import re
import signal
import sys

    
# GLOBALS --------------------------------------------------------------------

SparqEE.glob_debug = 5                      #Override global debug print level   

def debug(str):
    SparqEE.debug_print( str, SparqEE.debug["DEBUG"] )
    
def debug2(cmd, ret):
    debug(cmd)
    debug( "---> CMD RET --->: " + str(ret) )
    debug( "---> BUFFER  --->" + SparqEE.buffer )

#-----------------------------------------------------------------------------

try:
    SparqEE.cmd_setup()                     #set-up shield GPIO
    SparqEE.cmd_power()                     #power on
    SparqEE.cmd_connection()                #check cellular connection

    #BASIC AT COMMANDS
    #Nickname                       #at command     #Description
    print("STATUS")    
    ret=SparqEE.info_status()
    debug2("INFOSTATUS MEHDI",ret)
   
    print("STATUS CLASSIQUE")
    ret = SparqEE.at_status()       #at_at          #Quick status
    debug2 ("STATUS", ret)
    print("Echo")
    ret = SparqEE.at_echoOn()       #at_ate1        #Enable command echo
    debug2 ("ECHO", ret)
    print("Network registration status")
    ret = SparqEE.at_reg()          #at_creg        #Network registration status
    debug2 ("REG", ret)
   # print("List available networks")   
   # ret = SparqEE.at_nets()         #at_cops        #List available networks
   # debug2 ("NETS", ret)
    print("Current tech")
    ret = SparqEE.at_tech()         #at_cnti        #Current tech
    debug2 ("TECH", ret)
    print("Signal quality")
    ret = SparqEE.at_sig()          #at_csq         #Signal Quality
    debug2 ("SIG", ret)
    
#-----------------------------------------------------------------------------

    SparqEE.debug_print( "***END***", SparqEE.debug["WARNING"] )
    SparqEE.cmd_cleanup()                   #clean-up shield GPIO
    
except:
    SparqEE.debug_print( "***END (exception)***", SparqEE.debug["CRITICAL"] )
    SparqEE.cmd_cleanup()                   #clean-up shield GPIO
    print "Unexpected error:", sys.exc_info()[0]
    raise
