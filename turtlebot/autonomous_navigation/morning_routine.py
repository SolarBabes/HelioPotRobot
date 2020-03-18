#! /usr/bin/env python
import rospy, sys
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Illuminance

import go_to_goal

global base, windows
windows = []
max_illuminance = 0.0
max_window = (0.0, 0.0)

# Open json file
with open('predefined_locations.txt') as json_file:
    global windows, base
    locations = json.load(json_file)
    base = locations['c']
    for n in range(1, len(locations['w'])+1):
        windows.append((locations['w'][str(n)]))

def compute_distance(origin_x, origin_y, dest_x, dest_y):
    return math.sqrt((dest_x - origin_x)**2 + (dest_y - origin_y)**2)


# TODO change depending on the path of each sensor
def sensor_callback(msg):
    # Determine which light sensor it is
    msg.header.frame_id # type string
    msg.illuminance # type float

def sensor_listener():
    rospy.init_node('sensor_readings')
    rospy.Subscriber('/sensor_msgs', Illuminance, sensor_callback)
    rospy.wait_for_message('/sensor_msgs', Illuminance, timeout=1)


# Move to the window closest to current location
# Move to windows (sunrise)
def visit_windows():
    not_visited = windows.copy() # Windows not visited
    next_window_x = 0.0
    next_window_y = 0.0
    min_dist = sys.float_info.max # Distance to the closest window
    curr_pos = base
    avg_lux = 0.0 # Take average of all four light sensors to get the lux at each window
    while (not(not_visited)):
        for w in not_visited:
            # TODO Gather the data from the light sensors
            distance = compute_distance(curr_pos[0], curr_pos[1], w[0], w[1])
            if (distance < min_dist):
                min_dist = distance
                next_window_x = w[0]
                next_window_y = w[1]
        go_to_goal.move(w)
        # TODO
        # Get the sensor readings
        sensor_listener()
    

        not_visited.remove(w)
        curr_pos = (w[0], w[1])
    # Move to window with max lux
    go_to_goal.move(max_window)
