from hardware import *
from machine import Pin, PWM

class 

def init
        self.__servo1 = Servo1(21)
        self.__servo2 = Servo2(20)
        self.__Hall_Sensor = HallSensor(19)
        self.__ToF_Sensor = ToFSensor(18)
        
from machine import Pin, PWM

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


from machine import Pin, PWM
import time

class Servo:
    # Common settings for 270° servos:
    # 0.5 ms → minimum (0°)
    # 2.5 ms → maximum (270°)
    # Total span = 2.0 ms
    # Frequency: 50 Hz (20 ms period)
    # 
    # Duty % = Pulse width / Period x 100
    # Minimum (0°) = 0.5/20
    # Centre (135°) = 1.5/20
    # Maximum (270°) = 2.5/20
    #
    # Convert to Pico PWM (16-bit)
    # Pico uses: 0 → 65535
    # Duty value = Duty Fraction x 65535
    # Minimum (0.5 ms) = 0.025 * 65535
    # Centre (1.5 ms) = 0.075 * 65535
    # Maximum (2.5 ms) = 0.0125 * 65535
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°
    
    def __init__(self, ServoPin):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo
 
    # Convert angle (0–270) to duty
    def set_angle(self, angle):
       # Clamp angle
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
       self.servo.duty_u16(duty)


# Test Code
servo1 = Servo(Pin(15)) # Connected to Servo 1