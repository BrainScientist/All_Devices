# TTL_CircRec_led.py
# 120 sec recording from circular buffer.
# Video prior to trigger is also stored.
# Square 'MC2 recording' pulse Photron is receieved via port 17 (pin 11) triggers recording.
# TTL trigger delivered from RP2-IO pin7 received port 18 (pin 11) to triggers LED flash.
# Set up to label folders &  files for ttRPi-C.
# Avinash Bala, Oct 2016
import os
import io
import time
import socket
import pickle
import picamera
import RPi.GPIO as GPIO

##Script must be run as root (sudo -s before initializing)

# Load variables 
QUES = []
QUES.append({'sub': 'b001', 'session': '01', 'date': '160513', 'sessionID': '160513_b001_01'})
QUES.append({'trialdur': 3000, 'framew': 1920, 'frameh': 1080, 'framerate': 30, 'framedur':8000}, 'ISO':8000)
QUES.append({'host_name': 'RPi-C', 'host_ip': '192.168.0.7'})
# Filenames
FN=[]
FN.append({'recdir': QUES[0]['sessionID'],'recfile': QUES[0]['sessionID'] + "/" + QUES[0]['sessionID'] + "_01.h264" })
FN.append({'bakpath':'/media/ADSDATA'})
# Get Pi name to include in filename
host_name = socket.gethostname() # needed for naming files
host_ip = socket.gethostbyname(host_name)
QUES[2]['host_name'] = host_name
QUES[2]['host_ip'] = host_ip

#Set pin low to sense rising slope of the TTL
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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

# define GPIO event for triggering LED
def fireLED(channel):
	GPIO.wait_for_edge(18, GPIO.RISING) 
	inout = []
	TTL_time = time.time()
	time.sleep(1)
	GPIO.output(23,GPIO.HIGH)## Switch on pin 7
	LED_time = time.time()
	time.sleep(0.1)
	GPIO.output(23,GPIO.LOW)
	inout_times=TTL_time,LED_time
	inout.append(inout_times)
	print ("Edge detected; Trial " + str(ntrials) +" was triggered.")
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

GPIO.add_event_detect(18, GPIO.RISING, callback=fireLED, bouncetime=300)

def cam_vars():
    camera.resolution = (1920, 1080)
    camera.framerate = QUES[1]['framerate']
    camera.shutter_speed = QUES[1]['framedur']
    camera.ISO = QUES[1]['ISO']
    camera.hflip = True
    camera.vflip = True
    
    camera.exposure_mode = 'off'
    
try:
	while True:
		batch_ID = ('{0:02d}'.format(batch_num))
		print "Waiting for TTL on port 17"
		FN[0]['recfile'] = FN[0]['recdir'] + "/" + QUES[0]['sessionID'] +"_"+QUES[2]['host_name']+ "_" + str(batch_ID) + ".h264"
		with picamera.PiCamera() as camera:
			stream = picamera.PiCameraCircularIO(camera, seconds=(QUES[1]['trialdur'])/1000)
			cam_vars()
			camera.start_preview()
			camera.preview.window = 0,0,960,540
			camera.start_recording(stream, format='h264')
			GPIO.wait_for_edge(17, GPIO.RISING, bouncetime=300)
			camera.wait_recording(120)
			print('Edge detected')
			camera.stop_recording()
			camera.stop_preview()
			for frame in stream.frames:
				if frame.header:
					stream.seek(frame.position)
					break
			with io.open('FN[0]['recfile']', 'wb') as output:
				while True:
					data = stream.read1()
					if not data:
						break
					output.write(data)
			os.system("chmod 777 " +FN[0]['recfile'])
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()