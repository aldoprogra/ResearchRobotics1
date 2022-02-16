#include "ros/ros.h"
#include "nodes/Command.h" //topic for communicating user's command with motion_node
#include "std_srvs/Empty.h"
#include <iostream>




//Publisher initializing
ros::Publisher pub;

int command;


int main (int argc, char **argv)
{

       
        ros::init(argc, argv, "interface_node"); 
        ros::NodeHandle nh;
        
        //topic
        pub = nh.advertise<nodes::Command>("/command",1);
        nodes::Command com;
        ros::Rate rate(20);
  
        //reset_position
        ros::ServiceClient reset = nh.serviceClient<std_srvs::Empty>("/reset_positions",1);
        std_srvs::Empty srv1;
      
        
        //user interface
        std::cout<<"Enter the following commands:\n1 = RESET\n2= INCREASE SPEED\n3 = DECREASE SPEED\n";
       
        while(ros::ok()){
        
                std::cin >> command;
                
                
                if(command == 1){
                        reset.call(srv1);
                
                                }
                
                if(command == 2){
                        com.command = 2;
                                }
                
                if(command == 3){
                        com.command =3;
                                }
                

                
                std::cout <<"Command is:"<<command << "\n";
                pub.publish(com);
                rate.sleep();
        
               }
               
}

