from __future__ import print_function

import time
from sr.robot import *


"""

        ASSIGNMENT 12/11/21 SINATRA GESUALDO UNIGE 

	        Run with:
	        $ python run.py assignmentnovember.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token and in front of the robot, without caring on what is behind (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist= 3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -20 < token.rot_y <  20:
            dist=token.dist
	    rot_y=token.rot_y
    if dist == 3:
	return -1, -1
    else:
   	return dist, rot_y


def find_golden_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token and in front of the robot, without caring on what is behind (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    distg= 3
    for token in R.see():
        if token.dist < distg and token.info.marker_type is MARKER_TOKEN_GOLD and -70  < token.rot_y < 70:
            distg=token.dist
	    rotg_y=token.rot_y
    if distg== 3:
	return -1, -1
    else:
   	return distg, rotg_y


def find_corner():
	""" 
	This function looks for the right direction in which turn when the robot is near boundaries. 
	
	Returns :
	    dist1 right back side 
	    dist2 left back side.
	         
	In Not_crash() distancies will be analised, the one side which has the longest distance is the correct corner.
	"""
	
	dist1 = 100
	print("Looking direction")
    	for token in R.see():
		if token.dist < dist1 and token.info.marker_type is MARKER_TOKEN_GOLD and  100 < token.rot_y < 120: 
			dist1 = token.dist
			
	dist2 = 100	
	for token in R.see():	
	 	if token.dist < dist2 and token.info.marker_type is MARKER_TOKEN_GOLD and  -100 > token.rot_y > -120 : 
	 	        dist2 = token.dist 	
	
        if dist1 == 100 and dist2 == 100:
                print("Something doesn't work")
                return -1
	
	else:
	        print("I have returned parameters")
	        return dist1, dist2
	        
def Not_crash():
	"""
	This function avoit the robot touching boundaries. According to the angle between robot and the near golden token he turns more or less .
	"""
	
	distg, rotg_y = find_golden_token()
	dist, rot_y = find_silver_token()
        
        
	if  -20 <= rotg_y <= 20: # if we have to turn more than 90 grade  we call find_corner()
	       
	       
	       dist1,dist2 = find_corner()    
	       """ Comparing distancies and choose in which direction turn"""          
	       if dist2 > dist1 or 70 < rot_y < 110:
		                        
	                print("Turning left")
		        turn(-20,1.8)
		       
		                        
	             
               elif dist2 < dist1 or -70 > rot > -110:
                        
                        print("Turning right")	
		        turn(20,1.8)
		        
		        
	       
	elif 20 <  rotg_y <= 25:

		print("Turn left..")
		turn(-20,0.4)	
		

	 	
        elif 25 < rotg_y <= 90:
	 	
	 	print("Turning  a little left..")
		turn(-20,0.2)
		
        elif -20 > rotg_y >= -25:
	 	
	 	print("Turning right..")
		turn(20,0.4)

		
	elif -25 > rotg_y >= -90:
	 	
	 	print("Turning a little right..")
		turn(20,0.2)
	       


	       
def control():
        """ This function menages situations, if a silver token could be grab he calls grab_function() , otherwise in case the robot is near boundaries calls Not_crash()"""
        while 1:
        
                distg,rotg_y = find_golden_token()
                dist, rot_y = find_silver_token()
                
                print("Going ahead")
                drive(120,0.03)
                
                if  distg >= 0.9:
                
                        print("Going ahead")
                        drive(120,0.03)
                        
                        if 0 < dist < 3:
                                print("I have found something ")
                                break
                        
                
                elif  distg <  0.9:
                        
                        Not_crash()
                        
                        if   0 < dist < 3:
                        
                               print("I have found something ")
                               break
                                        
                                     


def grab_function():   	

        while 1:

            distg,rotg_y = find_golden_token()
            """ Going on grabbing the token only if we are far from boundaries"""
            dist, rot_y = find_silver_token()
           
            if   distg < 0.7: 
       
               print("entro in Not_crash")
               Not_crash()
        	
               """This part of code is the same of those of exercises"""  
            
            if dist == -1:
                
                control()
	        
            elif dist < d_th: # if we are close to the token, we try grab it.
            
                print("Found it!")
                if R.grab(): # if we are close to the token, we grab it.
                        print("Gotcha!")
                        turn(-20,3)
                        print("Now I release it")
                        R.release()
                        drive (-10,2)
                        turn(20,2.5)
                        """ After grabbing the token the code calls control() """            
                        control()               
                 
                else:   #sometimes the robot can't grab so doing this block he retry
                        drive(-30,2)
                        turn(0.5,0.5)        
	        
	        
            elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	        print("Ah, that'll do.")
                drive(120, 0.03)
        
            elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
                print("Left a bit...")
                turn(-10, 0.05)
                
            elif rot_y > a_th:
                print("Right a bit...")
                turn(10 , 0.05)
   	    
   	    else:
   	        control()
   	        
   	        
   	        
#THIS IS THE "MAIN":
grab_function()
