#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
import tf
from rbx1_nav.transform_utils import quat_to_angle, normalize_angle
from math import radians, copysign, sqrt, pow, pi

class Calibrate():
def __init__(self):

    rospy.init_node('calibration', anonymous=False)   
    rospy.on_shutdown(self.shutdown)

    # Publisher to control robot's speed
    self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

    # Robot movement update speed
    rate = 20
    r = rospy.Rate(rate)

    # Forward linear speed (m/s)
    linear_speed = 0.1
    goal_distance = 1.0

    # Rotation speed (rads/s)
    angular_speed = 1.0
    angular_tolerance = radians(2.5)
    # Rotation angle (360 degrees)
    goal_angle = 2*pi


    self.tf_listener = tf.TransformListener()
    rospy.sleep(2)
    self.odom_frame = '/odom'

    # Look if robot uses /base_link or /base_footprint
    try:
        self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
        self.base_frame = '/base_footprint'
    except (tf.Exception, tf.ConnectivityException, tf.LookupException):
        try:
            self.tf_listener.waitForTransform(self.odom_frame, '/base_link', rospy.Time(), rospy.Duration(1.0))
            self.base_frame = '/base_link'
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("Cannot find transform between /odom and /base_link or /base_footprint")
            rospy.signal_shutdown("tf Exception")  


    # Initialize position variable as a Point type
    position = Point()
    # Loop once for each leg of the trip
    for i in range(2):
        # Initialize the movement command
        move_cmd = Twist()
        # Set the movement command to forward motion
        move_cmd.linear.x = linear_speed

        # Get initial position     
        (position, rotation) = self.get_odom()
        x_start = position.x
        y_start = position.y

        # Keep track of the distance traveled
        # distance = 0
        # # Enter the loop to move along a side
        # while distance < goal_distance and not rospy.is_shutdown():
        #     # Publish the Twist message and sleep 1 cycle         
        #     self.cmd_vel.publish(move_cmd)

        #     r.sleep()

        #     # Get the current position
        #     (position, rotation) = self.get_odom()

        #     # Compute the Euclidean distance from the start
        #     distance = sqrt(pow((position.x - x_start), 2) + 
        #                     pow((position.y - y_start), 2))


        ### ROTATION
        # Stop the robot before the rotation
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)

        # Set the movement command to a rotation
        move_cmd.angular.z = angular_speed
        # Track the last angle measured
        last_angle = rotation
        # Track how far we have turned
        turn_angle = 0

        while abs(turn_angle + angular_tolerance) < abs(goal_angle) and not rospy.is_shutdown():
            # Publish the Twist message and sleep 1 cycle         
            self.cmd_vel.publish(move_cmd)
            r.sleep()
            # Get current rotation
            (position, rotation) = self.get_odom()
            delta_angle = normalize_angle(rotation - last_angle)

            turn_angle += delta_angle
            last_angle = rotation

        # Stop the robot before the next leg
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)

    # Stop the robot
    self.cmd_vel.publish(Twist())

def get_odom(self):
    # Get the current transform between the odom and base frames
    try:
        (trans, rot)  = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
    except (tf.Exception, tf.ConnectivityException, tf.LookupException):
        rospy.loginfo("TF Exception")
        return

    return (Point(*trans), quat_to_angle(Quaternion(*rot)))

def shutdown(self):
    # Always stop the robot when shutting down the node.
    rospy.loginfo("Stopping the robot...")
    self.cmd_vel.publish(Twist())
    rospy.sleep(1)



if __name__ == '__main__':
try:
    Calibrate()
except:
    rospy.loginfo("Calibration completed.")