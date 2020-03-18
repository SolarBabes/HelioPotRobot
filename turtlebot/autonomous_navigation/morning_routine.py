#! /usr/bin/env python
import rospy, sys
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Illuminance

import go_to_goal

global base, windows, lux_fr, lux_fl, lux_br, lux_bl
lux_fr, lux_fl, lux_br, lux_bl = 0.0
windows = []

# Open json file
with open('predefined_locations.txt') as json_file:
    global windows, base
    locations = json.load(json_file)
    base = locations['c']
    for n in range(len(locations['w'])):
        windows.append((locations['w'][n]))

def compute_distance(origin_x, origin_y, dest_x, dest_y):
    return math.sqrt((dest_x - origin_x)**2 + (dest_y - origin_y)**2)

def sensor_callback(msg):
    # Determine which light sensor it is
    global lux_fr, lux_fl, lux_br, lux_bl
    if msg.header.frame_id == '/front_right':
        lux_fr = msg.illuminance
    elif msg.header.frame_id == '/front_left':
        lux_fl = msg.illuminance
    elif msg.header.frame_id == '/back_right':
        lux_br = msg.illuminance
    elif msg.header.fram_id == '/back_left':
        lux_bl = msg.illuminance

def sensor_listener():
    rospy.init_node('sensor_readings')
    rospy.Subscriber('/illuminance', Illuminance, sensor_callback)
    # rospy.wait_for_message('/illuminance', Illuminance, timeout=1)

# Move to the window closest to current location
def visit_windows():
    not_visited = windows.copy() # Windows not visited
    # Window with max lux
    max_window = (0.0, 0.0)
    max_lux = 0.0
    while (not(not_visited)):
        # Next window to visit
        next_window = (0.0, 0.0)
        min_dist = sys.float_info.max # Distance to the closest window
        curr_pos = base
        for w in not_visited:
            distance = compute_distance(curr_pos[0], curr_pos[1], w[0], w[1])
            if (distance < min_dist):
                min_dist = distance
                next_window = w
        go_to_goal.move(next_window)
        # Get the sensor readings
        sensor_listener()
        curr_lux = max(lux_fr + lux_fl + lux_br + lux_bl)
        if curr_lux > max_lux:
            max_lux = curr_lux
            max_window = next_window
        not_visited.remove(next_window)
        curr_pos = (next_window[0], next_window[1])

    # Move to window with max lux
    go_to_goal.move(max_window)
