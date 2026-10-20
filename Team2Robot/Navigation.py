from Hardware import *
from LineFollow import LineFollow
from Grab import Grabber

class Navigation:
    def __init__(self):
        self.__line_follow = LineFollow()
        self.__grabber = Grabber()
        self.__ToF = ToF(0)
        self.__hall_sensor = HallSensor(0)
        self.__left_racks = [('l', n) for n in range(3,9)]
        self.__right_racks = [('r', n) for n in range(3,9)]
        self.__upper_left_racks = [('ul', n) for n in range(1,7)]
        self.__upper_right_racks = [('ur', n) for n in range(1,7)]
        self.__boxes = [('l', n) for n in range(3)] + [('r', n) for n in range(3)]
    
    def rack_search(self, racks, last_location, orientation):
        for rack in racks:
            if last_location == 0:
                self.__line_follow.go_from_start(rack, orientation)
            else:
                self.__line_follow.travel_same_side(last_location, rack)
            last_location = rack
            racks.remove(rack)
            if not self.__ToF.object_detected():
                self.__grabber.drop()
                break
            else:
                pass
        return last_location

    
    def main(self):
        self.__line_follow.go_from_start(('l', 1))
        self.__grabber.pick_up()
        if self.__hall_sensor.polarity():
            last_location = ('l',1)
            racks = self.__left_racks
        else:
            self.__line_follow.go_to_start(last_location)
            last_location = 0
            racks = self.__upper_left_racks
        self.rack_search(racks, last_location, 'r')


