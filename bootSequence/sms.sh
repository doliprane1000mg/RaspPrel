#!/bin/bash
#Deconnecte le modem 3g
#Lecture de l'ensemble des SMS, puis supp
#Redémarrage du modem 3G
#Script to connect to internet through VCELLgsm

while true
do
	sleep 10
	date >> /home/pi/RaspPrel/bootSequence/smsLog
	echo 'Trying to disconnect 3g' >> /home/pi/RaspPrel/bootSequence/smsLog
	sudo /home/pi/RaspPrel/bootSequence/./sakis3g disconnect 
	sudo python /home/pi/RaspPrel/bootSequence/readSms.py
	sudo /home/pi/RaspPrel/bootSequence/./sakis3g connect --console --nostorage --pppd APN="internet-entreprise" BAUD =115200 CUSTOM_TTY="/dev/ttyAMA0" MODEM="OTHER" OTHER="CUSTOM_TTY"  APN_USER="orange" APN_PASS="orange"  >> /home/pi/RaspPrel/bootSequence/bootLog
	
done



