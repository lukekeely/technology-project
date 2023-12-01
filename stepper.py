from machine import Pin
import utime

pins = [
    Pin(18,Pin.OUT),
    Pin(20,Pin.OUT),
    Pin(16,Pin.OUT),
    Pin(17,Pin.OUT),
    ]

full_step_sequence = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]

def Step(steps):
    while steps >= 0:
        for step in full_step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)
        steps -= 1
        
for i in range(22):
    Step(22)