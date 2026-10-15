from Hardware import *

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
        
    def __stay_on_line():
        if not self.__centre_left_sensor.on_line():
            self.__wheels.correct_right(self._on_track)
        elif not self.__centre_right_sensor.on_line():
            self.__wheels.correct_left(self._on_track)
    
    # def go_to_start(self, start)
    
    def navigate_to(self, finish):
        if start != 0:
            self.__wheels.left()
            self.__wheels.left()
            self.__wheels.forward()
            while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                self__stay_on_line()
                sleep(0.05)
            self.__wheels.stop()
            same_side = False
            if start[0] == 'l' and finish[0] == 'r':
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            elif start[0] == 'r' and finish[0] == 'l':
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor
            elif start[0] == 'l' and finish[0] == 'l':
                same_side = True
                if start[1] < finish[1]:
                    direction = self.__wheels.right
                else:
                    direction = self.__wheels.left
                    turn_sensor = self.__left_sensor
            elif start[0] == 'r' and finish[0] == 'r':
                same_side = True
                if start[1] < finish[1]:
                    direction = self.__wheels.left
                    turn_sensor = self.__left_sensor
                else:
                    direction = self.__wheels.right
            self.__calibrated_turn(direction)
            
            if same_side:
                count = abs(start[1] - end[1])
                if start_count > 3:
                    count -= 1
                self.__wheels.forward()
                while count > 0:
                    self.__stay_on_line()
                    if turn_sensor.on_line():
                        if not previously_on:
                            count -= 1
                            previously_on = True
                    else:
                        previously_on = False
                self.__calibrated_turn(direction)
                self.__wheels.forward()
                if end < 3:
                    while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                        self__stay_on_line()
                        sleep(0.05)
                else:
                    pass
                self.__wheels.stop()
                
            else:
                start_count = start[1]
                end_count = end[1]
                previously_on = False
                if start_count > 3:
                    start_count -= 1
                self.__wheels.forward()
                while start_count > 0:
                    self.__stay_on_line()
                    if turn_sensor.on_line():
                        if not previously_on:
                            start_count -= 1
                            previously_on = True
                    else:
                        previously_on = False
                self.__calibrated_turn(direction)
                
                mid_count = 2
                previously_on = False
                self.__wheels.forward()
                while mid_count > 0:
                    self.__stay_on_line()
                    if self._on_track and self.__left_sensor.on_line() and self.__right_sensor.on_line():
                        if not previously_on:
                            mid_count -= 1
                            previously_on = True
                    else:
                        previously_on = False
                sleep(0.5)
                while not turn_sensor.on_line():
                    self.__stay_on_line()
                self.__calibrated_turn(direction)
                
                previously_on = False
                self.__wheels.forward()
                while end_count > 0:
                    self.__stay_on_line()
                    if turn_sensor.on_line():
                        if not previously_on:
                            end_count -= 1
                            previously_on = True
                    else:
                        previously_on = False
                self.__calibrated_turn(direction)
                
                self.__wheels.forward()
                if end < 3:
                    while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                        self__stay_on_line()
                        sleep(0.05)
                else:
                    pass
                self.__wheels.stop()
                
        else:
            if finish[0] == 'r':
                self.__calibrated_turn(self.__wheels.right)
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            elif finish[0] == 'l':
                self.__calibrated_turn(self.__wheels.left)
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor
            mid_count = 1
            previously_on = False
            self.__wheels.forward()
            while mid_count > 0:
                self.__stay_on_line()
                if self._on_track and self.__left_sensor.on_line() and self.__right_sensor.on_line():
                    if not previously_on:
                        mid_count -= 1
                        previously_on = True
                else:
                    previously_on = False
            sleep(0.5)
            while not turn_sensor.on_line():
                self.__stay_on_line()
            self.__calibrated_turn(direction)
            
            previously_on = False
            self.__wheels.forward()
            while end_count > 0:
                self.__stay_on_line()
                if turn_sensor.on_line():
                    if not previously_on:
                        end_count -= 1
                        previously_on = True
                else:
                    previously_on = False
            self.__calibrated_turn(direction)
            
            self.__wheels.forward()
            if end < 3:
                while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                    self__stay_on_line()
                    sleep(0.05)
            else:
                pass
            self.__wheels.stop()
            
                    
