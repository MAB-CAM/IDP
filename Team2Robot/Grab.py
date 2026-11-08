from Hardware import *

"""Code for grabber: lift servo is connected to rack and pinnion
                     grip servo for forks
                     Requirement angle is a reset point for the start and end of every run to fit the dimensional constraints
"""
class Grabber:
    def __init__(self):
        self.__grip_servo = Servo(13)
        self.__lift_servo = Servo(15)
        self.__OPEN_ANGLE = 90
        self.__RACK_OPEN_ANGLE = 70 # different to open angle as racks pinched grabber
        self.__CLOSED_ANGLE = 55
        self.__UP_ANGLE = 30
        self.__DOWN_ANGLE = 140
        self.__REQUIREMENT_ANGLE = 200
        self.requirement()
        
# open the jaw and raise the fork ready to approach box
    def ready(self):
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)
        

#raise the forks    
    def up(self):
        self.__lift_servo.set_angle(self.__UP_ANGLE)
#lower the forks to minimum height       
    def down(self):
        self.__lift_servo.set_angle(self.__DOWN_ANGLE)
#open jaw to drop box
    def drop(self):
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)
#grip box with forks        
    def close(self):
        self.__grip_servo.set_angle(self.__CLOSED_ANGLE)
        
    def requirement(self):
        self.__lift_servo.set_angle(self.__UP_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__REQUIREMENT_ANGLE)
        sleep(1)



    

    


