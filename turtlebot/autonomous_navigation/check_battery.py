#!/usr/bin/env python
import rospy
from sensor_msgs.msg import BatteryState
from nav_msgs.msg import Odometry
import math, json

# Battery analysis
# 100% battery = 12.14V
# Beeping = 11.01V
# 11.49 V - after 35mins of moving forward with teleop = 546m
# Maximum translational velocity 0.26 m/s
global pos_x, pos_y, base_x, base_y, voltage, distance, go_to_base

rospy.init_node('check_battery')

# Initialise variables
voltage = 0 # Current battery charge
distance = 0 # Distance to base station
go_to_base = False

# Open json file to get coords of charging station
with open('predefined_locations.txt') as json_file:
    locations = json.load(json_file)
    base_x = locations['charging_station']['x']
    base_y = locations['charging_station']['y']

# dest_x, dest_y is always the same (charging station)
def compute_distance(origin_x, origin_y, dest_x, dest_y):
    distance = math.sqrt((dest_x - origin_x)**2 + (dest_y - origin_y)**2)

# Get battery voltage
def battery_callback(msg):
    rospy.loginfo("Listening to battery")
    voltage = round(msg.voltage, 2)

# Get position
def odom_callback(msg):
    global pos_x, pos_y
    pos_x = msg.pose.pose.position.x
    pos_y = msg.pose.pose.position.y


# if __name__ == "__main__":
while(1):
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.wait_for_message('/odom', Odometry, timeout=1)
    rospy.Subscriber('/battery_state', BatteryState, battery_callback)
    rospy.wait_for_message('/battery_state', BatteryState, timeout=1)

    compute_distance(pos_x, pos_y, base_x, base_y)
    print(voltage)
    print(distance)

    # Algorithm to decide when to go to charging station 
    if distance > 10 and voltage <= 11.50:
        go_to_base = True
    elif voltage < 11.30:
        go_to_base = True
