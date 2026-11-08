from machine import Pin
from utime import sleep
#Button is on pin 8- pin HIGH (1) on release
button = Pin(8, Pin.IN, Pin.PULL_UP)


#feedback code for debug
while not button.value():
    sleep(0.05)
    print(button.value())
        
