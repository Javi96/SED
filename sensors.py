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


import random

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = round(random.randint(0, 5), 2)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()




def execute_rasp():
	