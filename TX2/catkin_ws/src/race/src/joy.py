#!/usr/bin/env python
from inputs import get_gamepad
import rospy
from race.msg import drive_param
import curses
#import signal
#TIMEOUT = 0.1 # number of seconds your want for timeout
forward = 0;
left = 0;

# def interrupted(signum, frame):
#     "called when read times out"
#     global forward
#     forward = 0
#     global left
#     left = 0
#     stdscr.addstr(2, 20, "Stop")
#     stdscr.addstr(2, 25, '%.2f' % forward)
#     stdscr.addstr(3, 20, "Stop")
#     stdscr.addstr(3, 25, '%.2f' % left)
# signal.signal(signal.SIGALRM, interrupted)

# def input():
#     try:
#             foo = stdscr.getch()
#             return foo
#     except:
#             # timeout
#             return

stdscr = curses.initscr()
stdscr.keypad(1)
rospy.init_node('keyboard_talker', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

# set alarm
#signal.alarm(TIMEOUT)
#s = input()
# disable the alarm after success
#signal.alarm(0)
#print 'You typed', s

while 1:
        events = get_gamepad()
        for event in events:
#	signal.setitimer(signal.ITIMER_REAL,0.05)
#	key = input()
#	signal.alarm(0)
            if (event.code is "ABS_Y"):
                if (event.state < 120): 
	            forward = (120-event.state)*15/120
	            stdscr.addstr(2, 20, "Up  ")
	            stdscr.addstr(2, 25, '%.2f' % forward)
	            stdscr.addstr(5, 20, "    ")
                elif (event.state > 140):
	            forward = -(event.state-140)*15/120
	            stdscr.addstr(2, 20, "Down")
	            stdscr.addstr(2, 25, '%.2f' % forward)
	            stdscr.addstr(5, 20, "    ")
                else:
                    forward=0
            if (event.code is "ABS_X"):
                if (event.state < 120) :
                    left = -(120-event.state)*90/120
	            stdscr.addstr(3, 20, "left")
		    stdscr.addstr(3, 25, '%.2f' % left)
	            stdscr.addstr(5, 20, "    ")
	        elif (event.state > 140):
	            left = (event.state-140)*90/120
	            stdscr.addstr(3, 20, "rgt ")
	            stdscr.addstr(3, 25, '%.2f' % left)
	            stdscr.addstr(5, 20, "    ")
                else:
                    left =0

	    msg = drive_param()
	    msg.velocity = forward
	    msg.angle = left
	    pub.publish(msg)
