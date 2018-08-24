# newcar
There are two single board computers; Jetson TX2 and Raspberry Pi.

Self-driving and lidar codes are on the Jetson TX2
motor driving and imu codes are on the raspberry Pi
```
ssh nvidia@tx2_ip
cd ~/catkin_ws
catkin_make
source develop/setup.bash
roslaunch race auto.launch
rosrun race kill.py
```
On the raspberry Pi
```
ssh pi@raspberry_ip
cd ~/catkin_ws
catkin_make
source develop/setup.bash
roslaunch rpimotor f1.launch
```

We will need to create a remotelaunch procedure on TX2 (no need to login raspberry pi)
https://github.com/pandora-auth-ros-pkg/pandora_docs/wiki/Remote-Machines-Running-ROS-nodes 
1) remove known_hosts and create ssh credential
```
rm ~/.ssh/known_host
ssh-keygen -t rsa 
ssh-copy-id -i <ssh-key> pi@raspberrypi-ip-address
```

2) reconnect to raspberry pi
```
ssh pi@raspberrypi-ip-address -oHostKeyAlgorithms='ssh-rsa'
source develop/setup.bash
roslaunch race rauto.launch
```
