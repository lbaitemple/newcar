#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

pub = rospy.Publisher('mode', String, queue_size=10)
prev_range = -1
state = 'wall'

def getRange(data, theta):
    """ Find the index of the arary that corresponds to angle theta.
    Return the lidar scan value at that index
    Do some error checking for NaN and absurd values
    data: the LidarScan data
    theta: the angle to return the distance for
    """
    carAngle = theta+269
    index = carAngle
    return data.ranges[index]
def process_scan(scan_data):
    global state

    curr_range = getRange(scan_data, 45)
    base_range = getRange(scan_data,1)*1.5
    print('curr_range')
    print(curr_range)   
    if state == 'wall':
        if curr_range > base_range:
            state = 'corner'
            pub.publish(state)
    elif state == 'corner':
        if curr_range < base_range:
            state = 'wall'
            pub.publish(state)
    print(state)

if __name__ == '__main__':
    print('corner finding started')
    rospy.init_node('corner_finder', anonymous = True)
    rospy.Subscriber('scan', LaserScan, process_scan)
    rospy.spin()
