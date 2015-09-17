#!/usr/bin/python

#--------------------------------------

def po_turnOn():
	print "PO: TurnOn"
	sleep(1)
	GPIO.output(pin_po, False)
	sleep(1)
	GPIO.output(pin_po, True)

def prn_toggle(): 
	print "PRN: Toggle"
	sleep(1)
	GPIO.output(pin_prn, False)
	sleep(1)
	GPIO.output(pin_prn, True)

def led_read(): 
	print "LED: Read"
	print " ledB: ", GPIO.input(pin_ledB)
	print " ledR: ", GPIO.input(pin_ledR)
	print " ledG: ", GPIO.input(pin_ledG)

def debug_inputs():
	print "DEBUG: Inputs"
	print " Module Wakeup AP: ", GPIO.input(pin_mwa)
	print " Module Poweron: ", GPIO.input(pin_mp)
	print " Module Ready: ", GPIO.input(pin_mr)

#--------------------------------------

try:
	from time import sleep

	import RPi.GPIO as GPIO
	import serial

	#SERIAL
	ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=1)

	GPIO.setmode(GPIO.BOARD)

	pin_mp = 7
	pin_mwa = 11
	pin_ar = 12
	pin_awm = 13
	pin_mr = 15
	pin_po = 16
	pin_prn = 18
	pin_ledR = 22
	pin_ledB = 24
	pin_ledG = 26

	GPIO.setup(pin_mp,   GPIO.IN)
	GPIO.setup(pin_mwa,  GPIO.IN)
	GPIO.setup(pin_awm,  GPIO.OUT)
	GPIO.setup(pin_mr,   GPIO.IN)
	GPIO.setup(pin_ar,   GPIO.OUT)
	GPIO.setup(pin_po,   GPIO.OUT)
	GPIO.setup(pin_prn,  GPIO.OUT)
	GPIO.setup(pin_ledB, GPIO.IN)
	GPIO.setup(pin_ledR, GPIO.IN)
	GPIO.setup(pin_ledG, GPIO.IN)

	GPIO.output(pin_awm, False)
	GPIO.output(pin_ar,  False)
	GPIO.output(pin_po,  True)
	GPIO.output(pin_prn, True)

#--------------------------------------

	print "---> Main DEBUG INPUTS 1:"
	debug_inputs()

	print "---> Main PO TurnOn:"
	po_turnOn()
	sleep(30)

	print "---> Main DEBUG INPUTS 2:"
	debug_inputs()

	print "---"
	#ser.write("ate1\r")
	#sleep(1)
	#ser.write("at+cpin?\r")
	#sleep(1)
	#print ser.read(ser.inWaiting())
	#led_read()
	
	print "---> Main DEBUG INPUTS 3:"
	#debug_inputs()
	sleep(30)

	prn_toggle()
	sleep(30)

	#print "---> Main DEBUG INPUTS 4:"
	#debug_inputs()
	#sleep(30)

finally:
	GPIO.cleanup()


