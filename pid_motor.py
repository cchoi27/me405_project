from pyb import Pin, Timer
import encoder
import ROMI_MOTOR


class PID_motor:
    # interface with quadrature encoders
    
    def  __init__ (self, motor, encoder, kp, ki, kconstant, maxspeed):
        '''
            interface with quadrature encoder
        '''
        
        self.motor = motor
        self.encoder = encoder
        self.kp = kp
        self.ki = ki
        self.kc = kconstant
        self.max_speed = maxspeed
        self.integral_error = 0
        #pass
    
    # updates encoder position and delta
    def pi_controller(self, encoder_val, desired_val, integral_error):
        error = desired_val - encoder_val
        integral_error += error  # Accumulate integral error
        control_effort = self.kp * error + self.ki * integral_error + self.kc
        return control_effort, integral_error

        
    def set_pid_duty(self, desired_clicks):
        self.encoder.update()
        position_delta = self.encoder.get_delta()
        effort, self.integral_error = self.pi_controller(position_delta, desired_clicks, self.integral_error)
        effort = max(min(effort, self.max_speed), -self.max_speed)
        print(effort)

        self.motor.set_duty(effort)

if __name__ == '__main__':
    tim_2 = pyb.Timer(2, freq = 20_000)
    motor_l = ROMI_MOTOR.ROMI_MOTOR(direction_pin=Pin.cpu.C15, enable_pin=Pin.cpu.B0, effort_pin=Pin.cpu.A0, timer=tim_2, channel=1)
    motor_r = ROMI_MOTOR.ROMI_MOTOR(direction_pin=Pin.cpu.C1, enable_pin=Pin.cpu.C0, effort_pin=Pin.cpu.A1, timer=tim_2, channel=2)
    
    tim_1 = Timer(1, prescaler=0, period=65535)
    encoder_l = encoder.Encoder(IN1_pin=Pin.cpu.A8, IN2_pin=Pin.cpu.A9, timer=tim_1)
    # motor_l = ROMI_MOTOR.ROMI_MOTOR(direction_pin=Pin.cpu.C15, enable_pin=Pin.cpu.B0, effort_pin=Pin.cpu.A0, timer=tim_2, channel=1)
    
    tim_3 = Timer(3, prescaler=0, period=65535)
    encoder_r = encoder.Encoder(IN1_pin=Pin.cpu.B4, IN2_pin=Pin.cpu.B5, timer=tim_3)
    # tim_2 = pyb.Timer(2, freq = 20_000)
    
    closed_right = PID_motor(motor_r, encoder_r, .15, .1, 5, 30)

    # motor_r.enable()
    # motor_l.enable()
    
    while True:
        encoder_l.update()
        position_l_delta = (encoder_l.get_delta())
        print(position_l_delta)

        motor_l.set_duty(30)
        closed_right.set_pid_duty(3)
