#!/usr/bin/env python
import check_battery, weather, go_to_goal, morning_routine # Python scripts
import json, rospy
from sensor_msgs.msg import BatteryState

in_base = False
battery_charged = False

global base, windows, voltage
voltage = 0.0
windows = []

# Open json file
with open('predefined_locations.txt') as json_file:
    locations = json.load(json_file)
    base = locations['c']
    for n in range(len(locations['w'])):
        windows.append((locations['w'][n]))

# Get battery voltage
def battery_callback(msg):
    global voltage
    rospy.loginfo("Listening to battery")
    voltage = round(msg.voltage, 2)


if __name__ == "__main__":
    # Check battery
    rospy.Subscriber('/battery_state', BatteryState, battery_callback)
    rospy.wait_for_message('/battery_state', BatteryState, timeout=1)
    if voltage == 12.14:
        battery_charged = True

    # Move to charging station or visit windows
    if check_battery.go_to_base or weather.go_to_base:
        go_to_goal.move(base[0], base[1])
        in_base = True
    elif in_base and (not(weather.goToBase) or battery_charged):
        morning_routine.visit_windows()
        # Trigger sunflower mode
        in_base = False

    # TODO
    # If LED light is green, move to windows (morning_routine)

# For testing
# print('charging station')
# print(base)
# print('windows')
# print(windows)
# go_to_goal.move(base[0], base[1])

