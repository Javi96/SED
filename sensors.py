import RPi.GPIO as GPIO
import time
from datetime import datetime


# dinero
# fiabilidad
# tasa de fallos




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#led = 21
pir1 = 20
pir2 = 26

time_sensor = list()

#GPIO.setup(led, GPIO.OUT) 
GPIO.setup(pir1, GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(pir2, GPIO.IN, GPIO.PUD_DOWN) 

state = 0

try:
    time.sleep(2)
    # print('config completed...')
    while True:
        if state == 0 and GPIO.input(pir1):
            # print('pir 1 detected', datetime.now())
            time_sensor.append(1)
            state += 1
            time.sleep(2)
        elif state == 1 and GPIO.input(pir2):
            # print('pir 2 detected', datetime.now())
            time_sensor.append(2)
            state += 1
            time.sleep(2)
        elif state == 2:
            # print('result: ')
            print(time_sensor[1])
            state = 0
            time.sleep(2)
except:
    # print('rompe')
    GPIO.cleanup([pir1, pir2])


# conexion de los pines de los sm --> vcc,gcc,out

