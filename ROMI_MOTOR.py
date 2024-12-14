from pyb import Pin, Timer
class ROMI_MOTOR:

    def  __init__ (self, enable_pin, direction_pin, effort_pin, timer, channel):

        self.ENABL = Pin(enable_pin, mode=Pin.OUT_OD, pull=Pin.PULL_UP)        #enable
        self.DIREC = Pin(direction_pin, mode=Pin.OUT_PP)
        self.CHAN = timer.channel(channel, pin=effort_pin, mode=Timer.PWM, pulse_width_percent=0)
        
    def set_duty(self, effort):
        '''
        '''
        direction = 0
        if effort > 0:
            self.DIREC.low()  # Forward direction
            if effort > 100:
                effort = 100
            direction = 1
        elif effort < 0:
            self.DIREC.high()  # Reverse direction
            if effort < -100:
                effort = -100
            effort = -effort  # Convert to positive for PWM
            direction = 0

        else:
            effort = 0  # Stop the motor
            
        self.CHAN.pulse_width_percent(effort)
        
            
    def enable(self):
        self.ENABL.high()

    def disable(self):
        self.ENABL.low()
        
    def set_direction(self, direction):
        if direction:
            print("forwards")
            self.DIREC.low() 
        else:
            print("backwards")
            self.DIREC.high() 

