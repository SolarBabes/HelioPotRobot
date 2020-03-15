import sys, select, os, socket, time
from nav_msgs.msg import Odometry

global base_x, base_y, pose
windows = []
# pose

# Socket for messages from the app
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get position
def odom_callback(msg):
    # base_x = msg.pose.pose.position.x
    # base_y = msg.pose.pose.position.y
    pose = msg.pose.pose

def odom_listener():
    # rospy.init_node('windows')
    odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback)

# Receive message from button on the app
def get_message():
    msg = soc.recv(1024)
    msg = msg.decode('UTF-8')



# When button on the app is pressed, get position of turtlebot and mark as window
def add_window():
    odom_listener()
    windows.append(tuple(self.posx, self.posy))


finished = False
while(1):
    msg = (str(get_message())).rstrip()
    if (msg == "charging_station"):
        odom_listener()
        base_x = pose.position.x
        base_y = pose.position.y
        print("charging station coords")
        print(base_x)
        print(base_y)
    elif (msg == "window_location"):
        odom_listener()
        windows.append(tuple(pose.position.x, pose.position.y))


