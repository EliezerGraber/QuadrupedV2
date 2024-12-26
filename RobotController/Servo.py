from machine import Pin, PWM
#import time
import asyncio

class Servo:
    # these defaults work for the standard TowerPro SG90
    __servo_pwm_freq = 50
    __min_u10_duty = 26 - 6 # offset for correction
    __max_u10_duty = 123- 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = -0.001


    def __init__(self, pin, min_u10_duty = 20, max_u10_duty = 123):
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.__initialise(pin)
        print(self.__min_u10_duty, self.__max_u10_duty)


    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    async def move(self, angle, delta = 0): #time in seconds
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            #print("redundant")
            return

        if angle < 0:
            #print("oos: 0")
            angle = 0

        if angle > 180:
            #print("oob: 180")
            angle = 180
        
        # calculate the new duty cycle and move the motor
        duty_u10 = self.__angle_to_u10_duty(angle)
        if delta == 0 or self.current_angle < 0:
            self.__motor.duty(duty_u10)
        else:
            old_duty_u10 = self.__angle_to_u10_duty(self.current_angle)
            inc = (duty_u10 - old_duty_u10)/250
            for x in range(250):
                self.__motor.duty(int(old_duty_u10 + inc * x))
                await asyncio.sleep_ms(int(delta*1000/250))
        self.current_angle = angle

    def __angle_to_u10_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty


    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        print(self.__angle_conversion_factor)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)