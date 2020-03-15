# Python scripts

import check_battery
import go_to_goal
from set_locations import windows, base_x, base_y
import set_locations
# import morning_routine
# import weather

import rospy

in_base = False
battery_charged = False # Move to window once the battery has been charged
sunset = False # Turn off the light when the sun has set (plant cycle)



# if __name__ == "__main__":

# if weather.goToBase or check_battery.go_to_base:   
# while(1):
if check_battery.go_to_base:
    go_to_goal.move(base_x, base_y)
    in_base = True
# if in_base == True and battery_charged == True:
        
    

# TODO
# Create subscriber to the battery messages and when it reaches 12.14V move to windows
# If Ben's LED light is green, move to windows (morning_routine)



