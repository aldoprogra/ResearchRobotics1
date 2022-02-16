
# First Assignment

## Introduction

In the first assignment a __robot__ should do an infinite number of laps in a circuit avoiding touching _gold tokens_ in a __clockwise counter direction__ . Along the way, the robot will find some silver tokens which the robot should __grab__ and moove __behind__ .


### How to run the program

Firsly, download the folder "assignment" and after mooving to the working directiory inside "robot-sim", run in the command line:


```bash

python2 run.py assignmentnovember.py

```

Then you should see a simulation of a robot mooving in the track.

## Pseudocode

Part almost equal to past exercises:

* Declare libraries, object of  Robot class, inizialise some parametres. 
* Define functions turn() and drive() for mooving the robot linearly and angularly. 
* Define find_golden_token() and find_silver_token(). They returns angles and distances between correct silver and golden token in __front__ of the robot.

### grab_function() 

This function allows the robot allign himself and go towards the silven token.

```python
def grab_function():

        while 1:

                if far from golden token:
                        distance, angle = find_silver_token()
                        
                else:
                        Not_crash()
                        
                if near a silver token:
                        grab it
                        turn 180°
                        release
                        turn 180°
                        control()
                        
                elif far from silver token and well alligned:
                        moove to it 
                
                elif disalligned:
                        allign
                        
```

After releasing the token grab_function calls control() and if the robot is near a token calls Not_crash().

### Not_crash()

This function allows the robot to __avoid touching__ golden boxes

```python

def Nor_crash:      

                  
        distancegold,anglegold = find_gold_token()
        distancesilver,anglesilver = find_siver_token()
        
        """ when a gold box is in front of the robot he should turn more than  90 grade, indeed is important when there are corner """
                
        if -20 < anglegold < 20 then
        
                distance_gold_left, distance_gold_right = __find_corner__()
         
                if distance_gold_right < distance_gold_left then 
                        turn left
                
                else:
                        turn right
                        
        """ when a gold box is aside the robot he should turn a little avoiding touching them, good when trajectory is linear """
               
        elif  20 < anglegold <  90  then
                turn a little left
        else:
                turn a little right
```

### find_corner()

 This function returns distances of the back left and back right from the Robot which allows Not_crash to find correct direction when he turns.
 
 ```python
 
 def find_corner(): 

         for token in R.see:
                if token is gold and token.dist < distance  and if angle token is between 100 and 120 then
                        token.dist = distance_gold_right
                if token is gold and token.dist < distance  and if angle token is between -100 and -120 then
                        token.dist = distance_gold_left
                
         return distance_gold_left,distance_gold_right
 ```

### control()


This function menage the program to pass from grab_function to Not_crash and otherwise.


```python                       
def control(): 

        while 1:
                distance, angle = find_silver_token()
                distancegold, anglegold = find_gold_token()
                
                if distanzagold far from robot:
                
                        moove forward
                        
                        if angle silver is between 95 and 120:
                                break
                        
                        if angle is between -95° and - 120:
                                break
                        
                        
                if distanzagold near from robot:
                        Not_crash()
                        if 30 < anglesilver <30
                                break
```

## main

The main is  just:

```python

grab_function()

```

# Comments and possible improvements

Honestly, I have tested the program many times,in certain moment he changes direction and goes no more in a clockwise counter. 
Even though, his capacity of always taking a silver token and he never touches boundaries of the arena.  
I did not menage to find an optimal algorythm which find the right direction in turning without never fail the direction.





