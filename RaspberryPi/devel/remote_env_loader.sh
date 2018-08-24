#!/bin/bash

export ROS_IP=10.109.140.234
export ROS_MASTER_URI=http://10.109.28.73:11311
export ROS_IP=10.109.140.234

source /home/pi/catkin_ws/devel/setup.bash

exec "$@"
