#! /usr/bin/env python
## @package final_assignment
# @file master.py
# @brief Using ROS framework, this script allows the user to switch to different modalities:
#autonomously reach a x,y coordinate, drive the robot with the keyboard and
#drive the robot with keyboard but avoiding collisions. In the README file is explained how run the simulation.
# @author Sinatra Gesualdo
# @version 1
# @date 16/05/2022
#
# @details
#
# Subscribes to: <BR>
# /odom
# /move_base/status
# /scan
# Publishes to: <BR>
# /cmd_vel
# /move_base/cancel
#-rospy
# - pure python module for interfacing with ROS workspace
#

import rospy
#-os
# -access to OS functionalities like read command lines. It is used for clear the shell
import os

from move_base_msgs.msg import MoveBaseActionFeedback
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalID
from actionlib_msgs.msg import GoalStatusArray
from nav_msgs.msg import Odometry
#-termios
# - access to some terinal functionalities. It is used for read command line without pressing enter
import termios
import sys, tty
from sensor_msgs.msg import LaserScan
import jupyros
#-math
# - provide important functions for calculating distance and orientation of the robot.
import math


def intro():
	##
	# @brief Allow to print the main menù, doesn't have argument and returned variable neither.
	# 

        os.system("clear")
        print("PRESS 1,2,3 or 4:\n")
        print("[1]- Planning motion")
        print("[2]- Manual motion")
        print("[3]- Assisted-manual motion")
        print("[4]- Exit\n")
        

def todist(x,y,x_pos,y_pos):
	##
	# @brief Use pitagora formula for calculating the distance between the robot and goal position.
	# @param x position of the robot
	# @param y position of the robot
	# @param x_goal x coordinate of the goal
	# @param y_goal y coordinate of the goal
	# @return a float number, the distance

	return ((x-x_pos)**2-(y-y_pos)**2)**0.5
	
def move_base():
	##
	# @brief Represent the first motion option. In this function is asked coordinates to the user
	#the goal is published in /move_base/goal topic and the feedback is displayed to the user. Both at the end and during the motion towards the goal,
	#the user can cancel the current goal and choose another one.
        pub_movebase = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size = 50)
        position = rospy.wait_for_message("/odom",Odometry)
        x_pos = position.twist.twist.linear.x 
        y_pos = position.twist.twist.linear.y 
        
        rate = rospy.Rate(10)
        move = MoveBaseActionGoal()
        move.goal.target_pose.header.frame_id = "map"
        move.goal.target_pose.pose.orientation.w = 1
        

        while(True):
          
                os.system("clear")
                print("----PLANNING CHOICE-----\n")
                x = float(input("INSERT X COORDINATE: \n"))
                y = float(input("INSERT Y COORDINATE: \n"))
                
                move.goal.target_pose.pose.position.x = x
                move.goal.target_pose.pose.position.y = y
                dist = todist(x,y,x_pos,y_pos)
                pub_movebase.publish(move)
                rate.sleep()
                
                goal_info = None
                while(goal_info is None):
                        goal_info = rospy.wait_for_message("move_base/status",GoalStatusArray)
                        rate.sleep()
                           
                        status = int(goal_info.status_list[-1].status)
                        
                if(status == 1):
                        print("Goal accepted")
                        
                        
                        
            
                while(True):
        
                        goal_info = rospy.wait_for_message("move_base/status",GoalStatusArray)
                        _id = goal_info.status_list[0].goal_id.id
                        status = int(goal_info.status_list[-1].status)


                        if(status == 2):   
                               print("Goal not recheable\n")
                                                    
                                                
                        if(status == 3):
                               print("Goal reached")
                               state_answer()
                        
                        if(status == 4):
                                print("Goal aborted")
                        
                        rate.sleep()
                        os.system("clear")
                        print(dist)
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
def manual_show():
    	##
    	# @brief Print to the user which command press for start controlling the robot with the keyboard
        print("--- MANUAL DRIVE----\n")
        print("Press:\n[w]: Forward\n[a]: Left\n[d]:Right\n[s]: Back\n[q]: Quit\n")
        
                                
def getch():
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()



