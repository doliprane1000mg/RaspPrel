#!/usr/bin/python

import re
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO
import serial
    

#-----------------------------------------------------------------------------
# GLOBALS --------------------------------------------------------------------
#-----------------------------------------------------------------------------

debug = {                       #ENUM levels for printing (enum requires another module, so using a dict)
    "CRITICAL"    : 1,
    "ERROR"       : 2,
    "WARNING"     : 3,
    "INFO"        : 4,          #Includes: function titles
    "DEBUG"       : 5
}

glob_debug = 5                  #Global debug print level  

pin_mp = 7                      #Raspberry Pi shield pinout to CELLv1.0
pin_mwa = 11
pin_ar = 12
pin_awm = 13
pin_mr = 15
pin_po = 16
pin_prn = 18
pin_ledR = 22
pin_ledB = 24
pin_ledG = 26 

ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=1)    #serial port

#-----------------------------------------------------------------------------
# SIGNAL ---------------------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   handle Ctrl+C
#input:         none
#return:        none
def signal_handler(signal, frame):
    debug_print( '\n\nYou pressed Ctrl+C!', debug["INFO"] )
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#-----------------------------------------------------------------------------
# GPIO COMMANDS --------------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   Turn module on
#input:         none
#return:        none
def gpio_turnOn():
    debug_print( "GPIO: TurnOn", debug["INFO"] )
    sleep(1)
    GPIO.output(pin_po, False)
    sleep(1)
    GPIO.output(pin_po, True)
    sleep(30)
    
#description:   Turn module off
#input:         none
#return:        none
def gpio_turnOff():
    debug_print( "GPIO: TurnOff", debug["INFO"] )
    sleep(1)
    GPIO.output(pin_po, False)
    sleep(6)
    GPIO.output(pin_po, True)
    
#description:   Toggle module power
#input:         none
#return:        none
def gpio_toggle():
    debug_print( "GPIO: Toggle", debug["INFO"] )
    sleep(1)
    GPIO.output(pin_prn, False)
    sleep(1)
    GPIO.output(pin_prn, True)
    sleep(30)
    
#description:   Check if module is connected to a network or not
#input:         none
#return:        0=2G or 3G, 1=unregistered
def gpio_ledConnected():
    debug_print( "GPIO: LED Connected", debug["INFO"] )
    ledR = GPIO.input(pin_ledR)     #Unregistered
    ledG = GPIO.input(pin_ledG)     #2G
    ledB = GPIO.input(pin_ledB)     #3G
    if ((ledG == 0) or (ledB == 0)):
        debug_print( " Connected to a cellular network", debug["INFO"] )
        return 0
    else:
        debug_print( " SIM Unregistered", debug["INFO"] )
        return 1
        
#description:   Check if module power is on (one of the LEDs should be lit with power)
#input:         none
#return:        0=power,1=off
def gpio_ledLit():
    debug_print( "GPIO: LED Lit", debug["INFO"] )
    ledR = GPIO.input(pin_ledR)     #Unregistered
    ledG = GPIO.input(pin_ledG)     #2G
    ledB = GPIO.input(pin_ledB)     #3G
    if ((ledG == 0) or (ledB == 0) or (ledR == 0)):
        debug_print( " On", debug["INFO"] )
        return 0
    else:
        debug_print( " Off", debug["INFO"] )
        return 1
        
#description:   Module Wakeup AP
#input:         none
#return:        1=Wake AP, 0=AP Awake
def gpio_statusMWA():
    debug_print( "GPIO: statusMWA", debug["INFO"] )
    mwa = GPIO.input(pin_mwa)
    if (mwa == 0):
        debug_print( " PIN:MWA - Wake AP", debug["INFO"] )
        return 1
    else:
        debug_print( " PIN:MWA - AP Awake", debug["INFO"] )
        return 0
        
#description:   Module Poweron
#input:         none
#return:        1=off, 0=on
def gpio_statusMP():
    debug_print( "GPIO: statusMP", debug["INFO"] )
    mp = GPIO.input(pin_mp)
    if (mp == 0):
        debug_print( " PIN:MP - Off", debug["INFO"] )
        return 1
    else:
        debug_print( " PIN:MP - On", debug["INFO"] )
        return 0
        
#description:   Module Ready
#input:         none
#return:        0=awake, 1=asleep
def gpio_statusMR():
    debug_print( "GPIO: statusMR", debug["INFO"] )
    mr = GPIO.input(pin_mr)
    if (mr == 0):
        debug_print( " PIN:MR - Awake", debug["INFO"] )
        return 0
    else:
        debug_print( " PIN:MR - Asleep", debug["INFO"] )
        return 1

