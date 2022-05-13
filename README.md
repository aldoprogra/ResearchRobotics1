Third Assignment
================================

Introduction
----------------------

I was asked to develop a program in which the user control the robot in a 3D simulation enviroment in three different ways:
1) autonomously reach a x,y coordinate inserted by the user
2) drive the robot with the keyboard
3) drive the robot with keyboard but avoiding collisions

How to install
----------------------

Install in your workspace and build:

```
$ catkin_make
```

How to run
-----------------------------
Open 2 terminals and write in the command lines :

```bash
$ roslaunch final_assignment master.launch

$ rosrun final_assignment master.py
```

## Pseudocode
----------------------

1) Autonomous drive

After asking coordinates x,y, they will published to move_base/goal

```python
    ## provide and publish move_base with (x,y) values
    msg.target_pose.pose.position.x = x
    msg.goal.target_pose.pose.position.y = y
    publisher_movebase.publish(msg) 
```
The status is retrived by move_base/status and the user can cancel (publishing in move_base/cancel) the goal and insert a new one:

```python
