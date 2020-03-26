#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Illuminance
from geometry_msgs.msg import Twist
from threading import Thread

global illumin_fr
global illumin_fl
global illumin_br
global illumin_bl

illumin_fr = 0
illumin_fl = 0
illumin_br = 0
illumin_bl = 0

def get_illumin(msg):
    global illumin_fr
    global illumin_fl
    global illumin_br
    global illumin_bl
    if msg.header.frame_id == "/front_right":
        illumin_fr = msg.illuminance
    elif msg.header.frame_id == "/front_left":
        illumin_fl = msg.illuminance
    elif msg.header.frame_id == "/back_right":
        illumin_br = msg.illuminance
    elif msg.header.frame_id == "/back_left":
        illumin_bl = msg.illuminance

def rotate():
    while not is_front_balanced:
        twist = Twist()
        if illumin_fr > illumin_fl:
            twist.angular.z = -0.5

def is_front_balanced():
    toleance = 10
    average = (illumin_fr + illumin_fl) / 2
    if abs(average - illumin_fr) < toleance and abs(average - illumin_fl) < toleance:
        return True
    else:
        return False

def is_all_balanced():
    toleance = 10
    average = (illumin_fr + illumin_fl + illumin_br + illumin_bl) / 4
    if abs(average - illumin_fr) < toleance and abs(average - illumin_fl) < toleance and abs(average - illumin_br) < toleance and abs(average - illumin_bl) < toleance:
        return True
    else:
        return False

def move():
    illumin_sub = rospy.Subscriber('/illuminance', Illuminance, get_illumin)
    while True:
        print "fr: " + str(illumin_fr) + " fl: " + str(illumin_fl) + " br: " + str(illumin_br) + " bl: " + str(illumin_bl)
        

def main():
    
    cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    illumin_sub = rospy.Subscriber('/illuminance', Illuminance, get_illumin)

    rospy.init_node('neo_sunflower_mode', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        twist = Twist()
        while not is_front_balanced():
            if illumin_fr > illumin_fl or illumin_br < illumin_bl:
                print "CW"
                twist.angular.z = -0.3
                twist.linear.x = 0
                break
            elif illumin_fr < illumin_fl or illumin_br > illumin_bl:
                print "CCW"
                twist.angular.z = 0.3
                twist.linear.x = 0
                break

        while not is_all_balanced():
            if not is_front_balanced():
                break
            elif ((illumin_fr + illumin_fl) / 2) > ((illumin_br + illumin_bl) / 2):
                twist.linear.x = 0.1
                twist.angular.z = 0
                break
        cmd_pub.publish(twist)
        print "fr: " + str(illumin_fr) + " fl: " + str(illumin_fl) + " br: " + str(illumin_br) + " bl: " + str(illumin_bl)
        rate.sleep()

#if __name__ == '__main__':
#    try:
        # thread = Thread(target=move)
        # thread.daemon = True
        # thread.start()
        # print "rotating on"
#        main()
#    except rospy.ROSInterruptException:
#        pass