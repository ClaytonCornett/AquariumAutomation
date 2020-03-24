import time
import RPi.GPIO as GPIO
import os
import glob
import time

time.sleep(2)

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) #Relay 4, Heater
#GPIO.setup(RELAIS_1_GPIO, GPIO.LOW) #starts heater on

RELAY_3 = 27
GPIO.setup(RELAY_3, GPIO.OUT) #Relay 3, light
#GPIO.output(RELAY_3, GPIO.LOW) #Starts light on

RELAY_2 = 22
GPIO.setup(RELAY_2, GPIO.OUT) #Relay 2, Non custom feeder
mealsPerDay = 2
mealDaysRemaining = 7  #These vars keep track of when to turn off feeder
nonCustomFeederNeeded = True #Will not be used until needed
nonCustomFeederOn = False


try:
    while True:
        time.sleep(3)
        GPIO.output(17, GPIO.LOW)
	print("17 Low")
        time.sleep(3)
        GPIO.output(17, GPIO.HIGH)
	print("17 High")
        
        time.sleep(3)
        GPIO.output(27, GPIO.LOW)
	print("27 Low")
        time.sleep(3)
        GPIO.output(27, GPIO.HIGH)
	print("27 High")
        
        time.sleep(3)
        GPIO.output(22, GPIO.LOW)
	print("22 Low")
        time.sleep(3)
        GPIO.output(22, GPIO.HIGH)
	print("22 High")

	time.sleep(3)
	print("27 Low")
	GPIO.output(27, GPIO.LOW)
	time.sleep(3)
	print("17 Low")
	GPIO.output(17, GPIO.LOW)

except KeyboardInterrupt:
    print("Keyboard Interrupt ended script")

except:
    print("Other exception occured")

finally:
    GPIO.cleanup() #clean exit


