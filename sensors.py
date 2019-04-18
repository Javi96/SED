import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = 21
pir1 = 23
pir2 = 20

time = list()

GPIO.setup(led, GPIO.OUT) 
GPIO.setup(pir1, GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(pir2, GPIO.IN, GPIO.PUD_DOWN) 

state = 0

try:
	sleep(5)
	print('config completed...')
	while True:
		if state == 0: # reconocer primer objeto
			if GPIO.input(pir1):
				print('pir 1 detected')
				time.append(datetime.now())
				state += 1
		elif state == 1: # reconocer segundo objeto
			if GPIO.input(pir2):
				print('pir 2 detected')
				time.append(datetime.now())
				state += 1
		elif state == 2: # calcular infracción
			print('result: ')
			print((time[1]-time[0]).seconds)
			state = 0
except: 
	GPIO.cleanup([led, pir1, pir2])