#-----------------------------------------------------------------------------
# DEBUG COMMANDS -------------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   Print state of network LEDs
#input:         none
#return:        none
def debug_led():
    debug_print( "LED", debug["DEBUG"] )
    debug_print( " ledR: " + str(GPIO.input(pin_ledR)) + " Red   - Not Connected (0 on, 1 off)", debug["DEBUG"] )
    debug_print( " ledG: " + str(GPIO.input(pin_ledG)) + " Green - 2G (0 on, 1 off)", debug["DEBUG"] )
    debug_print( " ledB: " + str(GPIO.input(pin_ledB)) + " Blue  - 3G (0 on, 1 off)", debug["DEBUG"] )

#description:   Print state of status LEDs
#input:         none
#return:        none
def debug_inputs():
    debug_print( "Inputs", debug["DEBUG"] )
    debug_print( " Module Wakeup AP: " + str(GPIO.input(pin_mwa)) + "(0 wake AP, 1 AP awake)", debug["DEBUG"] )
    debug_print( " Module Poweron: " + str(GPIO.input(pin_mp)) + "(0 off, 1 power)", debug["DEBUG"] )
    debug_print( " Module Ready: " + str(GPIO.input(pin_mr)) + "(0 awake, 1 asleep)", debug["DEBUG"] )
    
#description:   debug print function
#input:         none
#return:        none
def debug_print(string, level):     #CHANGE DEBUG LOCATIONS (PRINT/LOG/CONSOLE/etc.)
    if (level <= glob_debug):
        if (debug["CRITICAL"] == level):
            print "CRITICAL:  ", string
        elif (debug["ERROR"] == level):
            print "ERROR:     ", string
        elif (debug["WARNING"] == level):
            print "WARNING:   ", string
        elif (debug["INFO"] == level):
            print "INFO:      ", string
        elif (debug["DEBUG"] == level):
            print "DEBUG:     ", string
        else:
            print "UNDEFINED: ", string
    
#-----------------------------------------------------------------------------
# INFO COMMANDS --------------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   checks the registration status of the SIM card.  
#               Make or break function - must pass this or app should fail
#input:         none
#return:        0=no issue (registered), 1=not registered, needs to alert user
def info_status():                  #+CREG: 0,5 ... OK
    debug_print( "Status", debug["INFO"] )
    tries = 3
    while (tries > 0):
        tries -= 1
        tries1 = 3
        while (tries1 > 0):
            tries1 -= 1
            cmd_ret = cmd_full("at+creg?\r", 3, 1, "CREG:")                 #get "at+creg?" response "CREG:"
            if (cmd_ret == 0):
                matchObj = re.search( r'CREG: \d,(\d)', buffer)             #check what the response is
                if matchObj:
                    re_ret = matchObj.group(1)
                    if ((re_ret == '0') or (re_ret == '3')):
                        debug_print( " SIM card not registering with current network", debug["ERROR"] )
                    elif ((re_ret == '1') or (re_ret == '5')):
                        debug_print( " SIM registered", debug["INFO"] )
                        return 0
                    elif re_ret == '2':
                        debug_print( " SIM still trying to register", debug["INFO"] )
                    elif re_ret == '4':
                        debug_print( " SIM registration unknown", debug["INFO"] )
                    else:
                        debug_print( " Unknown response", debug["ERROR"] )
                else:
                    debug_print( " Unable to retrieve SIM card registration", debug["ERROR"] )
        gpio_toggle()
    return 1
    
    
#-----------------------------------------------------------------------------
# PROCESSING COMMANDS --------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   Setup GPIO for RasPi shield
#input:         none
#return:        none
def cmd_setup():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin_mp,   GPIO.IN)   #(0 off, 1 power)           *poweron module
    GPIO.setup(pin_mwa,  GPIO.IN)   #(0 wake AP, 1 AP awake)    *wakeup AP (host device)
    GPIO.setup(pin_awm,  GPIO.OUT)  #(0 wakeup, 1 sleep)        wakeup module (ZTE modem)
    GPIO.setup(pin_mr,   GPIO.IN)   #(0 awake, 1 asleep)        *module ready - sleep status
    GPIO.setup(pin_ar,   GPIO.OUT)  #(0 wakeup, 1 sleep)        AP ready (host device)
    GPIO.setup(pin_po,   GPIO.OUT)  #(0 on/off, 1 awake)        *power on/off
    GPIO.setup(pin_prn,  GPIO.OUT)  #(0 reset, 1 no reset)      *reset
    GPIO.setup(pin_ledB, GPIO.IN)   #module pulls to 0 to turn LED on
    GPIO.setup(pin_ledR, GPIO.IN)   #module pulls to 0 to turn LED on
    GPIO.setup(pin_ledG, GPIO.IN)   #module pulls to 0 to turn LED on

    GPIO.output(pin_awm, False)
    GPIO.output(pin_ar,  False)
    GPIO.output(pin_po,  True)
    GPIO.output(pin_prn, True)
    
