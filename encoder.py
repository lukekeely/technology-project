from machine import Pin
import time as t
button_pin = Pin(13, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(12, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(11, Pin.IN, Pin.PULL_UP)

previous_value = True
button_down = False
n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())

while True:
    if n != ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value()):
        n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())
        if previous_value != step_pin.value():
            if step_pin.value() == False:
                if direction_pin.value() == False:
                    print("turned left")
                else:
                    print("turned right")
            previous_value = step_pin.value()   

        if button_pin.value() == False and not button_down:
            print("button pushed") 
            button_down = True
        if button_pin.value() == True and button_down:
            button_down = False

        if button_pin.value() == False:
            print("button pressed")
