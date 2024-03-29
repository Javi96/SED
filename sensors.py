# -*- coding: utf-8 -*-

'''
    Funcionalidades asociadas al uso de los sensores de movimiento para la detección de infracciones.
    
    Se utilizan los instantes en los que cada sensor detecta movimiento para inferir la velocidad a la que 
    iba el potencial infractor.
    
    Esta velocidad se proporcionará al cliente para que este determine, en función del tipo de vía en el que se 
    establece el radar, si ha producido una infracción.
'''

#Imports del radar
import RPi.GPIO as GPIO
import time
import re
from datetime import datetime
import requests
    

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pir1 = 20
pir2 = 26
dist = 10
time_sensor = list()


GPIO.setup(pir1, GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(pir2, GPIO.IN, GPIO.PUD_DOWN) 

state = 0

detect_1 = False
detect_2 = False

try:
    time.sleep(2)
    print('config completed...')
    while True:
        detect_1 = GPIO.input(pir1)
        detect_2 = GPIO.input(pir2)
        if state == 0 and detect_1:
            detect_1 = False
            aux1 = datetime.now()
            print('pir 1 detected', aux1)
            time_sensor.append(aux1)
            state += 1
            time.sleep(2)
        elif state == 1 and detect_2:
            detect_2 = False
            aux2 = datetime.now()
            print('pir 2 detected', aux2)
            time_sensor.append(aux2)
            
            res = str(dist/(aux2-aux1).total_seconds())
            
            print('result: ', res)
            info = re.sub(r'[\:\.\-\s]', '_', str(aux2))
            url = "http://localhost:5555/informa_infraccion/" + '/'.join([info, res])
            
            r = requests.get(url)    
            
            state = 0
            time.sleep(2)
except Exception as e:
    print(e)
    GPIO.cleanup([pir1, pir2])


# conexion de los pines de los sm --> vcc,gcc,out
