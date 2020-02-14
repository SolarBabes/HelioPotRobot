#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def rotate():
    # Start new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Receiving the user's input
    print("Rotate your robot")
    speed = input("Input your speed (degrees/sec):")
    angle = input("Type your distance (degrees):")
    clockwise = input("Clockwise?: ") #True or false

    # Converting from angles to radians
    # speed = 0.1
    # angle = 2.5
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    # Not using linear components because rotating in-place
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0


    # Checking if our movement is CW or CCW
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    # Setting the current time to compute angular distance
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)


    # Robot in the specified angle, so stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    rospy.spin()

if __name__ == '__main__':
    try:
        # Testing our function
        rotate()
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")