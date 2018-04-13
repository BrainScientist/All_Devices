import time
import RPi.GPIO as GPIO
import pickle
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18,GPIO.OUT)
ntrials = 1 
datfile = "GPIO_times.txt"
#Begin loop
try:
	while True:
		GPIO.wait_for_edge(17, GPIO.RISING) 
		inout = []
		TTL_time = time.time()
		time.sleep(1)
		GPIO.output(18,GPIO.HIGH)## Switch on pin 7
		LED_time = time.time()
		time.sleep(0.5)
		GPIO.output(18,GPIO.LOW)
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
			
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()			
