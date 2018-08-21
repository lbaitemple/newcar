#!/usr/bin/env python

import serial
import time
import sys
import termios
import tty
from tf.transformations import quaternion_from_euler
import rospy
from sensor_msgs.msg import Imu
import math

degrees2rad = math.pi/180.0


def talker():
    port=rospy.get_param('~serial_port', '/dev/ttyACM0')
    brate=rospy.get_param('~baudrate', 57600)
    timeout=rospy.get_param('~timeout', 1)
    try:
        ser = serial.Serial(port=port, baudrate=brate, timeout=timeout)
    except serial.serialutil.SerialException:
        sys.exit(0)

    pub = rospy.Publisher('imu', Imu, queue_size=10)
    rospy.init_node('imu_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    frame_id = rospy.get_param('~frame_id', 'imu_link')
    imuMsg = Imu()

    acc_fact = 1000.0
    mag_fact = 16.0
    gyr_fact = 900.0
    seq = 0
    imu_yaw_calibration = 0.0
    accel_factor = 9.806 / 256.0 
    imuMsg.orientation_covariance = [
    0.0025 , 0 , 0,
    0, 0.0025, 0,
    0, 0, 0.0025
    ]

    imuMsg.angular_velocity_covariance = [
    0.02, 0 , 0,
    0 , 0.02, 0,
    0 , 0 , 0.02
    ]

    
    imuMsg.linear_acceleration_covariance = [
    0.04 , 0 , 0,
    0 , 0.04, 0,
    0 , 0 , 0.04
    ]

    while not rospy.is_shutdown():
       try:
           buf = ser.readline()
           words=buf.rstrip().split(",")

           if (len(words) ==14):
           #in AHRS firmware z axis points down, in ROS z axis points up (see REP 103)

               # Publish message
               # AHRS firmware accelerations are negated
               # This means y and z are correct for ROS, but x needs reversing
               imuMsg.linear_acceleration.x = -float(words[1]) 
               imuMsg.linear_acceleration.y = float(words[2]) 
               imuMsg.linear_acceleration.z = float(words[3]) 

               imuMsg.angular_velocity.x = float(words[4])
               #in AHRS firmware y axis points right, in ROS y axis points left (see REP 103)
               imuMsg.angular_velocity.y = -float(words[5])
               #in AHRS firmware z axis points down, in ROS z axis points up (see REP 103) 
               imuMsg.angular_velocity.z = -float(words[6])

               imuMsg.orientation.w =float(words[10])
               imuMsg.orientation.x = float(words[11])
               imuMsg.orientation.y = float(words[12])
               imuMsg.orientation.z = float(words[13])
               imuMsg.header.stamp= rospy.Time.now()
               imuMsg.header.frame_id = 'base_imu_link'
               imuMsg.header.seq = seq
               seq = seq + 1
               pub.publish(imuMsg)

       except (KeyboardInterrupt, SystemExit):
           ser.close()
           raise

    ser.close()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