def manual():
	##
	# @brief Is the second option for the robot motion in the simulation.
	# it is possible in this modality to control the robot with the keyboard.
	# At every command is associated a different value of speed that will published to /cmd_vel 
        os.system("clear")
        manual_show()
        
        vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size= 50)
        my_vel = Twist()
        my_vel.linear.y = 0
        my_vel.linear.z = 0
        my_vel.angular.x = 0
        my_vel.angular.y= 0
        
        while(True):
        
            
                arrow = getch()
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
        return 1


def clbk_laser(msg):
	##
	#@brief Is the callback whenever new data in /scan topic is ready. The long list ranges of the 
	#topic is processed for getting closest obstacle distance in front, right and left direction of the robot.
	#@param msg the message coming from the sensor, published in the /scan topic
	#@return min_fright float minimum distance in the right direction
	#@return min_front float minimum distance in the front direction
	#@return min_fleft float minimum distance in the left direction
        min_fright = min(min(msg.ranges[144:287]), 5)
        min_front =  min(min(msg.ranges[288:431]), 5)
        min_fleft =  min(min(msg.ranges[432:575]), 5)
        
        
        return min_fright, min_front, min_fleft


def take_action(min_fright,min_front, min_fleft):
    ##
    #@brief Takes into account the closest obstacle distance for moving the robot in the opposite direction
    #the function is used in the assisted motion drive for force the robot to not crash
    #@param min_fright float minimum distance in the right direction
    #@parmam min_front float minimum distance in the front direction
    #@param min_fright float minimum distance in the left direction
    
    msg = Twist()
    msg.linear.y = 0
    msg.linear.z = 0
    msg.angular.x = 0
    msg.angular.y= 0
    my_vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 50)

    state_description = ''

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
    elif min_front > 1 and min_fleft < 1 and min_fright > 1:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = -1
    elif min_front < 1 and min_fleft > 1 and min_fright < 1:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = 1
    elif min_front < 1 and min_fleft < 1 and min_fright > 1:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = -1
    elif min_front < 1 and min_fleft < 1 and min_fright < 1:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = 2
    elif min_front > 1 and min_fleft < 1 and min_fright < 1:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0.3
        angular_z = 0

    #rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    my_vel.publish(msg)
        

def assisted_manual_show():
	##
	#@brief Display the command to the user for controlling the robot, and how to exit the modality and come back to the menu
        print("--- MANUAL DRIVE----\n")
        print("Press:\n[w]: Forward\n[a]: Left\n[d]:Right\n[s]: Back\n[q]: Quit\n")
        
def assisted_manual():
	##
	#@brief Is the third modality. After updating the distance between robot and closest distance, if the robot is too close take_action
	#take control otherwise the user uses can control the robot as he wishes.

	
        os.system("clear")
        assisted_manual_show()
        vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size= 50)

        

        my_vel = Twist()
        my_vel.linear.y = 0
        my_vel.linear.z = 0
        my_vel.angular.x = 0
        my_vel.angular.y= 0
        

        
        while True:
        
                laser = rospy.wait_for_message("/scan", LaserScan)     
                vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size= 50)
                
                [min_fright, min_front, min_fleft] = clbk_laser(laser)

                
                
                if min_front < 1 or min_fleft < 1 or min_fright < 1:
                        take_action(min_fright, min_front, min_fleft)
                        
                else:    

                        arrow = getch()

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
                        
        return 1
           
def main():
	##
	#@brief In the main the cde handles the modalities:
	#\li \c move_base -> planning 
	#\li \c manual -> manual control
	#\li \c assisted_manual -> assisted obstacle avoidance
	

        exit = True
        rospy.init_node('controller')
  
        
        while (not rospy.is_shutdown() ):
                
                intro()
                command = int(input())
                
                
                
                while (True):
 
                        if(command == 1):
                                move_base()
                                break
                        
                        if(command == 2):
                                manual()
                                break
                        
                        if(command == 3):
                                assisted_manual()
                                break
                        
                        if(command == 4):

                                return 1
                   
                        
                        else:
                                print("Command incorrect")
                                break
                        
                     
                        

if(__name__ == '__main__'):
    main() 
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                                
                                
                                
   
        
        
        



