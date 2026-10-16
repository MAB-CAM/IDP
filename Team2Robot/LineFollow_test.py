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
        self.__CORRECTION_TIME = 0.02
        
    def forward(self):
        print("GOING FORWARD")
        self.__left_wheel.forward()
        self.__right_wheel.forward()
        
    def backward(self):
        print("GOING BACKWARD")
        self.__left_wheel.backward()
        self.__right_wheel.backward()
    
    def left(self, on_line, rack=False):
        print("GOING LEFT")
        self.__left_wheel.backward()
        self.__right_wheel.forward()
        if rack:
            count = 2
        else:
            count = 1
        previously_on = True
        while count > 0:
            if on_line():
                if not previously:
                    count -= 1
                    previously = True
            else:
                previously_on = False
        self.__left_wheel.stop()
        self.__right_wheel.stop()
            
    def right(self, on_line, rack=False):
        print("GOING RIGHT")
        self.__left_wheel.forward()
        self.__right_wheel.backward()
        if rack:
            count = 2
        else:
            count = 1
        previously_on = True
        while count > 0:
            if on_line():
                if not previously:
                    count -= 1
                    previously = True
            else:
                previously_on = False
        self.__left_wheel.stop()
        self.__right_wheel.stop()
    
    def stop(self):
        print("STOPPING")
        self.__left_wheel.stop()
        self.__right_wheel.stop()
        
    def correct_left(self, on_track):
        print("CORRECTING LEFT")
        self.__left_wheel.forward(80)
        while not on_track():
            sleep(0.05)
        sleep(self.CORRECTION_TIME)
        self.__left_wheel.forward()
        print("CORRECTED")
        
    def correct_right(self, on_track):
        print("CORRECTING RIGHT")
        self.__right_wheel.forward(80)
        while not on_track():
            sleep(0.05)
        sleep(self.CORRECTION_TIME)
        self.__right_wheel.forward()
        print("CORRECTED")
        

class LineSensor:
    def __init__(self, dig_pin):
        self.__sensor = Pin(dig_pin, Pin.IN)

    def on_line(self):
        return self.__sensor.value()




class LineFollow:
    def __init__(self):
        self.__left_sensor = LineSensor(21)
        self.__centre_left_sensor = LineSensor(20)
        self.__centre_right_sensor = LineSensor(19)
        self.__right_sensor = LineSensor(18)
        self.__wheels = Wheels()
        self.__TURN_CALIB = 0.5
        
    def _on_track(self):
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line()   
        
    def __calibrated_turn(self, direction):
        self.__wheels.forward()
        sleep(self.__TURN_CALIB)
        self.__wheels.stop()
        direction(self._on_track)
        
    def __stay_on_line(self):
        if not self.__centre_left_sensor.on_line():
            self.__wheels.correct_right(self._on_track)
        elif not self.__centre_right_sensor.on_line():
            self.__wheels.correct_left(self._on_track)
    
    def __travel_with_counter(self, turn_detect, count, previously_on = False):
        self.__wheels.forward()
        while count > 0:
            self.__stay_on_line()
            if turn_detect():
                if not previously_on:
                    count -= 1
                    print("REDUCING COUNT BY 1")
                    previously_on = True
            else:
                previously_on = False
    
    def go_to_start(self, start):
        self.__wheels.left()
        self.__wheels.left()
        # need to edit 180 above
        self.__wheels.forward()
        while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
            self__stay_on_line()
            sleep(0.05)
        self.__wheels.stop()
        same_side = False
        if start[0] == 'l':
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        print(direction, turn_sensor)
        self.__calibrated_turn(direction)
        
        print("DIFFERENT SIDE")
        start_count = start[1]
        if start_count > 3:
            print("THIS IS A RACK BAY")
            start_count -= 1
        self.__travel_with_counter(start_count, turn_sensor)
        self.__calibrated_turn(direction)
        print("FINISHED START SIDE")
        
        mid_count = 2
        self.__travel_with_counter(start_count, lambda x: self._on_track() and self.__left_sensor.on_line() and self.__right_sensor.on_line())
        self.__wheels.stop()
        print("RETURNED TO START")
        
    
    def go_from_start(self, finish, orientation='f'):
        if orientation == 'f':
            if finish[0] == 'l':
                self.__wheels.left()
            if finish[0] == 'r':
                self.__wheels.right()
        print("GOING FROM START")
        if finish[0] == 'r':
            self.__calibrated_turn(self.__wheels.right)
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif finish[0] == 'l':
            self.__calibrated_turn(self.__wheels.left)
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        mid_count = 2
        previously_on = False if orientation=='f' else True
        self.__travel_with_counter(turn_sensor, mid_count, previously_on)
        self.__calibrated_turn(direction)
        
        print("NOW ON CORRECT SIDE")
        previously_on = False
        self.__travel_with_counter(turn_sensor, finish[1])
        self.__calibrated_turn(direction)
        
        self.__wheels.forward()
        print("FINISHING UP")
        if end < 3:
            while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                self__stay_on_line()
                sleep(0.05)
        else:
            pass # implement final travel to rack
        self.__wheels.stop()
        
    print("NAVIGATION FINISHED")
    
    
    def travel_same_side(self, start, finish):
        self.__wheels.left()
        self.__wheels.left()
        # need to edit 180 above
        self.__wheels.forward()
        while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
            self__stay_on_line()
            sleep(0.05)
        self.__wheels.stop()
        same_side = False
        if start[0] == 'l':
            if start[1] < finish[1]:
                direction = self.__wheels.right
            else:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            if start[1] < finish[1]:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            else:
                direction = self.__wheels.right   
        print(direction, turn_sensor)
        self.__calibrated_turn(direction)
        
        print("SAME SIDE")
        count = abs(start[1] - end[1])
        if start_count > 3:
            count -= 1
            print("THIS IS A RACK BAY")
        self.__travel_with_counter(turn_sensor, count)
        self.__calibrated_turn(direction)
        self.__wheels.forward()
        print("FINISHING UP")
        if end < 3:
            while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                self__stay_on_line()
                sleep(0.05)
        else:
            pass # perhaps implement as new method (finish route)
        self.__wheels.stop()
        
    
            
                    






if __name__ == "__main__":
    a = Wheels()
    a.backward()
    sleep(0.55)
    a.stop()
    a.right()
    