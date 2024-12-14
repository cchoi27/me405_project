# me405_project

Hello. This is Sofia Dias's and Christine Choi's final project for ME 405. 
The Romi Robot must follow a line on an arena. The robot uses a proportional control to follow the lines smoothly. 

This Romi uses:
- [Romi Robot Kit](https://www.pololu.com/product/4022)
- [8-Channel QTRX Sensor Array](https://www.pololu.com/product/3672)
- IMU
- [Bump Sensor](https://www.pololu.com/product/1403)

View the [Demo](https://youtu.be/HECtpBxoPgs)



# **Line Following Mechanism**
- Uses an array of QTRX sensors to detect and follow a line.
- Implements a PID (Proportional-Integral-Derivative) controller for precise movement adjustments based on the line position.
- Adjusts motor speeds dynamically to correct deviations from the line.
 ## PID Control Finetuning
- Proportional (KP): Adjusts motor speeds based on the current error
- Integral (KI): Accounts for past errors
- Derivative (KD): Rate of change in error with a moving average

## Moving Average Smoothing
- Applies a moving average filter to smooth error and improve stability in line detection. This is applied to the derivative
## Object detection with bump sensor
- Equipped with a bumper sensor that triggers when a collision occurs (in this case, a box in the middle of the track)
- The robot backs up and makes a semi circle around the box

#**Feedback**
##IMU Integration for Navigation
- Uses a BNO055 IMU sensor to measure heading and maintain orientation during recovery and final maneuvers
- Implements heading error correction to realign the robot's direction
##Encoder Feedback for Position Tracking
- Tracks wheel rotations using encoders to measure distance traveled
- Employs encoder data to determine the completion of recovery and navigation maneuvers
