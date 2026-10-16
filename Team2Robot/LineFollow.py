from Hardware import *

class LineFollow:
    def __init__(self):
        self.__left_sensor = LineSensor(18)
        self.__centre_left_sensor = LineSensor(20)
        self.__centre_right_sensor = LineSensor(19)
        self.__right_sensor = LineSensor(21)
        self.__wheels = Wheels()
        self.__TURN_CALIB = 0.5
        
    def _on_track(self):
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line()
    
    
    def __all_sensors_on(self):
        return self.__centre_left_sensor.on_line() and self.__centre_right_sensor.on_line() and self.__left_sensor.on_line() and self.__right_sensor.on_line()
        
    def __calibrated_turn(self, direction, rack=False):
        self.__wheels.forward()
        sleep(self.__TURN_CALIB)
        self.__wheels.stop()
        direction(self._on_track)

        
    def __stay_on_line(self):
        if not self.__centre_left_sensor.on_line():
            self.__wheels.correct_right(self._on_track)
        elif not self.__centre_right_sensor.on_line():
            self.__wheels.correct_left(self._on_track)
    
    def __travel_with_counter(self, turn_detect, count, previously_on = False):
        self.__wheels.forward()
        while count > 0:
            self.__stay_on_line()
            if turn_detect():
                if not previously_on:
                    count -= 1
                    print("REDUCING COUNT BY 1")
                    previously_on = True
            else:
                previously_on = False
                
    def __exit_location(self, rack):
        print("EXITING LOCATION")
        if rack:
            self.__wheels.turn(self._on_track)
        else:
            self.__calibrated_turn(self.__wheels.turn)
        self.__wheels.forward()
        while not(self._on_track() and self.__left_sensor.on_line() and self.__right_sensor.on_line()):
            self.__stay_on_line()
        self.__wheels.stop()
        
    def __enter_location(self, rack):
        print("ENTERING LOCATION")
        self.__wheels.forward()
        if rack:
            sleep(1.6)
        else:
            while not(self._on_track() and self.__left_sensor.on_line() and self.__right_sensor.on_line()):
                self.__stay_on_line()
        self.__wheels.stop()

    
    def go_to_start(self, start, rack=False):
        self.__exit_location(rack)
        if start[0] == 'l':
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        print(direction, turn_sensor)
        self.__calibrated_turn(direction)
        
        start_count = start[1]
        if start_count > 3:
            start_count -= 1
        self.__travel_with_counter(turn_sensor.on_line, start_count)
        self.__calibrated_turn(direction)
        print("FINISHED START SIDE")
        
        mid_count = 2
        self.__travel_with_counter(self.__all_sensors_on, mid_count)
        self.__wheels.stop()
        print("RETURNED TO START")
        
    
    def go_from_start(self, finish, orientation='f'):
        if orientation == 'f':
            if finish[0] == 'l':
                self.__wheels.left(self._on_track)
            if finish[0] == 'r':
                self.__wheels.right(self._on_track)
        print("GOING FROM START")
        if finish[0] == 'r':
            direction = self.__wheels.left
            turn_sensor = self.__left_sensor
        elif finish[0] == 'l':
            direction = self.__wheels.right
            turn_sensor = self.__right_sensor
        mid_count = 2
        self.__travel_with_counter(turn_sensor.on_line, mid_count, previously_on)
        self.__calibrated_turn(direction)
        
        print("NOW ON CORRECT SIDE")
        previously_on = False
        finish_counter = finish[1]
        self.__travel_with_counter(turn_sensor.on_line, finish_counter)
        if finish_counter > 2:
            self.__calibrated_turn(direction, rack=True)
        
        rack = True if finish[1] >= 3 else False
        self.__enter_location(rack)
    
    
    def travel_same_side(self, start, finish, rack=False):
        self.__exit_location(rack)
        if start[0] == 'l':
            if start[1] < finish[1]:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor
            else:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
        elif start[0] == 'r':
            if start[1] < finish[1]:
                direction = self.__wheels.left
                turn_sensor = self.__left_sensor
            else:
                direction = self.__wheels.right
                turn_sensor = self.__right_sensor  
        self.__calibrated_turn(direction)
        
        print("SAME SIDE")
        count = abs(start[1] - end[1])
        self.__travel_with_counter(turn_sensor.on_line, count)
        # add calibrated turn for rack - issues with rack to rack movement - perhaps split this method into categories
        self.__calibrated_turn(direction)
        
        rack = True if finish[1] >= 3 else False
        self.__enter_location(rack)
