import os,sys, select, termios, tty
import json
import sys
import settings
import time
from settings import wiringport

s0 = wiringport[settings.PINS['servo0']]
s1 = wiringport[settings.PINS['servo1']]

cmd= ["gpio mode {} pwm".format(s0),
     "gpio mode {} pwm".format(s1),
     "gpio pwm-ms",
     "gpio pwmc 1920",
     "gpio pwmr 100",
 ]



speedBindings={
        's':(0.15,0),
        'w':(0.20,0),
        'x':(0.10,0),
        'a':(0.01,0),
        'd':(-0.01,0),
        'r':(0.01,0),
        'l':(-0.01,0),
        't':(0.15,0),

    }

def setspeed(pin, sped):
    if (pin==12):
        str="gpio pwm {} {}".format(s0, sped*100)
        os.system(str)
    elif (pin==13):
        str="gpio pwm {} {}".format(s1, sped*100)
        os.system(str)

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, asettings)
    return key


if __name__=="__main__":
    asettings = termios.tcgetattr(sys.stdin)
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0
    sped =0.15
    angle=0.15

    for i in range(0, len(cmd)):
        print cmd[i]
        os.system(cmd[i])

    try:
        while(1):
            key = getKey()
            print (key)
            if key in speedBindings.keys():
                if (key=='a' or key=='d'):
                    pin =12
                    sped=sped+speedBindings[key][0]
                elif (key=='r' or key=='l'):
                    pin =13
                    angle=angle+speedBindings[key][0]
		elif (key=='w' or key=='x' or key=='s' ):
                    pin =12
                    sped=speedBindings[key][0]
                elif (key=='t'):
                    pin =13
                    angle=speedBindings[key][0]
                else:
		    sped=speedBindings[key][0]
                print(sped)
                if (pin==12):
	            setspeed(pin, sped)
                elif (pin==13):
                    setspeed(pin, angle) 
            else:
                if (key == '\x03'):
                    break
    except Exception as e:
        print(e)

    finally:

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, asettings)
        setspeed(12, 0.15)
        setspeed(13, 0.15)
