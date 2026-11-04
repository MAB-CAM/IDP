from Hardware import *
from LineFollow import LineFollow
from Grab import Grabber

# button pin 0

class Navigation:
    def __init__(self):
        self.__line_follow = LineFollow()
        self.__grabber = Grabber()
        self.__ToF = ToF(2,3)
        self.__hall_sensor = HallSensor(28)
        rack_order = (4,1,5,2,6,3)
        left_racks = [('l', n+2) for n in rack_order]
        right_racks = [('r', n+2) for n in rack_order]
        upper_left_racks = [('ul', n) for n in rack_order]
        upper_right_racks = [('ur', n) for n in rack_order]
        self.__racks = {'l': [left_racks, upper_left_racks], 'r': [right_racks, upper_right_racks]}
        self.__boxes = [('l', 1), ('l', 2), ('r', 1), ('r', 3)]
        self.__red = LED(10)
        self.__green = LED(11)
        
        self.__ToF.start_sensor()
    
    def __rack_search(self, racks, last_location):
        for rack in racks.copy():
            self.__line_follow.travel_same_side(last_location, rack)
            last_location = rack
            racks.remove(rack)
            sleep(1)
            if self.__ToF.box_detected():
                continue
            else:              
                self.__line_follow.small_entry(rack=True)
                sleep(1)
                self.__grabber.drop()
                sleep(1)
                self.__line_follow.small_exit()
                sleep(1)
                break

        return last_location

    
    def main(self):
        # TO DO: LEDs, ensure hall sensor and ToF are working, button for main file
        last_location = (0,0)
        for box in self.__boxes:
            sleep(1)
            self.__grabber.ready()
            if last_location[0] == box[0]:
                self.__line_follow.travel_same_side(last_location, box)
            else:
                orientation = 'f' if last_location==(0,0) else self.__line_follow.go_to_start(last_location) 
                self.__line_follow.go_from_start(box, orientation)
            sleep(1)
            self.__grabber.down()
            sleep(1)
            self.__line_follow.small_entry()
            sleep(1)
            self.__grabber.close()
            sleep(1)
            polarity = self.__hall_sensor.polarity()
            self.__grabber.up()
            sleep(1)
            if not polarity:
                assigned_led = self.__green
                assigned_led.on()
                racks = self.__racks[box[0]][0]
            else:
                assigned_led = self.__red
                assigned_led.on()
            last_location = box
            if last_location[1] == 3:
                last_location = (last_location[0], 2)
            racks = self.__racks[box[0]][0]
            last_location = self.__rack_search(racks, last_location)
            assigned_led.off()
        self.__line_follow.go_to_start(last_location)
        


    def grabber_test(self):
        self.__grabber.ready()
        self.__line_follow.go_from_start(('r', 1))
        sleep(1)
        self.__grabber.down()
        sleep(1)
        self.__line_follow.small_entry()
        sleep(1)
        self.__grabber.close()
        sleep(1)
        self.__grabber.up()
        sleep(1)
        self.__line_follow.travel_same_side(('r',1), ('r',3))
        sleep(1)
        self.__line_follow.small_entry()
        sleep(1)
        self.__grabber.drop()
        sleep(1)
        self.__line_follow.small_exit()
        sleep(1)
        self.__line_follow.go_to_start(('r',3))
        
    
    def tof_test(self):
        self.__grabber.ready()
        sleep(1)
        self.__grabber.down()
        sleep(1)
        self.__line_follow.small_entry()
        sleep(1)
        self.__grabber.close()
        sleep(1)
        self.__grabber.up()
        while True:
            sleep(0.5)
            print(self.__ToF.__distance())












