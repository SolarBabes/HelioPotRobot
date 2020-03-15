#!/usr/bin/env python
import rospy
from sensor_msgs.msg import BatteryState

import math

import move_to_base

# Battery analysis
# 100% battery = 12.14V
# Beeping = 11.01V
# 11.49 V - after 35mins of moving forward with teleop = 546m

self.voltage = 0 # Current battery charge
self.distance = 0 # Distance to base station

go_to_base = False

# Maximum translational velocity 0.26 m/s

# dest_x, dest_y is always the same (charging station)
def compute_distance(origin_x, origin_y, dest_x, dest_y):
    self.distance = math.sqrt((dest_x - origin_x)**2 + (dest_y - origin_y)**2)


# Get battery voltage
def battery_callback(msg):
    rospy.loginfo("Listening to battery")
    self.voltage = round(msg.voltage, 2)

# Get position
def odom_callback(msg):
    self.posx = msg.pose.pose.position.x
    self.posy = msg.pose.pose.position.y



# rospy.init_node('battery_charge')
odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback)
battery_sub = rospy.Subscriber('/battery_state', BatteryState, battery_callback)

# Algorithm to decide when to go to charging station 
if self.distance > 10 and self.voltage <= 11.50:
    go_to_base = True
elif self.voltage < 11.30:
    go_to_base = True

rospy.spin()




