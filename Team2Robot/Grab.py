from Hardware import *

class Grabber:
    def __init__(self):
        self.__grip_servo = Servo(13)
        self.__lift_servo = Servo(15)
        self.__OPEN_ANGLE = 90
        self.__RACK_OPEN_ANGLE = 60.5
        self.__CLOSED_ANGLE = 60
        self.__UP_ANGLE = 40
        self.__DOWN_ANGLE = 150
        self.__REQUIREMENT_ANGLE = 200
        self.__lift_servo.set_angle(self.__UP_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__REQUIREMENT_ANGLE)

    def ready(self):
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)
    
    def pick_up(self):
        self.__lift_servo.set_angle(self.__DOWN_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__CLOSED_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)

    def drop(self):
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)
        
    def close(self):
        self.__grip_servo.set_angle(self.__CLOSED_ANGLE)



    

    


