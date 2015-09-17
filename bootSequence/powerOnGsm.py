#!/usr/bin/python

import SparqEE #version 1
import re
import signal
import sys

#-----------------------------------------------------------------------------

try:
    SparqEE.cmd_setup()                     #set-up shield GPIO
    SparqEE.cmd_power()                     #power on
    
#-----------------------------------------------------------------------------
    
except:
    SparqEE.cmd_cleanup()                   #clean-up shield GPIO
    print "Unexpected error:", sys.exc_info()[0]
    raise
