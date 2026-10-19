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
        
    def turn_around(self, on_track):
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



class LineFollow:
    '''
    This class brings together the motors and line sensors to keep the robot
    navigating. This includes partial navigation between the start, boxes, and racks.
    '''
    def __init__(self):
        self.__left_sensor = LineSensor(18)
        self.__centre_left_sensor = LineSensor(20)
        self.__centre_right_sensor = LineSensor(19)
        self.__right_sensor = LineSensor(21)
        self.__wheels = Wheels()
        self.__TURN_CALIB = 0.5
        
    def _on_track(self):
        # this method is used to check if the robot is still on the line via the front two sensors
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line()
    
    def __all_sensors_on(self):
        # this method checks if all the sensors are on a line (usually for a turn leaving a box/rack location or stopping before a box)
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line() and self.__left_sensor.on_line() and self.__right_sensor.on_line()
        
    def __calibrated_turn(self, direction):
        # utilises wheels turning alongside moving forward a bit first to ensure the sensors end up on the line
        self.__wheels.forward()
        sleep(self.__TURN_CALIB)
        self.__wheels.stop()
        direction(self._on_track)

        
    def __stay_on_line(self):
        # line following using wheels movement correction to keep middle sensors on the line
        if not self.__centre_left_sensor.on_line():
            self.__wheels.correct_right(self._on_track)
        elif not self.__centre_right_sensor.on_line():
            self.__wheels.correct_left(self._on_track)
    
    def __travel_with_counter(self, turn_detect, count, previously_on = False):
        # when going to a location we have to count the turns we've passed to know
        # which one we should take, which is what this method does
        self.__wheels.forward()
        while count > 0:
            self.__stay_on_line()
            if turn_detect():
                if not previously_on:
                    count -= 1
                    print("REDUCING COUNT BY 1")
                    previously_on = True
                    # when we pass a turn we can reduce the count, and make previously_on
                    # true so we don't reduce extra counts
            else:
                previously_on = False
                # knows when we're off the current turn and now we can discretely sense another
                
    def __exit_location(self, rack):
        # this method is used to leave a line (box or rack) and go onto a main branch of the course
        print("EXITING LOCATION")
        if rack:
            self.__wheels.turn(self._on_track)
            # if on a rack we just do a 180
        else:
            self.__calibrated_turn(self.__wheels.turn)
            # if at a box location we have to go forward a bit so when
            # we turn around the sensors aren't off the line
        self.__wheels.forward()
        while not self.__all_sensors_on():
            self.__stay_on_line()
            # keep following line until we reach end of the location to turn onto a main branch
        self.__wheels.stop()
        
    def __enter_location(self, rack):
        print("ENTERING LOCATION")
        self.__wheels.forward()
        if rack:
            start_time = ticks_ms()
            condition = lambda: ticks_diff(ticks_ms(), start_time) < 1600
        else:
            condition = lambda: not self.__all_sensors_on()
        while condition():
            self.__stay_on_line()
        self.__wheels.stop()
        print("LOCATION ENTERED")

    
    def go_to_start(self, start):
        rack = True if start[1] >= 3 else False
        self.__exit_location(rack)
        if start[0] == 'l':
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        print(direction, turn_sensor)
        self.__calibrated_turn(direction)
        
        start_count = start[1]
        if start_count > 3:
            start_count -= 1
        self.__travel_with_counter(turn_sensor.on_line, start_count)
        self.__calibrated_turn(direction)
        print("FINISHED START SIDE")
        
        mid_count = 2
        self.__travel_with_counter(self.__all_sensors_on, mid_count)
        self.__wheels.stop()
        print("RETURNED TO START")
        
    
    def go_from_start(self, finish, orientation='f'):
        if orientation == 'f':
            if finish[0] == 'l':
                self.__wheels.left(self._on_track)
            if finish[0] == 'r':
                self.__wheels.right(self._on_track)
        print("GOING FROM START")
        if finish[0] == 'r':
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif finish[0] == 'l':
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        mid_count = 2
        self.__travel_with_counter(turn_sensor.on_line, mid_count)
        self.__calibrated_turn(direction)
        
        print("NOW ON CORRECT SIDE")
        finish_counter = finish[1]
        self.__travel_with_counter(turn_sensor.on_line, finish_counter)
        self.__calibrated_turn(direction)
        
        rack = True if finish[1] >= 3 else False
        self.__enter_location(rack)
        
        
    
    
    def travel_same_side(self, start, finish):
        rack = True if start[1] >= 3 else False
        self.__exit_location(rack)
        if start[0] == 'l':
            if start[1] < finish[1]:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor
            else:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            if start[1] < finish[1]:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            else:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor  
        self.__calibrated_turn(direction)
        
        print("SAME SIDE")
        count = abs(start[1] - finish[1])
        self.__travel_with_counter(turn_sensor.on_line, count)
        # add calibrated turn for rack - issues with rack to rack movement - perhaps split this method into categories
        # could alternate and then turn around odd/even
        self.__calibrated_turn(direction)
        
        rack = True if finish[1] >= 3 else False
        self.__enter_location(rack)

        


if __name__ == "__main__":
    a = LineFollow()
    sleep(1)
    a.go_from_start(('r',2))
    print("COMING BACK")
    a.travel_same_side(('r',2), ('r', 3))
    #a.__wheels.stop()