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
        return (self.__centre_left_sensor.on_line(), self.__centre_right_sensor.on_line())   
        
    def __calibrated_turn(self, direction):
        self.__wheels.forward()
        sleep(self.__TURN_CALIB)
        self.__wheels.stop()
        direction(self._on_track)
    
    
    def navigate_to(self, start, finish):
        if start != 0:
            self.__wheels.forward()
            while not(self._on_track[0] and self._on_track[1] and self.__left_sensor._on_track and self.__right_sensor._on_track):
                if not self._on_track[0]:
                    
                sleep(0.05)
            self.__wheels.stop()
            if start[0] == 'l' and start[0] == 'r':
                direction = self.__wheels.