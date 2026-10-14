class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def stop(self):
        self.pwm.duty_u16(0)
        
    def forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def backward(self, speed=100):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


class Wheels:
    def __init__(self):
        self.__left_wheel = Motor(4,5)
        self.__right_wheel = Motor(7,6)
        self.__CORRECTION_TIME = 0.5
        
    def forward(self):
        self.__left_wheel.forward()
        self.__right_wheel.forward()
    
    def left(self, on_track):
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        while not on_track():
            sleep(0.05)
            
    def right(self, on_track):
        self.__left_wheel.forward()
        self.__right_wheel.backward()
        while not on_track():
            sleep(0.05)
    
    def stop(self):
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def correct_left(self):
        self.__left_wheel.forward(80)
        sleep(self.CORRECTION_TIME)
        self.__left_wheel.forward()
        
    def correct_right(self):
        self.__right_wheel.forward(80)
        sleep(self.CORRECTION_TIME)
        self.__right_wheel.forward()
        
        