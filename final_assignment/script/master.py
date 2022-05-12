#! /usr/bin/env python

import rospy
import os
from move_base_msgs.msg import MoveBaseActionFeedback
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalID
from actionlib_msgs.msg import GoalStatusArray
import termios
import sys, tty
from sensor_msgs.msg import LaserScan


def intro():
        os.system("clear")
        print("PRESS 1,2,3 or 4:\n")
        print("[1]- Planning motion")
        print("[2]- Manual motion")
        print("[3]- Assisted-manual motion")
        print("[4]- Exit\n")
        

                
def move_base():

        pub_movebase = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size = 50)
 
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
        os.system("clear")
        print("--- MANUAL DRIVE----\n")
        print("Press:\n[w]: Forward\n[a]: Left\n[d]:Right\n[s]: Back\n[q]: Quit\n")
        
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

        min_fright = min(min(msg.ranges[144:287]), 5)
        min_front =  min(min(msg.ranges[288:431]), 5)
        min_fleft =  min(min(msg.ranges[432:575]), 5)
        
        return min_fright, min_front, min_fleft


def take_action(min_fright,min_front, min_fleft):
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
        
        
        
def assisted_manual():

        os.system("clear")
        vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size= 50)

        

        my_vel = Twist()
        my_vel.linear.y = 0
        my_vel.linear.z = 0
        my_vel.angular.x = 0
        my_vel.angular.y= 0
        
        print("--- ASSISTED MANUAL DRIVE----\n")
        print("Press:\n[w]: Forward\n[a]: Left\n[d]:Right\n[s]: Back\n[q]: Quit\n")
        
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
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                                
                                
                                
   
        
        
        



