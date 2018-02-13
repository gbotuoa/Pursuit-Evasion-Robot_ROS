# Project : Pursuit-Evasion Robot Using ROS-Kobuki-Turtlebot
The project is done @uoa for experimental robotics

## Overview

The following instructions will guide you to run the project in your local machines.

### Dependencies

We tested our project on the following environment.
* Ubuntu 14.04
* Python 2.7.6
* ROS Indigo
* Numpy
* Matplotlib
* OpenCV-Python 2.4.8

How to configure WiFi:
```
Give the example
```
How to configure Joy:
Include link
```
Give the example
```

### How to run 
#### Turtlebot Gazebo Simulation
##### Evasion
```
roslaunch turtlebot_bringup turtlebot_world.launch
cd catkin_ws
source devel/setup.bash
chmod +x fileName.py
catkin_make
rosrun packageName wander_sim.py 
```

##### Pursuit


#### Kobuku Turtlebot
##### Evasion
```
roslaunch turtlebot_bringup minimal.launch
roslaunch turtlebot_bringup 3dsensor.launch
roslaunch packageName standalone.launch #refer standalone.launch in project files
roslaunch turtlebot_teleop logitech.launch 
```

If joystick appears on js1 other than js0:
```
ls -l /dev/input/js1
roslaunch packageName joy.launch #refer joy.launch in project files
```
```
cd catkin_ws
source devel/setup.bash
chmod +x fileName.py
catkin_make
rosrun packageName wander.py cmd_vel:=cmd_vel/velocityramp #uses standalone.launch
```

##### Pursuit

Document Wifi commands

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```


## Discussion

Discuss how changing p changed the output


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Nazmus**
* **Vivian** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.



## Acknowledgement 

* [Programming Robots with ROS](https://github.com/osrf/rosbook/blob/master/LICENSE)
