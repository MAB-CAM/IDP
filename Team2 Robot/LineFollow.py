from Hardware import *

class LineFollow:
    def __init__(self):
        self.__left_sensor = LineSensor()
        self.__centre_left_sensor = LineSensor()
        self.__centre_right_sensor = LineSensor()
        self.__right_sensor = LineSensor()
        self.__wheels = Wheels()
        
    def __on_track(self):
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line()
    
    def __exit_box_location(self):
        # we could reverse or turn around
        # we could implement turning as part of this class or wheels class
        # for turning we could overshoot and then correct or calibrate from when sensors notice the turn
        
    
    def __exit_shelf_location(self):
        
    
    def navigate_to(self, start, finish):
        