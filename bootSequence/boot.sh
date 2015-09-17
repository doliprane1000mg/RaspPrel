#!/bin/bash
#Script to connect to internet through VCELLgsm
#sleep 20
echo "-------------------------------------------------" >> /home/pi/RaspPrel/bootSequence/bootLog
date >> /home/pi/RaspPrel/bootSequence/bootLog
sudo python /home/pi/RaspPrel/bootSequence/./powerOnGsm.py
sudo /home/pi/RaspPrel/bootSequence/./sakis3g connect --console --nostorage --pppd APN="internet-entreprise" BAUD =115200 CUSTOM_TTY="/dev/ttyAMA0" MODEM="OTHER" OTHER="CUSTOM_TTY"  APN_USER="orange" APN_PASS="orange"  >> /home/pi/RaspPrel/bootSequence/bootLog


