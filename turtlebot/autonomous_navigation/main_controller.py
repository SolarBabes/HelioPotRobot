# Python scripts
import check_battery
import go_to_goal
import json
# import morning_routine
import weather

import rospy

in_base = False
battery_charged = False # Move to window once the battery has been charged
sunset = False # Turn off the light when the sun has set (plant cycle)

global base, windows
windows = []

# Open json file
with open('predefined_locations.txt') as json_file:
    locations = json.load(json_file)
    base = locations['c']
    for n in range(1, len(locations['w'])+1):
        windows.append((locations['w'][str(n)]))


if __name__ == "__main__":
    if check_battery.go_to_base or weather.goToBase:
        go_to_goal.move(base[0], base[1])
        in_base = True
    elif in_base and not(weather.goToBase): # or battery_charged
        morning_routine
    # TODO
    # Create subscriber to the battery messages and when it reaches 12.14V move to windows
    # If LED light is green, move to windows (morning_routine)
    
# For testing
print('charging station')
print(base)
print('windows')
print(windows)
go_to_goal.move(base[0], base[1])

