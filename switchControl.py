import time
import RPi.GPIO as GPIO
import os
import glob
import time

time.sleep(2)

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) #Relay 4, Heater

RELAY_3 = 27
GPIO.setup(RELAY_3, GPIO.OUT) #Relay 3, light

RELAY_2 = 22
GPIO.setup(RELAY_2, GPIO.OUT) #Relay 2, Non custom feeder
mealsPerDay = 2
mealDaysRemaining = 7  #These vars keep track of when to turn off feeder
nonCustomFeederNeeded = True #Will not be used until needed
nonCustomFeederOn = False

os.system('modprobe w1-gpio')   #Temp Sensor
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]  #Temp Sensor
device_file = device_folder + '/w1_slave'


lightOn = False
lightOff = True

def read_temp_raw():    #Reads raw data for sensor
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():        #Reads temp in F for sensor
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_f

def control_heater():
    t = time.localtime()
    heater_time = time.strftime("%m/%d/%Y at %H:%M:%S", t)
    hour = time.strftime("%H", t)
    temp = read_temp()

    if int(hour) == 10 or int(hour) == 16 or int(hour) == 22:
        print("Temperature: ",temp, "F at ", heater_time)
    
    if float(temp) > 80.0: #if temp higher than 80 turn off heater
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # heater off
        print("Heater Off: ", heater_time)
    else: #heater off
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # heater on
        print("Heater On: ", heater_time)
	#print(temp)

def control_light():    #Controls light based on time of day
    t = time.localtime()
    light_time = time.strftime("%m/%d/%Y at %H:%M:%S", t)
    hour = time.strftime("%H", t)
    #minute = time.strftime("%M", t)

    if int(hour) == 10 and lightOff == True:
        GPIO.output(RELAY_3, GPIO.LOW) # turns light on at 10am
        lightOn = True
        lightOff = False
        print("---------------------------------------------")
        print("Light On: ", light_time)

    if int(hour) == 22:
        GPIO.output(RELAY_3, GPIO.HIGH) #turns off light at 10pm
        lightOff = True
        lightOn = False
        print("Non Custom Feeder Meal Days Remaining: ", mealDaysRemaining)
        print("Light Off: ", light_time)
        print("---------------------------------------------")

def control_noncustom_feeder():
    t = time.localtime()
    feeder_time = time.strftime("%m/%d/%Y at %H:%M:%S", t)
    hour = time.strftime("%H", t)
    if nonCustomFeederOn is False and nonCustomFeederNeeded is True:
        if int(hour) == 11: #Only turns on feeder at 11 in order to keep track
            nonCustomFeederOn = True
            GPIO.output(RELAY_2, GPIO.LOW)
            print("Non Custom Feeder On: ", feeder_time)

    if nonCustomFeederOn is True and nonCustomFeederNeeded is True:
        if int(hour) == 11:
            print("Non Custom Feeder morning: ", feeder_time)
        if int(hour) == 20:
            print("Non Custom Feeder afternoon: ", feeder_time)
            mealDaysRemaining = mealDaysRemaining - 1 #subtracts at end of day

        if mealDaysRemaining == 0: #Turns off feeder when out of food
            GPIO.output(RELAY_2, GPIO.HIGH)
            nonCustomFeederOn = False
            print("Non Custom Feeder Off: ", feeder_time)

try:
    while True:
        control_light()
        control_heater()
        control_noncustom_feeder()
        time.sleep(1)

#except KeyboardInterrupt:
    print("Keyboard Interrupt ended script")

#except:
    print("Other exception occured")

finally:
    GPIO.cleanup() #clean exit


