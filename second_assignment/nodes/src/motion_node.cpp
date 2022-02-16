#include "ros/ros.h"
#include "nodes/Command.h" //topic for communicating user's command with motion_node
#include "geometry_msgs/Twist.h" //topic cmd_vel
#include "sensor_msgs/LaserScan.h" //topic base_scan
#include <iostream>
#include <string>


#define SIZE 9

//variables 

float pos[720];
std::string state_description;
float min_front = 30 ;
float min_left = 30;
float min_right = 30;
float min_fright = 30;
float min_fleft = 30;
int i;

geometry_msgs::Twist my_vel;
ros::Publisher pub;
ros::Subscriber sub;
ros::Subscriber sub2;
int speed_factor = 1;
int command;

void control_speed();

//function for increamenting or decreamenting speed
void commandcallback(const nodes::Command::ConstPtr& msg0){     
        
        msg0 -> command;
        ROS_INFO("I heard : %d", msg0 -> command);  
        
	if (msg0 -> command == 2){ 
		speed_factor += 1;
		}

	if (msg0 -> command == 3){
		speed_factor -= 1;
                }       
           
          }
          
void enviromentcallback(const sensor_msgs::LaserScan::ConstPtr& msg1){
        for(i = 0 ; i< 720 ; i++){
                pos[i] = msg1 -> ranges[i];}
                
                
        //front side 
	for (i = 355 ; i < 365  ; i++){

	        if (pos[ i ] < min_front){
	                min_front = pos[ i ];
	                }
                }
              
        
        //fleft side 
       	for (i = 499 ; i < 509  ; i++){
	       
	        if (pos[i] < min_fleft){
	                min_fleft = pos[i];
	                }
                }
                
        //fright side
       	for (i = 211 ; i < 221  ; i++){
	     
	        if (pos[ i ] < min_fright){
	                min_fright = pos[ i ];
	                }
                }
        
        //right side
	for (i = 0 ; i < 10 ; i++){
		if (pos[ i ] < min_right){
	                min_right = pos[ i ];
	                }
		}

	//left from 710 to 720
	for (i = 710 ; i < 720 ; i++){
	
		if (pos[ i ] < min_left){
	                min_left = pos[ i ] ;
	                }
                }

        control_speed();
        
        }


void control_speed(){
    
    
    if (min_front > 0.9 and min_fleft > 0.9 and min_fright > 0.9){
        state_description = "case 1 - nothing" ;
        my_vel.linear.x = 0.6 * speed_factor;
        my_vel.angular.z = 0;}
    else if (min_front < 0.9 and min_fleft > 0.9 and min_fright > 0.9){
        state_description = "case 2 - front";
        my_vel.linear.x = 0;
        my_vel.angular.z = 0.5;}
    else if (min_front > 0.9 and min_fleft > 0.9 and min_fright < 0.9){
        state_description = "case 3 - fright";
        my_vel.linear.x = 0 * speed_factor;
        my_vel.angular.z = 0.5;}
    else if (min_front > 0.9 and min_fleft < 0.9 and min_fright > 0.9){
        state_description = "case 4 - fleft";
        my_vel.linear.x = 0 ;
        my_vel.angular.z = -0.5;}
    else if (min_front < 0.9 and min_fleft > 0.9 and min_fright < 0.9){
        state_description = "case 5 - front and fright";
        my_vel.linear.x = 0;
        my_vel.angular.z = 0.5;}
    else if (min_front < 0.9 and min_fleft < 0.9 and min_fright > 0.9){
        state_description = "case 6 - front and fleft";
        my_vel.linear.x = 0;
        my_vel.angular.z = -0.5;}
    else if (min_front < 0.9 and min_fleft < 0.9 and min_fright < 0.9){
        state_description = "case 7 - front and fleft and fright";
        my_vel.linear.x = 0;
        my_vel.angular.z = 0.5;}
    else if (min_front > 0.9 and min_fleft < 0.9 and min_fright < 0.9){
        state_description = "case 8 - fleft and fright";
        my_vel.linear.x = 0.5 * speed_factor;
        my_vel.angular.z = 0;}
    else{
        state_description = "unknown case";}

    

    std::cout<<state_description<<"\n";

    min_front = 30;
    min_right= 30;
    min_left = 30;
    min_fright = 30;
    min_fleft = 30;
    pub.publish(my_vel);
}

int main (int argc, char **argv)
{

                ros::init(argc, argv, "motion_node"); 
                ros::NodeHandle nh;

                
                //Define publisher in cmd_vel which controls the robot in the map 
                pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel",1);
                //Define subscriber in nodes/Command wich it returns comands pressed by user
                sub = nh.subscribe("/command",1, commandcallback);
                //Define subscriber in base_scan which returns distance from 0 to 180
                sub2 = nh.subscribe("/base_scan", 1, enviromentcallback);
                
                ros::spin();

        

        
        
        
}
