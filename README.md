# me405_project

Hello. This is Sofia Dias's and Christine Choi's final project for ME 405. 
The Romi Robot must follow a line on an arena. The robot uses a proportional control to follow the lines smoothly. The arena had curves, sharp turns, and a box obstacle.

This Romi uses:
- [Romi Robot Kit](https://www.pololu.com/product/4022)
- [8-Channel QTRX Sensor Array](https://www.pololu.com/product/3672)
- IMU 
- [Bump Sensor](https://www.pololu.com/product/1403)

View the [Demo](https://youtu.be/HECtpBxoPgs) !

![alt text](https://github.com/cchoi27/me405_project/blob/main/IMG_6417.jpg)




# **Line Following Mechanism**
- Uses an array of QTRX sensors to detect and follow a line.
- Implements a PID (Proportional-Integral-Derivative) controller for precise movement adjustments based on the line position.
- Adjusts motor speeds dynamically to correct deviations from the line.
 ## PID Control Finetuning
- Proportional (KP): Adjusts motor speeds based on the current error
- Integral (KI): Accounts for past errors
- Derivative (KD): Rate of change in error with a moving average
More about our implementation below

## Moving Average Smoothing
- Applies a moving average filter to smooth error and improve stability in line detection. This is applied to the derivative
## Object detection with bump sensor
- Equipped with a bumper sensor that triggers when a collision occurs (in this case, a box in the middle of the track)
- The robot backs up and makes a semi circle around the box

#  **Feedback**
## IMU Integration for Navigation
- Uses a BNO055 IMU sensor to measure heading and maintain orientation during recovery and final maneuvers
- Implements heading error correction to realign the robot's direction
## Encoder Feedback for Position Tracking
- Tracks wheel rotations using encoders to measure distance traveled
- Employs encoder data to determine the completion of recovery and navigation maneuvers


# Build Instructions with a Romi
1. Calibrate the QTRX sensor array. Record an all-white array. Add this all-white array to the sensor class. Now whenever the sensors are read, the offset will be given. This is usually more accurate than the pure value. Find more information about the line sensors and calibration below. 
2. Observe for a threshold for black lines. To simplify the PID controller, these analog values are turned to binary.
3. Adjust encoder values. These will differ depending on the motor and battery voltage level. A closed-loop class is included to ensure consistent results.
4. Adjust the IMU. The starting position of when the ROMI is configured is typically the starting heading, 0. 
5. Adjust PID constants (KP, KI, KD) to suit the specific track and robot behavior. Tips we learned will be written below.
6. Compile and upload the code to the microcontroller.
7. Place the robot on the track and initiate line-following mode.

![alt text](https://github.com/cchoi27/me405_project/blob/main/me_405_sensors.png)


# Line Following Logic
A way ensure that the robot can follow the line is to have the both sides of the array equal. It is not enough to attempt to keep a line inside the middle since the track has parts of the line being dashed or perpendicular crossing. Ensuring that the left part of the array is always seeing something equal to the right side is part of the error correction. 
We implemented this logic with a weighted array, multiplying all the values with [-4, -3, -2, -1, 1, 2, 3, 4] and took the sum of that as the error. If the left and right were matching, the error is 0. Else, the error is weighted on how much difference there is between the left and right sensors. 
This success is highly dependent on lighting and thresholding. If values are inconsistent, we found success in adding a line of tape to shield the line sensor from the room's light conditions. 

# PID calibration tips
**Start with Proportional**
-  If the wheels aren't changing fast enough, increase KP
-  If the wheels seem to be overshooting, decrease KP
  
**Integral**
- This is the sum of accumulated errors
- This can be adjusted to be the moving average of errors instead. This may be more useful in a line following configuration
- If the system's outputs seem to be "degrading" the longer the system runs, increase KI
- NOTE: We did not have to use a KI value

**Derivative**
- This is the rate of change in error
- A moving average can also be used to incorporate past delta errors
- This will put more influence on sudden  changes, such as sharp turns and squiggles
- NOTE: Our system had a very influential KD

**Other controls**
In our system, more adjustments were added beyond PID, such as feedforward adjustments. These are added through observation. For example, due to the K constant value, the opposing motor would never drive negative, which was crucial for sharp turns. Depending on the polarity of the adjusted error, the left or right motor would have an increased subtraction to allow for this correction. 

  


