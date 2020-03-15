#! /usr/bin/env python
import rospy
from nav_msgs.msg import Odometry

import go_to_goal
from set_locations import windows

global posx, posy, max_light_window


# sort window points according to distance

# Move to windows (sunrise from weather)
def visit_windows():
    for w in windows: # Gather the data from the light sensors
        go_to_goal.move(w)
