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
    print('------------------------')
    curr_range1 = getRange(scan_data, 44)
    curr_range2 = getRange(scan_data, 45)
    curr_range3 = getRange(scan_data, 46)
    if state == 'wall':
        if curr_range1 > 3 and abs(curr_range1 - prev_range) > 1.5 and curr_range2 > 3 and abs(curr_range2 - prev_range) > 1.5 and curr_range3 > 3 and abs(curr_range3 - prev_range) > 1.5:
            state = 'corner'
            pub.publish(state)
    elif state == 'corner':
        if curr_range1 < 1.5 and curr_range2 < 1.5 and curr_range3 <1.5:
            state = 'wall'
            pub.publish(state)
    print(state)
if __name__ == '__main__':
    print('corner finding started')
    rospy.init_node('corner_finder', anonymous = True)
    rospy.Subscriber('scan', LaserScan, process_scan)
    rospy.spin()