#description:   Cleanup GPIO for RasPi
#input:         none
#return:        none
def cmd_cleanup():
    GPIO.cleanup()                  #clean-up GPIO
    
#description:   Straight write to module serial port
#input:         str - text to write
#return:        none
def cmd_write(str):
    ser.write(str)                  #data to send
    
#description    Check if CELLv1.0 is on, if not, turn it on
#input:         none
#return:        none
def cmd_power():
    tries = 3
    ret = 1
    while (tries > 0):
        tries -= 1
        debug_led()
        debug_inputs()
        
        tries_led=3 #in case the LED is flashing
        while ((tries_led > 0) and (ret != 0)):
            ret &= gpio_ledLit()
            tries_led -= 1;
            sleep(1)
        debug_print( "LED RETURN: " + str(ret) + "(0 1+ LED on, 1 all LEDs off)", debug["DEBUG"] )
        if (ret != 0):
            #ret_status = gpio_statusMR()
            #if (ret_status != 0):
            gpio_turnOn()
        else:
            tries = 0
    if (ret != 0):
        debug_print( "FATAL ERROR - Module is not turning on (Check power)", debug["CRITICAL"] )
        sys.exit(1)

#description    Check if CELLv1.0 is connected to a network, if not, try to connect or fix the issue
#input:         none
#return:        none
def cmd_connection():
    ret = gpio_ledConnected()
    if (ret != 0):
        ret = info_status()                                                 #check SIM registration status - try to fix or turn on if necessary
        if ret:
            debug_print( "FATAL ERROR - Module is not connecting to network (Check antenna and SIM card)", debug["CRITICAL"] )
            sys.exit(1)

#description:   "command" is executed a maximum number of tries with a "delay" in between if fail
#               "buffer" contains valid response matched by "search" or last response if "search not found
#input:         command string, maximum number of tries, delay between each, search string
#return:        0=no issue, 1=error
def cmd_full(string, tries, delay, search = "OK"):
    debug_print( "CMD: Full", debug["INFO"] )
    global buffer
    buffer = ""
    while (tries > 0):              #"command" is executed a maximum number of tries
        #debug_print( "TRY: " + str(tries), debug["DEBUG"] )
        ser.write(string)           #write to modem
        sleep(delay)
        buffer = ser.read(ser.inWaiting())
        matchObj = re.search(search, buffer, re.M)
        if matchObj:
            return 0
        else:
            debug_print( "BUFFER: " + buffer + "\n-----", debug["DEBUG"] )
            tries-=1
    return 1
    
#description:   Specialized function to parse HTML response from a web query
#input:         none
#return:        body without header
def cmd_parseHtmlResponse():
    debug_print( "CMD: Parse HTML Response", debug["INFO"] )
    #matchObj = re.search(r'(Content-Type:.*$)(.*)', buffer, re.S)
    #matchObj = re.search(r'(Content-Type:.*[\n\r])(.*)', buffer, re.S)
    #matchObj = re.search(r'Content-Type:\s+\S+\s+[\n\r]+(.*)', buffer, re.S)
    #matchObj = re.search(r'Content-Type:(\s+\S+\s+[\n\r]+\s\d+)(.*)(ZIPSTAT.+)', buffer, re.S)
    #matchObj = re.search(r'Content-Type:(\s+\S+\s+[\n\r]+\s\d+)(.*)(\d+[\s\n\r]+\+ZIPSTAT.+)', buffer, re.S)
    #matchObj = re.search(r'Content-Type:(\s+\S+\s+[\n\r]+\s\d+)(.*)([\s\n\r]+\d+[\s\n\r]+\+ZIPSTAT.+)', buffer, re.S)
    
    #matchObj = re.search(r'Content-Type:\s+\S+\s+[\n\r]+\s\d+(.*)[\s\n\r]+\d+[\s\n\r]+\+ZIPSTAT.+', buffer, re.S)
    matchObj = re.search(r'Content-Type:\s+\S+\s+[\n\r]+(.*)[\s\n\r]+\+ZIPSTAT.+', buffer, re.S)
    if matchObj:
        #debug_print( " MATCHED (1): " + matchObj.group(1), debug["DEBUG"] )
        return matchObj.group(1)
    else:
        debug_print( " HTML match failed", debug["ERROR"] )
        return 0
        
#-----------------------------------------------------------------------------
# AT COMMANDS ----------------------------------------------------------------
#-----------------------------------------------------------------------------
#NOTE: cmd_full(string, tries, delay, search)

#base AT commands
def at_at():                                        #Quick status
    return cmd_full("at\r", 3, 4);
at_status = at_at
    
def at_ate1():                                      #Enable command echo
    return cmd_full("ate1\r", 3, 4);
at_echoOn = at_ate1
    
