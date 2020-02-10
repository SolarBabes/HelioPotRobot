# #!/usr/bin/env python
 
# import rospy
# from nav_msgs.msg import Odometry

# # Infinite loop printing position and orientation of Turtlebot
# def callback(msg):
#     print(msg.pose.pose)
    
# rospy.init_node('check_odometry')
# odom_sub = rospy.Subscriber('/odom', Odometry, callback)
# rospy.spin()

import re
import numpy as np

global pos_x, pos_y, or_x, or_y, or_z, or_w

def get_pose(txt_file):
    f = open(txt_file, 'r')
    lines = f.readlines()
    pos_found = False
    or_found = False
    for i,l in enumerate(lines):
        if ('position' in l):
            pos_x = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+1])
            pos_y = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+2])
            pos_found = True
        if ('orientation' in l):
            or_x = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+1])
            or_y = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+2])
            or_z = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+3])
            or_w = re.findall("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", lines[i+4])
            or_found = True
        if (pos_found and or_found):
            break
    
    turtlebot_pose = np.asarray(pos_x + pos_y + or_x + or_y + or_z + or_w)
    poses = turtlebot_pose.astype(np.float)
    np.save('turtlebot_pose.npy', poses)
    f.close()

get_pose('pose.txt')