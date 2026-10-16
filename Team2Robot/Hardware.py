from machine import Pin, PWM
from utime import sleep

class Motor:
    def __init__(self, dir_pin, PWMPin):
        self.mDir = Pin(dir_pin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def stop(self):
        self.pwm.duty_u16(0)
        
    def backward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor
        
    def forward(self, speed=100):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


class Wheels:
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
    
# add a 180 sleep option  
    def left(self, on_line):
        print("GOING LEFT")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        sleep(self.__TURN_SLEEP)
        while not on_line():
            continue
        self.__left_wheel.stop()
        self.__right_wheel.stop()
            
    def right(self, on_line):
        print("GOING RIGHT")
        self.__left_wheel.forward()
        self.__right_wheel.backward()
        sleep(self.__TURN_SLEEP)
        while not on_line():
            continue
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def turn_around(self, on_line):
        print("TURNING AROUND")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        sleep(self.__TURN_AROUND_SLEEP)
        while not on_line():
            continue
        self.__left_wheel.stop()
        self.__right_wheel.stop()
    
    def stop(self):
        print("STOPPING")
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def correct_left(self, on_track):
        self.__right_wheel.forward(60)
        while not on_track():
            continue
        sleep(self.__CORRECTION_TIME)
        self.__right_wheel.forward()
        
    def correct_right(self, on_track):
        self.__left_wheel.forward(60)
        while not on_track():
            continue
        sleep(self.__CORRECTION_TIME)
        self.__left_wheel.forward()
        

class LineSensor:
    def __init__(self, dig_pin):
        self.__sensor = Pin(dig_pin, Pin.IN)

    def on_line(self):
        return self.__sensor.value()
