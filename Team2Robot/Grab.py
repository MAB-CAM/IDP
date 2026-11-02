from Hardware import *

class Grabber:
    def __init__(self):
        self.__grip_servo = Servo(13)
        self.__lift_servo = Servo(15)
        self.__OPEN_ANGLE = 90
        self.__RACK_OPEN_ANGLE = 70
        self.__CLOSED_ANGLE = 55
        self.__UP_ANGLE = 30
        self.__DOWN_ANGLE = 140
        self.__REQUIREMENT_ANGLE = 200
        self.__lift_servo.set_angle(self.__UP_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__REQUIREMENT_ANGLE)
        sleep(1)

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



    

    


