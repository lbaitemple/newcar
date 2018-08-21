# newcar
There are two single board computers; Jetson TX2 and Raspberry Pi.
```
ssh nvidia@tx2_ip
cd catkin_ws
catkin_make
source develop/setup.bash
roslaunch race auto.launch
rosrun race kill.py
```



```
ssh pi@raspberry_ip
cd catkin_ws
catkin_make
source develop/setup.bash
roslaunch rpimotor f1.launch
```

