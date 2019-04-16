import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BMC)

pir = 20
led = 21

GPIO.setup(pir, GPIO.IN) 
GPIO.setup(led, GPIO.OUT) 

while True:
	if GPIO.input(pir):
		GPIO.output(led, 1)   
		time.sleep(1)     
		GPIO.output(led, 0)   
