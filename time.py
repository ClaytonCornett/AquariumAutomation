import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
new_time = time.strftime("%m/%d/%Y at %H:%M:%S", t)
hour = time.strftime("%H", t)
minute = time.strftime("%M", t)
print(current_time)
print("Hour: ", hour)
print("Minute: ", minute)

if int(hour) == 21:
    print("hour works")

if int(minute) == 7:
    print("min works")

print(new_time)
