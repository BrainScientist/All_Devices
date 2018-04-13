import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

GPIO.output(18,GPIO.HIGH)## Switch on pin 7
time.sleep(1)
GPIO.output(18,GPIO.LOW)
GPIO.cleanup()
