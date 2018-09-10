#!/usr/bin/env python

import sys, tty, termios, time, rospy
import wiringpi as GPIO
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Empty
from std_msgs.msg import Int32
from race.msg import drive_param
import pigpio

str_msg = Int32()
flagStop = False

pwm_center = 15
pwm_lowerlimit = 10
pwm_upperlimit = 20
mport=1
sport=23


def setMotor(pin, duty):
   global pi
   duty=duty*10000
   p=pi.hardware_PWM(pin, 100, duty) 
   

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def messageDrive(pwm):
    global mport
    global sport
    global flagStop

    if(flagStop is False):
	v = pwm.velocity * 5 + pwm_center
#        rospy.loginfo("speed is %d", v)
        if(v < pwm_lowerlimit):
	    setMotor(mport, pwm_lowerlimit)
	elif(v > pwm_upperlimit):
	    setMotor(mport, pwm_upperlimit)
	else:
	    setMotor(mport, v)

	a = pwm.angle + pwm_center
        rospy.loginfo("angle is %d", a)
	if(a < pwm_lowerlimit):
	    setMotor(sport, pwm_lowerlimit)
	elif(a > pwm_upperlimit):
	    setMotor(sport, pwm_upperlimit)
	else:
	    setMotor(sport, a)
    else:
        setMotor(mport, pwm_center)
	setMotor(sport, pwm_center)

def messageEmergencyStop(flag):
        global flagStop
	flagStop = flag.data
	if(flagStop is True):
		setMotor(mport, pwm_center)
		setMotor(sport, pwm_center)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("drive_parameters", drive_param, messageDrive)
    rospy.Subscriber("eStop", Bool, messageEmergencyStop)
    rospy.spin()

if __name__ == '__main__':
    global pi
    pi = pigpio.pi()

    if not pi.connected:
        exit()


    sport=rospy.get_param('~steer_port', 13)
    mport=rospy.get_param('~motor_port', 18)

    setMotor(mport, pwm_center)
    setMotor(sport, pwm_center)


    print "ROS stuff initializing"
    listener()
    
    setMotor(mport, pwm_center)
    setMotor(sport, pwm_center)

    pi.stop()
