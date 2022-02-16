# Second Assignment

## Introduction

In the second assignment of Research Track course, we were asked to use Ros arhitecture for mooving a robot inside a circuit. 

## How to run the program

After have downloaded the package, divide the terminal in two part and enter:

```bash
rosrun stage_ros stageros $(rospack find second_assignment)/world/my_world.world
```

```bash
rosrun nodes interface_node
```

```bash
rosrun nodes motion_node
```

## Interface_node |Pseudocode

This node through a while loop, ask continuously the client to enter commands for resetting the position, increasing or decreasing the speed. The last two commands are published in the topic /Command, whereas the first command trigger the service for /reset_positions. 

```c++
#include "ros/ros.h"
#include "nodes/Command.h" //type command topic, whose structure is in msg folder
#include "std_msgs/Empty.h". //type reset service


int main(){
  while ros::ok(){

    ros::init()
    ros::Publisher pub
    ros::Node nh
    pub = nh.Advertise<>()
    ros::ServiceClient reset = type of /reset_positions service
    std_msgs::Empty srv;
    
    cin << command
    if command == 1{
          reset.call(srv)}
    if command == 2{
      publish command}
    if command == 3{
      publish command
    }
    
  }
   
```

## Motion_node

This node deals with the motion of the robot. The node is subscribed in:

* /base_scan for the informationos about distances
* /Command for the informations about the command pressed by the user

And can publish in:

* /cmd_vel the topic where publish velocities

After being subscribed in each topic, every time messages is published in the topic functions are called:

* /base_scan call enviromentcallback()
* /Command call commandcallback()

```c++

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

```

### Enviromentcallback

This function retrive a vector of 720 items and divide it into five regions: front, right , left , front-right, front-left. Hence, for those regions is calculated the minimum.



```c++
void enviromentcallback(const sensor_msgs::LaserScan::ConstPtr& msg1){
        //coping the array
        for(i = 0 ; i< 720 ; i++){
                pos[i] = msg1 -> ranges[i];}
                
         //DIVIDING IT INTO REGIONS AND CALULATE THE MINIMUM
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
```

At the end is called controll_speed().

### Controll_speed()

This function in base of minimum calculated before will not crash into boundaries and continue smoothly in the whole circuit.

``` c++
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
	
	publisg velocity

``` 

### Commandcallback()

In this function, the comand published in interface_node is retrivied. Accordingly to the command the variable speed_factor is incremented or decremented. Speed_factor is multiplied with the linear velocity allowing the user to controll the speed. Notice that incrementing too much the speed the robo will not complete the circuit.

``` c++

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

```










