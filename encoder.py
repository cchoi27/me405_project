from pyb import Pin, Timer
class Encoder:
    # interface with quadrature encoders
    
    def  __init__ (self, IN1_pin, IN2_pin, timer):
        '''
            interface with quadrature encoder
        '''

        self.timer = timer
        self.tim_chan1 = timer.channel(1, pin=IN1_pin, mode=Timer.ENC_AB)
        self.tim_chan2 = timer.channel(2, pin=IN2_pin, mode=Timer.ENC_AB)

        self.threshold = timer.period()/2
        self.period = timer.period()

        self.position = 0
        self.prev_position = 0
        self.delta = 0
        self.prev_count = 0

        #pass
    
    # updates encoder position and delta
    def update(self):
        current_count = self.timer.counter()
        difference = current_count - self.prev_count

        if abs(difference) > self.threshold:
            if difference > 0:
                difference -= self.period  # overflow adjustment
            else:
                difference += self.period  # underflow adjustment

        self.position += difference
        self.delta = difference
        self.prev_count = current_count

    # get the most recent encoder
    def get_position(self):
        return self.position

    # get the most recent encoder detlta
    def get_delta(self):
        return self.delta
    
    # reset the encoder position to zero
    def zero(self):
        self.position = 0
        self.prev_position = 0
        self.delta = 0
    
