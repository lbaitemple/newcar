#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

desired_trajectory = 0.5
vel = 10

pub = rospy.Publisher('error', pid_input, queue_size=10)

def getRange(data, theta):
    """ Find the index of the arary that corresponds to angle theta.
    Return the lidar scan value at that index
    Do some error checking for NaN and absurd values
	data: the LidarScan data
	theta: the angle to return the distance for
	"""
    carAngle = theta+180
    index = carAngle
    return data.ranges[index]
    

def callback(data):
    theta = 50;
    a = getRange(data, theta)
    b = getRange(data, 0)
    swing = math.radians(theta)
    print "a -> {}\nb -> {}".format(a, b)
    print "Swing -> {}".format(swing)

    ABangle = math.atan2( a * math.cos(swing) - b , a * math.sin(swing))
    AB = b * math.cos(ABangle)
    print "AB -> {}".format(AB)

    AC = 1
    CD = AB + AC * math.sin(ABangle)
    error = CD - desired_trajectory
    print "Error -> {}".format(error)

    msg = pid_input()
    msg.pid_error = error
    msg.pid_vel = vel
    pub.publish(msg)
    

if __name__ == '__main__':
    print("Laser node started")
    rospy.init_node('dist_finder',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()
