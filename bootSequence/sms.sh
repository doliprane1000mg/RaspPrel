#!/bin/bash
#Deconnecte le modem 3g
#Lecture de l'ensemble des SMS, puis supp
#Redémarrage du modem 3G
#Script to connect to internet through VCELLgsm


#sleep 600
sudo /home/pi/RaspPrel/bootSequence/./sakis3g disconnect 
sudo python /home/pi/RaspPrel/bootSequence/readSms.py
sudo /home/pi/RaspPrel/bootSequence/./orange.sh

