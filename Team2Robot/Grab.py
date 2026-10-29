from machine import Pin, PWM, ADC, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep

class Servo:
    def __init__(self, pin_num):
        self.__pwm = PWM(Pin(pin_num))
        self.__pwm.freq(50)              # 20 ms period
        # duty_u16 = (pulse / 20 ms) * 65535: 0.5 ms -> 1638, 2.5 ms -> 8192
        self.__MIN_DUTY = 1638           # 0°
        self.__MAX_DUTY = 8192           # 270°
        self.__RANGE = 270
        self.__CENTRE = 135

    def set_angle(self, angle):
        angle = max(0, min(self.__RANGE, angle))
        duty = int(self.__MIN_DUTY + (angle / self.__RANGE) * (self.__MAX_DUTY - self.__MIN_DUTY))
        self.__pwm.duty_u16(duty)

    def centre(self):
        self.set_angle(self.__CENTRE)

    def release(self):
        self.__pwm.duty_u16(0)           # no pulses -> servo goes limp

class Grabber:
    def __init__(self):
        self.__grip_servo = Servo(13)
        self.__lift_servo = Servo(15)
        self.__OPEN_ANGLE = 90
        self.__RACK_OPEN_ANGLE = 60.5
        self.__CLOSED_ANGLE = 60
        self.__UP_ANGLE = 50
        self.__DOWN_ANGLE = 160
        self.__REQUIREMENT_ANGLE = 200
        #self.__lift_servo.set_angle(self.__UP_ANGLE)
        sleep(1)
        #self.__grip_servo.set_angle(self.__REQUIREMENT_ANGLE)

    def ready(self):
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)
    
    def pick_up(self):
        self.__lift_servo.set_angle(self.__DOWN_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__CLOSED_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)

    def drop(self):
        self.__grip_servo.set_angle(self.__RACK_OPEN_ANGLE)



    
if __name__ == "__main__":
    grabber = Grabber()
    '''
    sleep(2)
    grabber.ready()
    sleep(2)
    grabber.pick_up()
    sleep(2)
    grabber.drop()
    '''
    grabber.__lift_servo.set_angle(20)
