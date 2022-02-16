Third Assignment
================================

Introduction
----------------------

I was asked to develop a program in which the user control the robot in a 3D simulation enviroment in three different ways:
- 1) autonomously reach a x,y coordinate inserted by the user
- 2) drive the robot with the keyboard
- 3) drive the robot with keyboard but avoiding collisions

How to install
----------------------

Install in your workspace and build:

```
$ cd catkin_make
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

```
    ## provide and publish move_base with (x,y) values
    msg.target_pose.pose.position.x = x
    msg.goal.target_pose.pose.position.y = y
    publisher_movebase.publish(msg) 
```
The status is retrived by move_base/status and the user can cancel (publishing in move_base/cancel) the goal and insert a new one:

```
    print("\nDo you want a new goal?[y] or [n]\n")
                         
    button = input()
     
     if(button == 'y'):
     	print("Okay\n")
      	break
     if(button == 'n'):
        publisher_cancel = rospy.Publisher("/move_base/cancel", GoalID, queue_size = 1)
        cancel = GoalID()
        publisher_cancel.publish(cancel)
        return 1
```

2) Manual control 

The user digit the comand and the correct velocity is published in cmd/vel
```
    if (arrow == 'w'):
    	[my_vel.linear.x, my_vel.angular.z] =[1 , 0] 
    elif (arrow == 'a'):
     	[my_vel.linear.x, my_vel.angular.z] =[0 , 2]
    elif (arrow == 'd'):
        [my_vel.linear.x, my_vel.angular.z] =[0, -2]
    elif (arrow == 's'):
        [my_vel.linear.x, my_vel.angular.z] =[-1 , 0]
    elif (arrow == 'q'):
        [my_vel.linear.x, my_vel.angular.z] =[0 , 0]
        vel_pub.publish(my_vel)
        break
    else:
        print("Wrong button")
    	vel_pub.publish(my_vel)
```

3) Assisted-manual drive

The program compute the minimum distance in several direction 

```
        min_fright = min(min(msg.ranges[144:287]), 5)
        min_front =  min(min(msg.ranges[288:431]), 5)
        min_fleft =  min(min(msg.ranges[432:575]), 5)
```

and if it is less then a threshold the velocity is published not by the user but by take_action() trying to avoid obstacles
```
    if min_front > 1 and min_fleft > 1 and min_fright > 1:
        state_description = 'case 1 - nothing'
        linear_x = 0.6
        angular_z = 0
    elif min_front < 1 and min_fleft > 1 and min_fright > 1:
        state_description = 'case 2 - front'
        linear_x = -2
        angular_z = 0
    elif min_front > 1 and min_fleft > 1 and min_fright < 1:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = 1
```
