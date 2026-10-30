from Hardware import *
from LineFollow import LineFollow
from Grab import Grabber

# button pin 0

class Navigation:
    def __init__(self):
        self.__line_follow = LineFollow()
        self.__grabber = Grabber()
        #self.__ToF = ToF(2,3)
        #self.__hall_sensor = HallSensor(28)
        self.__left_racks = [('l', n) for n in range(3,9)]
        self.__right_racks = [('r', n) for n in range(3,9)]
        self.__upper_left_racks = [('ul', n) for n in range(1,7)]
        self.__upper_right_racks = [('ur', n) for n in range(1,7)]
        self.__boxes = [('l', n) for n in range(3)] + [('r', n) for n in range(3)]
        self.__red = LED(10)
        self.__green = LED(11)
        self.__yellow = LED(12)
        
        #self.__ToF.start_sensor()
    
    def rack_search(self, racks, last_location, orientation):
        for rack in racks[:]:
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
        last_location = self.rack_search(racks, last_location, 'r')

        self.__line_follow.travel_same_side(last_location, ('l', 2))
        self.__grabber.pick_up()
        if self.__hall_sensor.polarity():
            last_location = ('l',2)
            racks = self.__left_racks
        else:
            self.__line_follow.go_to_start(last_location)
            last_location = 0
            racks = self.__upper_left_racks
        last_location = self.rack_search(racks, last_location, 'r')

        self.__line_follow.go_to_start(last_location)


    def grabber_test(self):

        #self.__grabber.ready()
        self.__line_follow.go_from_start(('r', 1))
        #self.__grabber.pick_up()
        sleep(2)
        self.__line_follow.travel_same_side(('r',1), ('r',3))
        #sleep(2)
        #self.__line_follow.push_into_rack(self.__grabber.drop, self.__grabber.close)
        #sleep(1)
        #self.__grabber.ready()
        #sleep(2)
        #self.__line_follow.go_to_start(('r',3))








