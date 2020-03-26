#!/usr/bin/env python
import socket, sys, os, json, time
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Odometry
from threading import Thread

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind(('', 9800))
#recv_socket.setblocking(0)
global_command = 'STOP'
global_position = 0

locations = {}
locations['c'] = []
locations['w'] = []

folder = os.path.dirname(os.path.abspath(__file__))
text_file = os.path.join(folder, 'predefined_locations.txt')
text_file = open('predefined_locations.txt', 'w')

def getKey():
    while True:
        command, address = recv_socket.recvfrom(1024)
        global_command = command.decode('UTF-8')
        print global_command

def move(twist, linear_x, angular_z):
    twist.linear.x = linear_x
    twist.angular.z = angular_z

def get_pose(msg):
    global_position = msg.pose.pose

def cyka():
    while True:
        print "yes boi"
        time.sleep(1)

def remoCon():
    cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    odom_sub = rospy.Subscriber('/odom', Odometry, get_pose)
    rospy.init_node('remocon', anonymous=True)
    rate = rospy.Rate(10)
    twist = Twist()
    location_finish_flag = False
    while not rospy.is_shutdown():
        local_command = global_command
        print local_command
        if local_command == 'FORWARD':
            move(twist, 0.2, 0)
        elif local_command == 'BACKWARD':
            move(twist, -0.2, 0)
        elif local_command == 'ACW':
            move(twist, 0, 0.7)
        elif local_command == 'CW':
            move(twist, 0, -0.7)
        elif local_command == 'STOP':
            move(twist, 0, 0)
        elif local_command == 'LOCATION_STATION' and not location_finish_flag:
            (local_x, local_y) = (global_position.x, global_position.y)
            locations['c'].append((local_x, local_y))
        elif local_command == 'LOCATION_WINDOW' and not location_finish_flag:
            (local_x, local_y) = (global_position.x, global_position.y)
            locations['w'][0] = (local_x, local_y)
        elif local_command == 'FINISH' and not location_finish_flag:
            location_finish_flag = True
            json.dump(locations, text_file)
            text_file.close()
        else:
            move(twist, 0, 0)
        cmd_pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        thread = Thread(target=getKey)
        thread.start()
        print "receiving thread on"
        #remoCon()
        cyka()
    except rospy.ROSInterruptException:
        pass
