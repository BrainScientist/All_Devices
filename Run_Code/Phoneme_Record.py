# TTL_LED.py
# 120 sec recording from circular buffer.
# Video prior to trigger is also stored.
# Square 'MC2 recording' pulse Photron is receieved via port 17 (pin 11) triggers recording.
# TTL trigger delivered from RP2-IO pin7 received port 18 (pin 11) to triggers LED flash.
# Set up to label folders &  files for ttRPi-C.
# Avinash Bala, Oct 2016
import os
import io
import time
import pickle
import socket
import RPi.GPIO as GPIO

##Script must be run as root (sudo -s before initializing)

#Preferences
QUES = []
QUES.append({'sub': 'b001', 'session': '01', 'date': '160513', 'sessionID': '160513_b001_01'})
QUES.append({'trialdur': 900000, 'framew': 800, 'frameh': 800, 'framerate': 30, 'framedur':8000})
QUES.append({'host_name': 'RPi-C', 'host_ip': '192.168.0.7'})

FN=[]
FN.append({'recdir': QUES[0]['sessionID'],'recfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264",'datfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264"})
FN.append({'bakpath':'/media/ADSDATA'})
datfile = FN[0]['datfile']
host_name = socket.gethostname() # needed for naming files
host_ip = socket.gethostbyname(host_name)
QUES[2]['host_name'] = host_name
QUES[2]['host_ip'] = host_ip

print ("Script running on " + host_name)

QUES[0]['sub']=raw_input("Input subject ID: ") # get user input for subject ID
session_num = raw_input("Input Session number:  ")
QUES[0]['session'] = session_num.zfill(2) 
QUES[0]['date'] = str(time.strftime("%y%m%d"))
QUES[0]['sessionID'] = QUES[0]['date'] + "_" + QUES[0]['sub'] + "_" + QUES[0]['session']
print("Ready to record Session: " + QUES[0]['sessionID'])
FN[0]['recdir']=(QUES[0]['sessionID']+"_"+QUES[2]['host_name'])
os.system("mkdir "+FN[0]['recdir'])
os.system("chmod 777 " +FN[0]['recdir'])

#Set pin low to sense rising slope of the TTL
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.OUT)

nbatch=0

# define GPIO event for triggering LED
def fireLED(channel):
    #GPIO.wait_for_edge(18, GPIO.RISING)
    datfile = FN[0]['recdir'] + "/" + QUES[0]['sessionID'] +"_"+QUES[2]['host_name']+"GPIO_times.txt"
    inout = []
    TTL_time = time.time()
    #time.sleep(1)
    GPIO.output(23,GPIO.HIGH)## Switch on pin 7
    LED_ONtime = time.time()
    time.sleep(0.1)
    GPIO.output(23,GPIO.LOW)## Switch off pin 7
    LED_OFFtime = time.time()
    inout_times=TTL_time,LED_ONtime,LED_OFFtime
    inout.append(inout_times)
    print(inout_times)
    print ("LED was triggered.")
    #if file already exists, load the data and append to it
    if os.path.exists(datfile):
        # "with" statements are very handy for opening files.
        with open(datfile,'rb') as rfp:
            inout = pickle.load(rfp)
            # "with" statements are very handy for opening files.
            # Notice that there's no "rfp.close()"
            #   ... the "with" clause calls close() automatically!
            inout.append(inout_times)
            with open(datfile,'wb') as wfp:
                pickle.dump(inout, wfp)
    else:
        with open(datfile,'wb') as wfp:
                pickle.dump(inout, wfp)
                

GPIO.add_event_detect(18, GPIO.RISING, callback=fireLED, bouncetime=300)
    
try:
        while True:
                FN[0]['recfile'] = FN[0]['recdir'] + "/" + QUES[0]['sessionID'] +"_"+QUES[2]['host_name']+ "_" + str(nbatch) + ".h264"
                run_command = ("raspivid -o "+ FN[0]['recfile'] +" -t "+str(QUES[1]['trialdur'])+
		" -w "+str(QUES[1]['framew'])+" -h "+str(QUES[1]['frameh'])+" -fps "+str(QUES[1]['framerate'])+
		" -pf high -ex fixedfps -vf -hf -p '0, 0, 960, 540' -ex off -ss "+str(QUES[1]['framedur']))
                print ("Waiting for TTL on port 17")
                GPIO.wait_for_edge(17, GPIO.RISING, bouncetime=300)
                os.system(run_command)
                print('Edge detected')
                nbatch += 1
except KeyboardInterrupt:
    	print(" Quitting script")
        GPIO.cleanup()
GPIO.cleanup()
