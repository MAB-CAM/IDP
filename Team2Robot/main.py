from Navigation import *
from _thread import start_new_thread

def flashing(led, operating):
    while operating:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
        
        
if __name__ == "__main__":
    button = Pin(8, Pin.IN, Pin.PULL_UP)
    yellow_led = LED(12)
    nav = Navigation()  
    while not button.value():
        sleep(0.05)
        print(button.value())
    operating = True
    start_new_thread(flashing, (yellow_led, operating))
    nav.main()
    operating = False


    