def at_ate0():                                      #Disable command echo
    return cmd_full("ate0\r", 3, 4);
at_echoOff = at_ate0
    
def at_creg():                                      #Network registration status
    return cmd_full("at+creg?\r", 3, 4, "CREG");
at_reg = at_creg
    
def at_cops():                                      #List available networks
    return cmd_full("at+cops=?\r", 3, 300, "COPS");
at_nets = at_cops
    
def at_cnti():                                      #Current tech
    return cmd_full("at*cnti?\r", 3, 4);
at_tech = at_cnti
    
def at_csq():                                       #Signal Quality
    return cmd_full("at+csq\r", 3, 4);
at_sig = at_csq

#SMSes
def at_cmgf():                                      #set SMS to plaintext mode
    return cmd_full("at+cmgf=1\r", 3, 4);
    
def at_cmgs(num):                                   #set destination phone number, format "+12223334444"
    return cmd_full("at+cmgs=\"" + num + "\"\r", 3, 4, ">");

def at_cnmiOut():                                   #set SMS to pass incoming directly to output
    return cmd_full("at+cnmi=1,2,0,0,0\r", 3, 4);
    
def at_cmgsMem():                                   #set SMS to pass incoming directly to memory
    return cmd_full("at+cnmi=1,1,0,0,0\r", 3, 4);
    
def at_cmgr(ind):                                   #Read message at index 0
    return cmd_full("at+cmgr=" + str(ind) + "\r", 3, 4);
    
def at_cmgd(ind):                                   #Delete message at index 0
    return cmd_full("at+cmgd=" + str(ind) + "\r", 3, 4);
    
def at_cmgl():                                      #Read all message
    return cmd_full('at+cmgl="all"\r', 3, 4);                             

def at_delSms():
	return cmd_full("at+cmgd=0,2\r",3,4);
#TCP/UDP
def at_zipcallOpen():                               #start call - state 1 open
    return cmd_full("at+zipcall=1\r", 3, 10, "ZIPCALL:")
at_webopen = at_zipcallOpen

def at_zipcallClose():                              #stop call - state 0 close
    return cmd_full("at+zipcall=0\r", 3, 4)
at_webclose = at_zipcallClose

def at_zipopen(socket, type, ip, port):             #socket id,type(UDP=1,TCP=0),hostname/IP,Port
    return cmd_full("at+zipopen=" + str(socket) + "," + str(type) + "," + ip + "," + str(port) + "\r", 3, 4, "ZIPSTAT:")
at_websetup = at_zipopen
    
def at_zipsend(socket):                             #send data
    return cmd_full("at+zipsend=" + str(socket) + "\r", 3, 4, ">")
at_websend = at_zipsend
    
def at_zipwrite(msg):
    cmd_write(msg)
    return cmd_full("\x1A", 1, 10)
at_webmsg = at_zipwrite

#-----------------------------------------------------------------------------
# COMBINED AT COMMANDS -------------------------------------------------------
#-----------------------------------------------------------------------------

#description:   Full SMS send
#input:         num ("+12223334444") - phone number, msg - message to send
#return:        none
def at_sms(num, msg):
    ret = at_cmgf()
    debug_print( "CMGF - Plaintext", debug["DEBUG"] )
    debug_print( "---> CMD RET --->: " + str(ret), debug["DEBUG"] )
    debug_print( "---> BUFFER  --->" + buffer, debug["DEBUG"] )
    if (ret != 0):
        debug_print ("SMS Failed: cmgf", debug["ERROR"] )
        return 1
        
    ret = at_cmgs(num)
    debug_print( "CMGS - Phone #", debug["DEBUG"] )
    debug_print( "---> CMD RET --->: " + str(ret), debug["DEBUG"] )
    debug_print( "---> BUFFER  --->" + buffer, debug["DEBUG"] )
    if (ret != 0):
        debug_print ("SMS Failed: cmgs", debug["ERROR"] )
        return 1
        
    cmd_write(msg)
    debug_print( "WRITE", debug["DEBUG"] )
    ret = cmd_full("\x1A", 1, 10)
    if (ret != 0):
        debug_print ("SMS Failed: finish", debug["ERROR"] )
        return 1
        
    return 0
    
def at_readSms(n):
	ret= at_cmgf()
#	if (ret !=0):
#		debug_print("SMS Failed: cmgf", debug["ERROR"])
#		return 1

	ret = at_cmgr(n)
	#at_cmgsMem()
	#ret= at_cmgl()
	debug_print("---> BUFFER --->"+buffer, debug["DEBUG"])
	#print("RET="+str(ret))
	
	return buffer

def at_readAllSms():
	at_cmgf()
	ret=at_cmgl()
	debug_print("---> BUFFER --->"+buffer, debug["DEBUG"])
	return buffer

def closeSerial():
	ser.close()
