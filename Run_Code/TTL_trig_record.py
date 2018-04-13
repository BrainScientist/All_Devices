# RPi_C_TTL_trigger.py
# for Pi-3, called RPi-C. Photron TTL Triggers 70 sec recording 
#  via port 17 (pin 11). Set up to label folders &  files for this Pi.
# Avinash Bala, Jul 2016
import os
import time
import RPi.GPIO as GPIO
import socket
import pickle

##Script must be run as root (sudo -s before initializing)

#Preferences
QUES = []
QUES.append({'sub': 'b001', 'session': '01', 'date': '160513', 'sessionID': '160513_b001_01'})
QUES.append({'trialdur': 120000, 'framew': 1920, 'frameh': 1080, 'framerate': 30, 'framedur':8000})
QUES.append({'host_name': 'RPi-C', 'host_ip': '192.168.0.7'})

FN=[]
FN.append({'recdir': QUES[0]['sessionID'],'recfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264" })
FN.append({'bakpath':'/media/ADSDATA'})

host_name = socket.gethostname() # needed for naming files
host_ip = socket.gethostbyname(host_name)
QUES[2]['host_name'] = host_name
QUES[2]['host_ip'] = host_ip

print ("Script running on " + host_name)

# set up general purpose IO port 17 to listen to rising edge of pulse
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

batch_num = 1 # batch = 15 trials with gifts going up +down
QUES[0]['sub']=raw_input("Input subject ID: ") # get user input for subject ID
session_num = raw_input("Input Session number:  ")
QUES[0]['session'] = session_num.zfill(2) 
QUES[0]['date'] = str(time.strftime("%y%m%d"))
QUES[0]['sessionID'] = QUES[0]['date'] + "_" + QUES[0]['sub'] + "_" + QUES[0]['session']
print("Ready to record Session: " + QUES[0]['sessionID'])
FN[0]['recdir']=(QUES[0]['sessionID']+"_"+QUES[2]['host_name'])
os.system("mkdir "+FN[0]['recdir'])
os.system("chmod 777 " +FN[0]['recdir'])

print("Now listening for TTL.")
#Begin loop
try:
	while True:
		batch_ID = ('{0:02d}'.format(batch_num))
		print "Waiting for TTL on port 17"  
		GPIO.wait_for_edge(17, GPIO.RISING) 
		print ("Edge detected; Batch " + str(batch_num) +" is ongoing.")
		FN[0]['recfile'] = FN[0]['recdir'] + "/" + QUES[0]['sessionID'] +"_"+QUES[2]['host_name']+ "_" + str(batch_ID) + ".h264"
		run_command = ("raspivid -o "+ FN[0]['recfile'] +" -t "+str(QUES[1]['trialdur'])+
		" -w "+str(QUES[1]['framew'])+" -h "+str(QUES[1]['frameh'])+" -fps "+str(QUES[1]['framerate'])+
		" -pf high -ex fixedfps -vf -hf -p '0, 0, 960, 540' -ex off -ss "+str(QUES[1]['framedur']))
		os.system(run_command)
		os.system("chmod 777 " +FN[0]['recfile'])
                w_file = open((FN[0]['recdir']+"/"+FN[0]['recdir']+"_var.txt"),'w')
                pickle.dump((QUES,FN,batch_num),w_file)
                w_file.close()
		batch_num=batch_num + 1
except KeyboardInterrupt:
	print(" Quitting script")
        w_file = open((FN[0]['recdir']+"/"+FN[0]['recdir']+"_var.txt"),'w')
        pickle.dump((QUES,FN,batch_num),w_file)
        w_file.close()
	GPIO.cleanup()
GPIO.cleanup()
