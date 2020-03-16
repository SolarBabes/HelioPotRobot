import re
import numpy as np
#import rospy
#import nav_msgs.msg import Odometry
global pos_x, pos_y, pos_z, or_x, or_y, or_z, or_w

f = open('initial_position.txt', 'r')
flag = 1

for line in f.readlines():
	if (flag == 1):
		line = line.strip()
		if (line[0] == 'x'):
			pos_x = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
		if (line[0] == 'y'):
			pos_y = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
		if (line[0] == 'z'):
			pos_z = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
			flag = 2
	elif (flag == 2):
		line = line.strip()
		if (line[0] == 'x'):
			or_x = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
		if (line[0] == 'y'):
			or_y = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
		if (line[0] == 'z'):
			or_z = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
		if (line[0] == 'w'):
			or_w = re.findall("-?\d+\.?\d+(?:[eE][-+]?\d+)?", line)
			break
	
turtlebot_pose = np.asarray(pos_x + pos_y + pos_z + or_x + or_y + or_z + or_w)
poses = turtlebot_pose.astype(np.float)
print(poses)
np.save('init_config.npy', poses)
f.close()


