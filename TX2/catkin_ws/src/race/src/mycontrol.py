#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input
from std_msgs.msg import String
import math

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

kp = (14.0*2)
kd = 0.09 * 2
servo_offset = 18.5
prev_error = 0.0 
vel_input = 7
mode = 'gost'

def control(data):
    vel_input = 8
    global kp
    global kd
    global servo_offset
    global prev_error
    global vel_input
    global mode

    msg = drive_param();
    msg.velocity = vel_input
    if mode == 'gost':
        pid_error = data.pid_error
        error = pid_error * kp
        errordot = kd * (pid_error - prev_error)

        angle = error + errordot

        if angle > 100:
            angle = 100
        elif angle < -100:
            angle = -100

        prev_error = pid_error

        print 'pid_error -> {}\nangle -> {}'.format(pid_error, angle)
        msg.angle = angle

    elif mode == 'turnrig':
        print 'turnrig mod, angle 100'
        msg.angle = 100
    elif mode =='turnlef':
        print 'turnlef mod,angle -100'
        msg.angle=-100
    elif mode =='stop':
        print 'stop mod,vel_input = -7,angle=0'
        vel_input=-9
        msg.angle=0
    if math.isnan(msg.angle):
        msg.angle =  0

    msg.velocity = vel_input
    pub.publish(msg)
    print(msg.angle)
def update_mode(_mode):
    global mode
    mode = _mode.data

if __name__ == '__main__':
    print("Listening to error for PID")
    rospy.init_node('pid_controller', anonymous=True)
    rospy.Subscriber('error', pid_input, control)
    rospy.Subscriber('mode', String, update_mode)
    rospy.spin()
