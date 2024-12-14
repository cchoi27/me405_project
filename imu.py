import time

from machine import I2C
from bno055 import *  # Import your BNO055 class

def task_imu():
    """
    Task that initializes the IMU, tracks its heading, and checks if it returns to the starting position.
    """
    # Initialize I2C communication for the IMU
    i2c = machine.I2C(1, freq=400000)  # Set I2C frequency to 400kHz for better stability
    imu = BNO055(i2c)  # Initialize the BNO055 IMU sensor
    
    # Set initial relative starting position (heading)
    starting_heading = imu.euler()[0]
    
    print(f"Starting heading: {starting_heading}")
    
    while True:
        # Continuously read current heading from the IMU
        current_heading = imu.euler()[0]
        print(f"Current heading: {current_heading}")
        
        # Normalize heading error to be within 0 to 360 degrees
        heading_error = (current_heading - starting_heading) % 360
        
        # Check if the heading has returned to the starting position
        #if heading_error < 2 or heading_error > 355:
        if heading_error < 2:
            # If within range of the starting position (5 degrees tolerance)
            print("Back to where started!")
            print()
        
        else:
            print("Not back yet damn")
        # Yield to allow other tasks to run (if using cooperative multitasking)
        yield 0
        time.sleep(0.1)  # Adding a slight delay to avoid overwhelming the processor

# Example use in a cooperative multitasking system (pseudo-code)
if __name__ == '__main__':
    # Create the task that reads IMU and sends data to the queue
    imu_task = task_imu()
    
    # Run the task (in a real-time or cooperative multitasking setup)
    while True:
        imu_task.send(None)  # "Resume" the task each time it yields
        time.sleep(0.1)