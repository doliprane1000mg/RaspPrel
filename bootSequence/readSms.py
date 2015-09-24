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
    debugFile=open("/home/pi/RaspPrel/log/smsLog","a+")
    
   # SparqEE.at_cmgsMem()	
    sms=SparqEE.at_readAllSms()
   # test=sms.split("+CMGL") 
   # print("Printing sms:"+sms)
    retour=sms.split('+CMGL')
 #   retour= [ v for v in retour if not v.startswith("at")]
#    print("retour="+retour[0]+ "taille=" + str(len(retour)))
    cmp=1
    ret=-1
    #gotNum=False
    #gotMsg=False
    print("Taille retour="+str(len(retour)))
    for v in retour: 
	print("****************************************************")
	print("Sms["+str(cmp)+"]:"+v)
	print("****************************************************")
	print("\n")
	cmp=cmp+1
    print("fin test")   
    for cmp  in range(1,len(retour)):
   		
   	chaine=retour[cmp]
	chaine=chaine.split("\n")
	print('split:'+chaine[0].split(',')[0])
	debugFile.write(retour[cmp])
#	if(str[0].startswith("+CMGL")): #Verifie qu'il ne s'agit pas d'une trame vide. 
    	numero=(chaine[0].split(','))[2] 
	numero=numero[1:-1]#Remove quote
	#	gotNum=True
#    	else:
	message=chaine[1]
	message= "RASPBERRY ACCUSE RECEPTION:"+"\n"+message+"\n"+"HEURE:"+str(datetime.now())
	#	gotMessage=True
       #	if(gotNum and gotMessage):   
 	ret=SparqEE.at_sms(numero,message)
	#	gotNum=False
	#	gotMessage=False
    
    	if(ret==0):
		SparqEE.at_delSms()
    debugFile.close()
    SparqEE.cmd_cleanup()
    SparqEE.closeSerial()    		    
except:
    SparqEE.debug_print( "***END (exception)***", SparqEE.debug["CRITICAL"] )
    SparqEE.cmd_cleanup()           #clean-up shield GPIO
    SparqEE.closeSerial()
    print "Unexpected error:", sys.exc_info()[0]
    raise
