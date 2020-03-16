#! /usr/bin/env python
import rospy, sys
from nav_msgs.msg import Odometry

import go_to_goal

global base_x, base_y, windows
windows = []

# Open json file
with open('predefined_locations.txt') as json_file:
    global windows, base_x, base_y
    locations = json.load(json_file)
    base_x = locations['charging_station']['x']
    base_y = locations['charging_station']['y']
    for n in range(1, len(locations['windows'])+1):
        windows.append((locations['windows'][str(n)]['x'], locations['windows'][str(n)]['y']))


def compute_distance(origin_x, origin_y, dest_x, dest_y):
    return math.sqrt((dest_x - origin_x)**2 + (dest_y - origin_y)**2)


# Move to the window closest to the charging station
# Move to the next window closest to current window location

not_visited = windows.copy() # Windows not visited
next_window_x = 0.0
next_window_y = 0.0
min_dist = sys.float_info.max # Distance to the closest window
pos_x = base_x
pos_y = base_y
# Move to windows (sunrise)
def visit_windows():
    while (not(not_visited)):
        for w in not_visited:
            # TODO Gather the data from the light sensors
            distance = compute_distance(pos_x, pos_y)
            if (distance < min_dist):
                min_dist = distance
                next_window_x = w[0]
                next_window_y = w[1]
        go_to_goal.move(w)
        not_visited.remove(w)
        pos_x = w[0]
        pos_y = w[1]
