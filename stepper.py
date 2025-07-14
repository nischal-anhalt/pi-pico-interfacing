from machine import Pin
import utime

class StepperMotor:

    def __init__(self):
        # Define stepper pins (GP0–GP3)
        self.pins = [Pin(i, Pin.OUT) for i in range(4)]
        # Full-step sequence
        self.sequence = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

    def step_motor(self, steps, direction=1, delay=0.002):
        for _ in range(steps):
            for step in self.sequence[::direction]:
                for i in range(4):
                    self.pins[i].value(step[i])
                utime.sleep(delay)

    def rotate_to_angle(self, angle, direction=1):
        steps_per_rev = 512
        steps = int((angle / 360) * steps_per_rev)
        self.step_motor(steps, direction)