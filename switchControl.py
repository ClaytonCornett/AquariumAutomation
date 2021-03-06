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
#GPIO.setup(RELAIS_1_GPIO, GPIO.HIGH)

RELAY_3 = 27
GPIO.setup(RELAY_3, GPIO.OUT) #Relay 3, light
#GPIO.output(RELAY_3, GPIO.LOW) #Starts light on
#GPIO.output(RELAY_3, GPIO.HIGH)

RELAY_2 = 22
GPIO.setup(RELAY_2, GPIO.OUT) #Relay 2, Non custom feeder
#GPIO.output(RELAY_2, GPIO.LOW)
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

heaterOn = False
heaterOff = True

tempCheck1 = False
tempCheck2 = False
tempCheck3 = False

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
    global heaterOn
    global heaterOff

    global tempCheck1
    global tempCheck2
    global tempCheck3

    if int(hour) == 10 and tempCheck1 == False:
	print("Temperature: ",temp, "F at ", heater_time)
	tempCheck1 = True
    if int(hour) == 16 and tempCheck2 == False:
	print("Temperature: ",temp, "F at ", heater_time)
	tempCheck2 = True
    if int(hour) == 22 and tempCheck3 == False:
	print("Temperature: ",temp, "F at ", heater_time)
	tempCheck3 = True
    
    if int(hour) == 23:
        tempCheck1 = False
        tempCheck2 = False
        tempCheck3 = False
    
    
    if float(temp) > 80.0 and heaterOn == True: #if temp higher than 80 turn off heater
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # heater off
        print("Heater Off: ", heater_time)
	heaterOn = False
	heaterOff = True
    if float(temp) < 77.0 and heaterOff == True: 
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # heater on
        print("Heater On: ", heater_time)
	heaterOn = True
	heaterOff = False
	#print(temp)

def control_light():    #Controls light based on time of day
    t = time.localtime()
    light_time = time.strftime("%m/%d/%Y at %H:%M:%S", t)
    hour = time.strftime("%H", t)
    #minute = time.strftime("%M", t)
    global lightOff
    global lightOn

    if int(hour) == 10 and lightOff == True:
        GPIO.output(RELAY_3, GPIO.LOW) # turns light on at 10am
        lightOn = True
        lightOff = False
        print("---------------------------------------------")
        print("Light On: ", light_time)

    if int(hour) == 22 and lightOn == True:
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
    global nonCustomFeederOn
    global nonCustomFeederNeeded
    global mealDaysRemaining
    if nonCustomFeederOn == False and nonCustomFeederNeeded == True:
        if int(hour) == 11: #Only turns on feeder at 11 in order to keep track
            nonCustomFeederOn = True
            GPIO.output(RELAY_2, GPIO.LOW)
            print("Non Custom Feeder On: ", feeder_time)

    if nonCustomFeederOn == True and nonCustomFeederNeeded == True:
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
    print("Start of program")
    GPIO.output(17, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(27, GPIO.LOW)
    print("Inital Light turn on")
    lightOn = True
    lightOff = False
    time.sleep(3)
    while True:
        control_light()
        control_heater()
        #control_noncustom_feeder()
        time.sleep(1)

except KeyboardInterrupt:
    print("Keyboard Interrupt ended script")

except:
    print("Other exception occured")

finally:
    GPIO.cleanup() #clean exit


