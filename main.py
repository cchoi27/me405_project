import time
import pyb
from pyb import Pin, ADC,  Timer, ExtInt
import machine
import pyb

import ROMI_MOTOR, QTRXSensor
import encoder
import time
from array import array
import time
from machine import I2C
from bno055 import * 

KC = 15
KP = 0.8
KI = 0
KD = 2
max_speed = 40
prev_error = 0

prev_left = 10
prev_right = 10

MOVING_AVERAGE_WINDOW = 2
average_buffer = [0] * MOVING_AVERAGE_WINDOW

# Returns moving average
def moving_average(new_value):
    global average_buffer
    average_buffer.pop(0)
    average_buffer.append(new_value)
    return sum(average_buffer) / len(average_buffer)

bump_flag = 0
finish_flag = 0
# If the bump sensor was pressed, set bump_flag = 1
def bumpped_flag_toggle(the_pin):
    global bump_flag
    print("ouch")
    bump_flag = 1


button_int = ExtInt(Pin.cpu.C7, ExtInt.IRQ_FALLING,
Pin.PULL_UP, bumpped_flag_toggle)


motor = 1
# Switch to enable/disable for motors
def toggle_motors(the_pin):
    global motor
    
    if (motor):
        motor_r.enable()
        motor_l.enable()
        motor = 0
    else:
        motor_r.disable()
        motor_l.disable()
        motor = 1
        

button = ExtInt(Pin.cpu.C13, ExtInt.IRQ_FALLING,
Pin.PULL_NONE, toggle_motors)

# returns line following average using line sensor weights
def line_following_average(qtr, motor_l, motor_r):
    
    global prev_error, prev_right_error, prev_left, prev_right
    
    array, total =  qtr.read_cal_sensors()
    left_sensors = 0
    right_sensors = 0
     
    for i, sensor in enumerate(array):
        if (i < 4):
            right_sensors += sensor
        else:
            left_sensors += sensor
    
    weights = [-4, -3, -2, -1, 1, 2, 3, 4]
    line_array = [0 if val < 600 else 1 for val in array]
    
    adjusted = sum([a*b for a, b in zip(line_array, weights)])
    
    flipped_array = line_array[::-1]

    
    print(flipped_array)
    average = 0
    found = 0
    for i, sensor in enumerate(line_array):
        if (sensor):
            average += i
            found += 1
        
    if (found):
        average = (average /found)
        
    smoothed_position = moving_average(adjusted)
    
    print("difference", adjusted)
    
    subtract_from_right = 0
    subtract_from_left = 0
    pol = 1
    #pid stuff-----------
    if (adjusted < 0):
        print("going left, motor right higher")
        subtract_from_left = - adjusted *1.5 - abs(adjusted-smoothed_position)*1.8
        subtract_from_right = 0
        pol = 1
    elif (adjusted == 0):
        print("forward")
    else:
        #difference is negative
        print("going right, motor left higher")
        subtract_from_right = adjusted * 1.5 + abs(adjusted-smoothed_position)*1.8
        subtract_from_left = 0
        pol = -1

    
    integral = (adjusted-prev_error * KI)
    derivative = abs(adjusted-smoothed_position) *KD * pol
    proportional = (adjusted * KP) 
    print("pid", proportional, "int:", integral, "der:", derivative) 
    
    left_duty = KC + proportional + integral + derivative  + subtract_from_right 
    right_duty = KC - proportional - integral - derivative + subtract_from_left 
        
    print(left_duty, right_duty)
    
    print("------------------")
    #min max speed adjustment
    left_duty = min(left_duty, max_speed)
    right_duty = min(right_duty, max_speed)
    left_duty = max(left_duty, -5)
    right_duty = max(right_duty, -5)
    print(left_duty, right_duty)

    prev_left = left_duty
    prev_right = right_duty
    
    motor_l.set_duty(left_duty)
    motor_r.set_duty(right_duty)
        
    prev_error = adjusted

