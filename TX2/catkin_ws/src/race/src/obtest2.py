#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

pub = rospy.Publisher('mode', String, queue_size=10)
prev_range = -1
state ='gost'
modbase ='wall'


def getRange(data, theta):
    """ Find the index of the arary that corresponds to angle theta.
    Return the lidar scan value at that index
    Do some error checking for NaN and absurd values
    data: the LidarScan data
    theta: the angle to return the distance for
    """
    carAngle = theta+269
    if carAngle > 359:
        carAngle = carAngle-359
    return data.ranges[carAngle]
def process_scan(scan_data):
    global state
    global modbase
    global modob
    print('------------------------')
    #modbase find right wall and right corner
    curr45 = [0,0,0]
    for num in range(0,2):
        curr45[num] = getRange(scan_data, 44+num)
    if modbase == 'wall':
       flag =1
       for num in range(0,2):
           if curr45[num] < 1.8 or abs(curr45[num] - prev_range) < 1.5:
               flag =0
       if flag:
            modbase = 'rigcor'
    elif modbase == 'rigcor':
        flag =1
        for num in range(0,2):
            if curr45[num] > 1.5:
                flag =0
        if flag :
            modbase = 'wall'
    #modlob find left corner or face wall
    flag=1
    curr90 = [0,0,0]
    for num in range(0,2):
        curr90[num] = getRange(scan_data, 89+num)
        if curr90[num] < 1.5:
            flag =0
    if flag:
        modob='safe'
    elif flag==0:
        curr135 =[0,0,0]
        flag2=1
        for num in range(0,2):
            curr135[num]=getRange(scan_data,134+num)
            if math.isinf(curr135[num])==False and math.isinf(curr45[num])==False:
                if curr45[num]-curr135[num]>0.10 or curr135[num]<1.0:
                    flag2=0
        if flag2:
            modob='lefcor'
        elif flag2==0:
            modob='stop'
    #find state
    if modbase=='rigcor':
        state ='turnrig'
        pub.publish(state)
    elif modob=='stop':
        state ='stop'
        pub.publish(state)
    elif modob=='lefcor':
        state ='turnlef'
        pub.publish(state)
    elif modob=='safe':
        state ='gost'
        pub.publish(state)
    print(state)
if __name__ == '__main__':
    print('corner finding started')
    rospy.init_node('corner_finder', anonymous = True)
    rospy.Subscriber('scan', LaserScan, process_scan)
    rospy.spin()
