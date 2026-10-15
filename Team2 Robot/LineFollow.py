from Hardware import *

class LineFollow:
    def __init__(self):
        self.__left_sensor = LineSensor()
        self.__centre_left_sensor = LineSensor()
        self.__centre_right_sensor = LineSensor()
        self.__right_sensor = LineSensor()
        self.__wheels = Wheels()
        self.__TURN_CALIB = 0.5
        
    def _on_track(self):
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line()   
        
    def __calibrated_turn(self, direction):
        self.__wheels.forward()
        sleep(self.__TURN_CALIB)
        self.__wheels.stop()
        direction(self._on_track)
    
    
    def navigate_to(self, start, finish):
        if start != 0:
            # turn around the vehicle
            self.__wheels.forward()
            while not(self._on_track and self.__left_sensor._on_track and self.__right_sensor._on_track):
                if not self.__centre_left_sensor.on_line():
                    self.__wheels.correct_right(self._on_track)
                elif not self.__centre_right_sensor.on_line():
                    self.__wheels.correct_left(self._on_track)
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
            
            if same_side:
                # pass
            else:
                self.__calibrated_turn(direction)
                start_count = start[1]
                end_count = end[1]
                if start_count > 3:
                    
                while True:
                    if not self.__centre_left_sensor.on_line():
                        self.__wheels.correct_right(self._on_track)
                    elif not self.__centre_right_sensor.on_line():
                        self.__wheels.correct_left(self._on_track)
                    if self
                    
