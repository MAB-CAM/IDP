from machine import Pin, PWM, ADC, I2C, SoftI2C
from libs.VL53L0X.VL53L0X import VL53L0X
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
        self.__TURN_SLEEP = 0.6 
        self.__TURN_AROUND_SLEEP = 1
        
    def forward(self):
        print("GOING FORWARD")
        self.__left_wheel.forward()
        self.__right_wheel.forward()
        
    def backward(self):
        print("GOING BACKWARD")
        self.__left_wheel.backward()
        self.__right_wheel.backward()

    def left(self, on_line, timed=False, time=0):
        # turning axis is midpoint between wheels
        print("GOING LEFT")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        if timed:
            sleep(time)
        else:
            sleep(self.__TURN_SLEEP) 
            #  above we sleep for the majority of the turn to avoid early detection
            # (e.g. a different close by line)
            while not on_line():
                continue
            # only stop turning when we're back on the line
        self.__left_wheel.stop()
        self.__right_wheel.stop()
            
    def right(self, on_track, timed=False, time=0):
        # turning axis is midpoint between wheels
        print("GOING RIGHT")
        self.__left_wheel.forward()
        self.__right_wheel.backward()
        if timed:
            sleep(time)
        else:
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
        self.__left_wheel.forward(100)
        while not on_track():
            continue
        sleep(self.__CORRECTION_TIME)
        # sleep a short time period to ensure the bot is straight
        self.__right_wheel.forward()
        
    def correct_right(self, on_track):
        # this method is used to correct movement to stay on the line
        self.__left_wheel.forward(60)
        self.__right_wheel.forward(100)
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



class LED:
    def __init__(self, led_pin):
        self.__led = Pin(led_pin, Pin.OUT)
        
    def on(self):
        self.__led.value(1)
        
    def off(self):
        self.__led.value(0)
        
        

class HallSensor:
    def __init__(self, sensor):
        self.__sensor = ADC(sensor)
        self.__NORTH = 45000
        self.__SOUTH = 30000

    def __read(self):
        return self.__sensor.read_u16()
    
    def polarity(self):
        reading = 0
        for i in range(100):
            reading += self.__sensor.read_u16()
        reading /= 100
        if reading > self.__NORTH:
            return True
        elif reading < self.__SOUTH:
            return False
        else:
            return None


class Infrared:
    def __init__(self, dig_pin):
        self.__sensor = Pin(dig_pin, Pin.IN)

    def reading(self):
        return self.__sensor.value()


class ToF:
    def __init__(self, sda, scl):
        sda_pin = Pin(sda)
        scl_pin = Pin(scl)
        i2c_bus = SoftI2C(sda=sda_pin, scl=scl_pin) # I2C0 on GP8 & GP9
        
        # Setup vl53l0 object
        self.__vl53l0 = VL53L0X(i2c_bus)
        self.__vl53l0.set_Vcsel_pulse_period(self.__vl53l0.vcsel_period_type[0], 18)
        self.__vl53l0.set_Vcsel_pulse_period(self.__vl53l0.vcsel_period_type[1], 14)

    def start_sensor(self):
        self.__vl53l0.start()
    
    def __distance(self):
        return self.__vl53l0.read()
    
    def box_detected(self):
        return self.__distance() < 120

    def stop_sensor(self):
        self.__vl53l0.stop()
    
if __name__ == "__main__":
    wheels = Wheels()
    wheels.stop()




