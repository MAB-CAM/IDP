from machine import Pin

button = Pin(8, Pin.IN)
while True:
    print(button.value())