from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(28))

def buzz(s):
    for i in range(s):
        buzzer.freq(1000)
        buzzer.duty_u16(50000)
        sleep(1)
        buzzer.duty_u16(0)
        sleep(1)
