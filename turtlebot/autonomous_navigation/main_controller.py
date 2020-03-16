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

global base_x, base_y, windows
windows = []

# Open json file
with open('predefined_locations.txt') as json_file:
    locations = json.load(json_file)
    base_x = locations['charging_station']['x']
    base_y = locations['charging_station']['y']
    for n in range(1, len(locations['windows'])+1):
        windows.append((locations['windows'][str(n)]['x'], locations['windows'][str(n)]['y']))

print('charging station')
print(base_x)
print(base_y)
print('windows')
print(windows)

go_to_goal.move(base_x, base_y)

# if __name__ == "__main__":
while(1):
    if check_battery.go_to_base:
        go_to_goal.move(base_x, base_y)
        in_base = True
    
        
# Weather
# if weather.goToBase:
#     go_to_goal.move(base_x, base_y)
# elif not(weather.goToBase):
#     morning_routine



# TODO
# Create subscriber to the battery messages and when it reaches 12.14V move to windows
# If LED light is green, move to windows (morning_routine)
# elif in_base == True and battery_charged == True:

