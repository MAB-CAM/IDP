from Hardware import *
from utime import ticks_ms, ticks_diff

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
        
    def __enter_location(self, rack, upper_flag):
        print("ENTERING LOCATION")
        self.__wheels.forward()
        if upper_flag:
            rack_time = 1200
        else:
            rack_time = 1600
        if rack:
            start_time = ticks_ms()
            condition = lambda: ticks_diff(ticks_ms(), start_time) < rack_time
        else:
            condition = lambda: not self.__all_sensors_on()
        while condition():
            self.__stay_on_line()
        self.__wheels.stop()
        print("LOCATION ENTERED")

    
    def go_to_start(self, start):
        upper_flag = start[0] == "ul" or start[0] == "ur"
        rack = True if start[1] >= 3 or upper_flag else False
        self.__exit_location(rack, upper_flag)
        if start[0] == 'l' or start[0] == "ur":
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif start[0] == 'r' or start[0] == "ul":
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        print(direction, turn_sensor)
        self.__calibrated_turn(direction)
        
        if start[1]>3 and not upper_flag:
            start_count -= 1
        if start[1] == 1 and upper_flag:
            start_count += 1
        self.__travel_with_counter(turn_sensor.on_line, start_count)
        print("FINISHED START SIDE")

        if not upper_flag:
            self.__calibrated_turn(direction)
            mid_count = 2
            self.__travel_with_counter(self.__all_sensors_on, mid_count)
            self.__wheels.stop()
            print("RETURNED TO START")
        
    
    def go_from_start(self, finish, orientation='f'):
        upper_flag = False
        if orientation == 'f':
            if finish[0] == 'l':
                self.__wheels.left(self._on_track)
            if finish[0] == 'r':
                self.__wheels.right(self._on_track)
        if orientation == 'b':
            if finish[0] == 'l':
                self.__wheels.right(self._on_track)
            if finish[0] == 'r':
                self.__wheels.left(self._on_track)

        if finish[0] == "ul" or finish[0] == "ur":
            upper_flag = True
            if orientation == 'l':
                self.__wheels.right(self._on_track)
            if orientation == 'r':
                self.__wheels.left(self._on_track)
        print("GOING FROM START")
        if finish[0] == 'r' or finish[0] == "ul":
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif finish[0] == 'l' or finish[0] == "ur":
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        if not upper_flag:
            mid_count = 2
            self.__travel_with_counter(turn_sensor.on_line, mid_count)
            self.__calibrated_turn(direction)
        
        print("NOW ON CORRECT SIDE")
        finish_counter = finish[1]
        self.__travel_with_counter(turn_sensor.on_line, finish_counter)
        self.__calibrated_turn(direction)
        
        rack = True if finish[1] >= 3 or upper_flag else False
        self.__enter_location(rack, upper_flag)
        
        
    def travel_same_side(self, start, finish):
        upper_flag = start[0] == "ul" or start[0] == "ur"
        rack = True if start[1] >= 3 or upper_flag else False
        self.__exit_location(rack)
        if start[0] == 'l' or start[0] == "ur":
            if start[1] < finish[1]:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor
            else:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
        elif start[0] == 'r' or start[0] == "ul":
            if start[1] < finish[1]:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            else:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor  
        self.__calibrated_turn(direction)
        
        print("SAME SIDE")
        count = start[1] - finish[1]
        if (rack or upper_flag) and count >= 1:
            self.__motors.backward()
            sleep(0.3) # instead could alternate and then turn around odd/even, or could turn straight away for single move
        self.__travel_with_counter(turn_sensor.on_line, abs(count))
        self.__calibrated_turn(direction)
        
        rack = True if finish[1] >= 3 or upper_flag else False
        self.__enter_location(rack, upper_flag)


    def switch_upper_rack(self, start, finish):
        pass
    
        