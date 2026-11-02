from machine import Pin
from utime import sleep

button = Pin(8, Pin.IN, Pin.PULL_UP)

while not button.value():
    sleep(0.05)
    print(button.value())
        
