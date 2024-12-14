import time
import pyb
from pyb import Pin, ADC



class QTRXSensorArray:
    # init
    def __init__(self, control_odd, control_even, sensor_pins):
            # Setup control pins for QTRX sensor (PB0 and PC0)
            self.control_odd = Pin(control_odd, Pin.OUT)
            
            self.control_even = Pin(control_even, Pin.OUT)
            
            self.sensors = [(Pin(pin, Pin.IN)) for pin in sensor_pins]
            self.pins = sensor_pins
            self.sum = [0, 0, 0, 0, 0, 0, 0, 0]
            self.readings = 0
            self.threshold = 20

    def change_threshold(self, num):
        self.threshold = num

                    
    def dim_leds(self):
        for i in range (15):
            self.control_odd.low()
            self.control_even.low()
            time.sleep_us(1)
            self.control_odd.high()
            self.control_even.high()
            time.sleep_us(1)
    
    def read_bin(self):
        sensor_values = [(1 if sensor.read()>self.threshold else 0) for sensor in self.sensors]
        print(f'{sensor_values}')
        
    def read_adc(self):
        
        sensor_values = [sensor.read() for sensor in self.sensors]
        print(sensor_values)
        bin_values = [(1 if sensor_val>self.threshold else 0) for sensor_val in sensor_values]
        print(bin_values)

        
    def print_sensors_test_bin(self):
        self.dim_leds()
        self.changing_to_outputs()
        self.changing_to_inputs()
        
        self.read_bin()
        time.sleep_us(1)
        self.read_bin()

        time.sleep_us(1)
        self.read_bin()

        
        self.control_odd.low()
        self.control_even.low()
        print("----")
        
    def read_cal_sensors(self):
        #actually the read_sensor
        self.dim_leds()
        self.changing_to_outputs()
        self.changing_to_inputs()
        time.sleep_us(500)
        sensor_values = [sensor.read() for sensor in self.sensors]
        self.control_odd.low()
        self.control_even.low()
        calibrated = [a - b for a, b in zip(sensor_values, self.sum)]
        return calibrated, sensor_values
        
    def read_sensors(self):
        #actually the read_sensor
        self.dim_leds()
        self.changing_to_outputs()
        self.changing_to_inputs()
        time.sleep_us(500)
        sensor_values = [sensor.read() for sensor in self.sensors]
        self.control_odd.low()
        self.control_even.low()
        return sensor_values
        
    def changing_to_outputs(self):
        #changes to outputs and drives it HIGH
            self.sensors = [(Pin(pin, Pin.OUT)) for pin in self.pins]
            for sensor in self.sensors:
                sensor.value(1)
            time.sleep_us(10)
            
    def changing_to_inputs(self):
            self.sensors = [(ADC(pin)) for pin in self.pins]

    def print_average(self):
        print(self.readings)
        array = [int(sum/self.readings) for sum in self.sum]
        print(array)

    def calibration(self):
        #calibrate
        
        total_array = [0,0,0,0,0,0,0,0]
        for i in range(10):
            print("Calibrating")
            cal_values = self.read_sensors()
            for i, val in enumerate(cal_values):
                total_array[i] += val
            time.sleep(1)
                
        self.sum = [int(sum/10) for sum in total_array]
        print(self.sum)

    def set_calib(self, calib):
        self.sum =calib 
            

if __name__ == '__main__':
    
    qtr = QTRXSensorArray(control_odd = Pin.cpu.B7, control_even=Pin.cpu.B13, sensor_pins=[Pin.cpu.C3, Pin.cpu.C2, Pin.cpu.A5, Pin.cpu.A6,  Pin.cpu.A7,  Pin.cpu.B1, Pin.cpu.C5,  Pin.cpu.C4])


#high: [2831, 2596, 1631, 2620, 2490, 2292, 1745, 1557]
#find your calibration of all white sensors!

    while True:
        
        sensors = qtr.read_sensors_test()
        # print(sensors)
                
        # Sleep for a bit before reading again
        time.sleep(1)