# for handling bumping
def bumped(motor_l, motor_r, imu):
    global bump_flag, finish_flag
    print("bump")    
    
    starting_heading = imu.euler()[0]
    heading_error = 100
    bump_flag = 0

    #back up
    motor_l.set_duty(-15)
    motor_r.set_duty(-15)
    time.sleep_ms(1000)

    #turn
    while( not (heading_error < (93) and heading_error > (87))):
        print(heading_error)
        
        motor_l.set_duty(15)
        motor_r.set_duty(-15)
        heading_error = (imu.euler()[0] - starting_heading) % 360 
    
    encoder_r.zero()
    encoder_r.update()
    while (not (  abs(encoder_r.get_position())> 5400)): #maybe add
        #circle left
        motor_l.set_duty(30)
        motor_r.set_duty(50)
        
        encoder_r.update()

        print(encoder_r.get_position())
        
    time.sleep_ms(2800)
            
    print("position", encoder_r.get_position())
    encoder_r.update()
    
    # heading_error = 100

    # while( not (heading_error < 5) or heading_error > (355)):
    #     print(heading_error)
        
    #     motor_l.set_duty(15)
    #     motor_r.set_duty(-15)
    #     heading_error = (imu.euler()[0] - starting_heading) % 360 
    
    bump_flag = 0
    finish_flag = 1
    motor_l.set_duty(0)
    motor_r.set_duty(0)
    
    
#initing our objects 

tim_2 = pyb.Timer(2, freq = 20_000)
motor_l = ROMI_MOTOR.ROMI_MOTOR(direction_pin=Pin.cpu.C13, enable_pin=Pin.cpu.B0, effort_pin=Pin.cpu.A0, timer=tim_2, channel=1)
motor_r = ROMI_MOTOR.ROMI_MOTOR(direction_pin=Pin.cpu.C1, enable_pin=Pin.cpu.C0, effort_pin=Pin.cpu.A1, timer=tim_2, channel=2)

tim_1 = Timer(1, prescaler=0, period=65535)
encoder_l = encoder.Encoder(IN1_pin=Pin.cpu.A8, IN2_pin=Pin.cpu.A9, timer=tim_1)

tim_3 = Timer(3, prescaler=0, period=65535)
encoder_r = encoder.Encoder(IN1_pin=Pin.cpu.B4, IN2_pin=Pin.cpu.B5, timer=tim_3)

i2c = I2C(1)  
imu = BNO055(i2c) 

if __name__ == '__main__':

    i2c = I2C(1)  
    imu = BNO055(i2c) 
    motor_r.enable()
    motor_l.enable()

    # set up line sensor
    qtr = QTRXSensor.QTRXSensorArray(control_odd = Pin.cpu.B7, control_even=Pin.cpu.B13, sensor_pins=[Pin.cpu.C3, Pin.cpu.C2, Pin.cpu.A4, Pin.cpu.A6,  Pin.cpu.A7,  Pin.cpu.B1, Pin.cpu.C5,  Pin.cpu.C4])

    qtr.change_threshold(1700)
    #qtr.calibration()
    qtr.set_calib([3015, 2611, 2544, 2414, 2581, 2694, 2664, 2670]) #adjust this to your speciifc calibration

    starting_heading = imu.euler()[0]
    print("starting heading", {starting_heading})

    time.sleep(1)
    while True:
        # if bump was true
        if (bump_flag == 1):
            bumped(motor_l, motor_r, imu, qtr)
            encoder_r.zero()
        # if finished
        if  (finish_flag == 1):
            encoder_r.update()       
            pos =  encoder_r.get_position()   
            print("encoder:", pos)
            if (pos > 8000):
                break
        
        line_following_average(qtr, motor_l, motor_r)
        
        #clear screen
        print("\033[2J\033[H")

    while True:
        #reach final position
        motor_l.set_duty(0)
        motor_r.set_duty(0)
        time.sleep_ms(200)
        encoder_r.zero()
        heading_error = (imu.euler()[0] - starting_heading) % 360 
        pos = 0
        
        while(pos<6500):
            
            encoder_r.update()
            pos = encoder_r.get_position()
            heading_error = (imu.euler()[0] - starting_heading) % 360 
            
            while( not (heading_error < 5) or heading_error > (355)):
                print("fixing header", heading_error)
                
                if ((heading_error > 180)):
                    motor_l.set_duty(10)
                    motor_r.set_duty(-10)
                else:
                    motor_l.set_duty(-10)
                    motor_r.set_duty(10)
                heading_error = (imu.euler()[0] - starting_heading) % 360 
            print("fixed, pos", pos)
                
            motor_l.set_duty(20)
            motor_r.set_duty(20)        
        break
    
    
    #romi done
    motor_l.set_duty(0)
    motor_r.set_duty(0)

