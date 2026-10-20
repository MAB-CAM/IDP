from Hardware import *

class Grabber:
    def __init__(self):
        self.__grip_servo = Servo(0)
        self.__lift_servo = Servo(0)
        self.__OPEN_ANGLE = 0
        self.__CLOSED_ANGLE = 0
        self.__UP_ANGLE = 0
        self.__DOWN_ANGLE = 0

    def pick_up(self):
        self.__grip_servo.set_angle(self.__CLOSED_ANGLE)
        sleep(1)
        self.__lift_servo.set_angle(self.__UP_ANGLE)

    def drop(self):
        self.__lift_servo.set_angle(self.__DOWN_ANGLE)
        sleep(1)
        self.__grip_servo.set_angle(self.__OPEN_ANGLE)

