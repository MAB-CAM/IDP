from machine import Pin, PWM
from utime import sleep, ticks_ms, ticks_diff

class Motor:
    def __init__(self, dir_pin, PWMPin):
        self.mDir = Pin(dir_pin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def stop(self):
        self.pwm.duty_u16(0)
        
    def backward(self, speed=100):
        self.mDir.value(0)                     
        self.pwm.duty_u16(int(65535 * speed / 100))
        
    def forward(self, speed=100):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


class Wheels:
    '''
    This class is used for wheel synchronisation, allowing for easier use
    by LineFollow class. Includes methods for moving forwards and backwards,
    turning, and correcting path for line following.
    '''
    def __init__(self):
        self.__left_wheel = Motor(4,5)
        self.__right_wheel = Motor(7,6)
        self.__CORRECTION_TIME = 0.02 
        self.__TURN_SLEEP = 0.4 
        self.__TURN_AROUND_SLEEP = 1
        
    def forward(self):
        print("GOING FORWARD")
        self.__left_wheel.forward()
        self.__right_wheel.forward()
        
    def backward(self):
        print("GOING BACKWARD")
        self.__left_wheel.backward()
        self.__right_wheel.backward()

    def left(self, on_line):
        # turning axis is midpoint between wheels
        print("GOING LEFT")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        sleep(self.__TURN_SLEEP) 
        #  above we sleep for the majority of the turn to avoid early detection
        # (e.g. a different close by line)
        while not on_line():
            continue
        # only stop turnign when we're back on the line
        self.__left_wheel.stop()
        self.__right_wheel.stop()
            
    def right(self, on_track):
        # turning axis is midpoint between wheels
        print("GOING RIGHT")
        self.__left_wheel.forward()
        self.__right_wheel.backward()
        sleep(self.__TURN_SLEEP)
        #  above we sleep for the majority of the turn to avoid early detection
        # (e.g. a different close by line)
        while not on_track():
            continue
        # only stop turning when we're back on the line
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def turn(self, on_track):
        # this method is used for 180 degree turns
        print("TURNING AROUND")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        sleep(self.__TURN_AROUND_SLEEP)
        # above we sleep for majority of the turn to avoid early detection
        # (e.g. a different close by line)
        while not on_track():
            continue
        # only stop turning when we're back on the line
        self.__left_wheel.stop()
        self.__right_wheel.stop()
    
    def stop(self):
        print("STOPPING")
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def correct_left(self, on_track):
        # this method is used to correct movement to stay on the line
        self.__right_wheel.forward(60)
        while not on_track():
            continue
        sleep(self.__CORRECTION_TIME)
        # sleep a short time period to ensure the bot is straight
        self.__right_wheel.forward()
        
    def correct_right(self, on_track):
        # this method is used to correct movement to stay on the line
        self.__left_wheel.forward(60)
        while not on_track():
            continue
        sleep(self.__CORRECTION_TIME)
        # sleep a short time period to ensure the bot is straight
        self.__left_wheel.forward()
        

class LineSensor:
    '''
    This class represents a line sensor component which reads a digit
    output from the component (high means line detected)
    '''
    def __init__(self, dig_pin):
        self.__sensor = Pin(dig_pin, Pin.IN)

    def on_line(self):
        return self.__sensor.value()