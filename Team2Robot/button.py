from machine import Pin

button = Pin(8, Pin.IN, Pin.PULL_UP)
while True:
    print(button.value())