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
        left_racks = [('l', n) for n in range(3,9)]
        right_racks = [('r', n) for n in range(3,9)]
        upper_left_racks = [('ul', n) for n in range(1,7)]
        upper_right_racks = [('ur', n) for n in range(1,7)]
        self.__racks = {'l': [left_racks, upper_left_racks], 'r': [right_racks, upper_right_racks]}
        self.__boxes = [('l', n) for n in range(3)] + [('r', n) for n in range(3)]
        self.__red = LED(10)
        self.__green = LED(11)
        
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
                self.__line_follow.push_into_rack(self.__grabber)
                break
            else:
                pass
        return last_location

    
    def main(self):
        # TO DO: LEDs, ensure hall sensor and ToF are working, button for main file
        last_location = 0
        for box in self.__boxes:
            if last_location[0] == box[0]:
                self.__line_follow.travel_same_side(last_location, box)
            else:
                orientation = 'f' if not last_location else self.__line_follow.go_to_start(last_location) 
                self.__line_follow.go_from_start(box, orientation)
            self.__grabber.pick_up()
            sleep(1)
            if self.__hall_sensor.polarity():
                last_location = box
                racks = self.__racks[box[0]][0]
            else:
                self.__line_follow.go_to_start(box)
                last_location = 0
                racks = self.__racks[box[0]][1]
            orientation = 'r' if box[0] == 'l' else 'r'
            last_location = self.rack_search(racks, last_location, orientation)


    def grabber_test(self):

        self.__grabber.ready()
        self.__line_follow.go_from_start(('r', 1))
        self.__grabber.pick_up()
        sleep(2)
        self.__line_follow.travel_same_side(('r',1), ('r',3))
        sleep(1)
        self.__grabber.drop()
        sleep(1)
        self.__line_follow.go_to_start(('r',3))










