# TTL_Rec_LED.py
# Needs split trigger to pin 11 and 12 (BCM 17&18)
# Pin 17 incoming TTL
#	1. Records time
#	2. Triggers raspivid
# 	3. 1 s delay
#	4. Records post HIGH time (turn LED on)
#	5. Triggers LED to fire
# Pin 18 event is coded via callback
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
QUES.append({'trialdur': 10000, 'framew': 1920, 'frameh': 1080, 'framerate': 30, 'framedur':8000})
QUES.append({'host_name': 'RPi-C', 'host_ip': '192.168.0.7'})

FN=[]
FN.append({'recdir': QUES[0]['sessionID'],'recfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264" })
FN.append({'bakpath':'/media/ADSDATA'})

host_name = socket.gethostname() # needed for naming files
host_ip = socket.gethostbyname(host_name)
QUES[2]['host_name'] = host_name
QUES[2]['host_ip'] = host_ip

print ("Script running on " + host_name)

# set up general purpose IO port 17 (pin 11)to listen for rising edge; port 23 (pin16) for outgoing 3V current
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.OUT)

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
		GPIO.wait_for_edge(17, GPIO.RISING, bouncetime=300) 
		inout = []
		TTL_time = time.time()
		print ("Edge detected; Batch " + str(batch_num) +" is ongoing.")
		FN[0]['recfile'] = FN[0]['recdir'] + "/" + QUES[0]['sessionID'] +"_"+QUES[2]['host_name']+ "_" + str(batch_ID) + ".h264"
		run_command = ("raspivid -o "+ FN[0]['recfile'] +" -t "+str(QUES[1]['trialdur'])+
		" -w "+str(QUES[1]['framew'])+" -h "+str(QUES[1]['frameh'])+" -fps "+str(QUES[1]['framerate'])+
		" -pf high -ex fixedfps -vf -hf -p '0, 0, 960, 540' -ex off -ss "+str(QUES[1]['framedur']))
		os.system(run_command)
		# save time, fire LED output; save time; write time to disk
		time.sleep(1)
		GPIO.output(23,GPIO.HIGH)## Switch on pin 7
		LED_time = time.time()
		time.sleep(0.2)
		GPIO.output(23,GPIO.LOW)
		inout_times=TTL_time,LED_time
		inout.append(inout_times)
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
