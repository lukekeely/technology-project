from machine import I2C, Pin, PWM
from pico_i2c_lcd import I2cLcd
from machine import Pin, I2C
from dht import DHT11, InvalidChecksum

import time as t
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

button_pin = Pin(13, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(12, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(11, Pin.IN, Pin.PULL_UP)

previous_value = True
button_down = False
n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())

def Step(steps):
    while steps >= 0:
        for step in full_step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)
        steps -= 1
        
def FullStep():
    Step(22)

def getTime(c,h,m):
    #Fix
    hourc = h
    minc = m
    millis = int(t.ticks_ms())
    minutes=(millis/(1000*60))%60
    minutes = int(minutes) + minc
    hours=(millis/(1000*60*60))%24
    hours = int(hours) + hourc


    
    if len(str(minutes)) < 2:
        minutes = "0"+ str(minutes)
        
    if len(str(hours)) < 2:
        if len(str(hours)) < 1:
            hours = "00"+ str(hours)
        hours = "0"+ str(hours)
        
    return (f"{hours}:{minutes}")

def replaceInfoTime():
    lcd.move_to(2,1)
    lcd.putstr(getTime(False,0,0))
    
def replaceSettingsTime():
    if currentOption <= 4:
        if currentOption == 2:
            lcd.move_to(9,1)
            lcd.putstr(getTime(False,0,0))
        else:
            lcd.move_to(6,1)
            lcd.putstr(getTime(False,0,0))
    elif currentOption == 5:
        lcd.move_to(6,0)
        lcd.putstr(getTime(False,0,0))

def dispence():
    print("Dispensing")
    FullStep()
    #buzz(1)

def getEnv():
    try:
        pin = Pin(26, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        t  = (sensor.temperature)
        h = (sensor.humidity)
    except:
        try:
            t  = (sensor.temperature)
            h = (sensor.humidity)
        except:
            t  = '19.2'
            h = '47.0'
    return(t,h)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

buzzer = PWM(Pin(28))

#Commands
# lcd.blink_cursor_on()
# lcd.blink_cursor_off()
# 
# lcd.backlight_on()
# lcd.backlight_off()
# 
# lcd.putstr()
# lcd.clear()
# 
# lcd.move_to(x,y)

#Menus max 20 per item
time = '00:00'
date = '03/04/2022'

led_level = "100"
buzzer_level = "100"
stepper_steps = "22"

Drop1 = "09:00"
Drop2 = "18:00"
Drop3 = "21:00"

Temp, Humidity = getEnv()

Info_Menu = ["Main Menu",
             f"T:      D:{date}",
             f"La:{Drop1} Ne:{Drop2}",
             f"Temp:{Temp} Hmd:{Humidity}"]

Main_Menu = ["Information","Settings","Config","About","Dispense Next"]

Settings_Menu = ["Main Menu",
                 f"Time :     ",
                 f"Date :{date}",
                 f"Drop 1 :{Drop1}",
                 f"Drop 2 :{Drop2}",
                 f"Drop 3 :{Drop3}"]

Config_Menu = ["Main Menu",
               f"LED :{led_level}",
               f"Loudness :{buzzer_level}",
               f"Steps :{stepper_steps}"]

About_Menu = ["Main Menu",
              "Titus Medical",
              "Designed by [Blank]",
              "LC Technology 2022"]

def print_menu(options,selection):
    display_height = 4
    current_menu = options
    s = selection -1
    
    if selection - display_height < 0:
        down_vote = 0
    elif selection - display_height > len(current_menu) - display_height:
        down_vote = 0
    else:
        down_vote = selection - display_height
        
    lcd.clear()
    #height check
    if len(current_menu) >= display_height:
        for i in range(display_height):
            lcd.move_to(0,i)
            if s > len(current_menu) -1:
                s = len(current_menu) -1
            elif s < 0:
                s = 0
            
            if i +down_vote  == s:
                string = str(">> " + current_menu[i +down_vote])
                lcd.putstr(string)
            else:
                string = str(current_menu[i +down_vote])
                lcd.putstr(string)
    else:
        display_height = len(current_menu)
        for i in range(display_height):
            lcd.move_to(0,i)
            if s > len(current_menu) -1:
                s = len(current_menu) -1
            elif s < 0:
                s = 0
            
            if i == s:
                string = str(">> " + current_menu[i])
                lcd.putstr(string)
            else:
                string = str(current_menu[i])
                lcd.putstr(string)
                
currentMenu = Info_Menu
currentOption = 1
print_menu(currentMenu,currentOption)
replaceInfoTime()

def buzz(s):
    for i in range(s):
        buzzer.freq(1000)
        buzzer.duty_u16(50000)
        t.sleep(1)
        buzzer.duty_u16(0)
        t.sleep(1)

def setTime():
    button_pin = Pin(13, Pin.IN, Pin.PULL_UP)
    direction_pin = Pin(12, Pin.IN, Pin.PULL_UP)
    step_pin  = Pin(11, Pin.IN, Pin.PULL_UP)

    previous_value = True
    button_down = False
    n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())

    minshift = 0
    hourshift = 0
    
    lcd.move_to(9,1)
    lcd.putstr('     ')
    
    close = False
    t.sleep(0.5)
    while close == False:
        if n != ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value()):
            n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())
            if previous_value != step_pin.value():
                if step_pin.value() == False:
                    if direction_pin.value() == False:
                        print("turned left")
                        hourshift -= 1 
                    else:
                        print("turned right")
                        hourshift += 1  
                previous_value = step_pin.value()   
        if button_pin.value() == False:
            print("exit change")
            close = True
        if hourshift >= 0:
            msg = "+"+str(hourshift)+ " hrs  "
        else:
            msg = str(hourshift)+ " hrs  "
        lcd.move_to(10,1)
        lcd.putstr(msg)
        
    
    close = False
    t.sleep(0.5)
    while close == False:
        if n != ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value()):
            n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())
            if previous_value != step_pin.value():
                if step_pin.value() == False:
                    if direction_pin.value() == False:
                        print("turned left")
                        if minshift == -59:
                            minshift = 59
                        else:
                            minshift -= 1  
                    else:
                        print("turned right")
                        if minshift == 59:
                            minshift = -59
                        else:
                            minshift += 1  
                previous_value = step_pin.value()   
        if button_pin.value() == False:
            print("exit change")
            close = True
        lcd.move_to(10,1)
        if minshift >= 0:
            msg = "+"+str(minshift)+ " mins  "
        else:
            msg = str(minshift)+ " mins  "
        lcd.putstr(msg)
    lcd.move_to(9,1)
    lcd.putstr('        ')
    print("Adding",str(hourshift)+":"+str(minshift))
    getTime(True,hourshift,minshift)
    replaceSettingsTime()
        
def setDate():
    lcd.move_to(9,2)
    lcd.putstr('~~/~~/~~~~')
    
def setDrop():
    lcd.move_to(11,3)
    lcd.putstr('~~:~~')

def onDown(currentOption):
    Len_Info = 1
    Len_Main = 5
    Len_Settings = 6
    Len_Config = 4
    Len_About = 1
    
    if currentMenu == Main_Menu:
        if currentOption < Len_Main:
            currentOption += 1
            print_menu(currentMenu,currentOption)
            
    elif  currentMenu == Info_Menu:
        if currentOption < Len_Info:
            currentOption += 1
            print_menu(currentMenu,currentOption)
            
    elif  currentMenu == Settings_Menu:
        if currentOption < Len_Settings:
            currentOption += 1
            print_menu(currentMenu,currentOption)
            
    elif  currentMenu == Config_Menu:
        if currentOption < Len_Config:
            currentOption += 1
            print_menu(currentMenu,currentOption)
            
    elif  currentMenu == About_Menu:
        if currentOption < Len_About:
            currentOption += 1
            print_menu(currentMenu,currentOption)
    return currentOption

def onUp(currentOption):
    if currentOption > 1:
        currentOption -= 1
        print_menu(currentMenu,currentOption)
    return currentOption

def onSelect(currentMenu,currentOption):
    #Main
    if currentMenu == Main_Menu:
        if currentOption == 1:
           currentMenu = Info_Menu
           currentOption = 1
           print_menu(Info_Menu,currentOption)
           replaceInfoTime()
        elif currentOption == 2:
           currentMenu = Settings_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
        elif currentOption == 3:
           currentMenu = Config_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
        elif currentOption == 4:
           currentMenu = About_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
        elif currentOption == 5:
           dispence()
           
    #Info        
    elif  currentMenu == Info_Menu:
        if currentOption == 1:
           currentMenu = Main_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
           
    #Settings        
    elif  currentMenu == Settings_Menu:
        if currentOption == 1:
           currentMenu = Main_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
        elif currentOption == 2:
            setTime()
        elif currentOption == 3:
            setDate()
        elif currentOption == 4:
            setDrop()
        elif currentOption == 5:
            setDrop()
        elif currentOption == 6:
            setDrop()
    
    #Config
    elif  currentMenu == Config_Menu:
        if currentOption == 1:
           currentMenu = Main_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
    
    #About
    elif  currentMenu == About_Menu:
        if currentOption == 1:
           currentMenu = Main_Menu
           currentOption = 1
           print_menu(currentMenu,currentOption)
           
    return currentMenu,currentOption

last_pressed = t.ticks_ms()
screen = False

while True:
    if t.ticks_ms() - last_pressed > 20000:
        screen = False
        lcd.backlight_off()
        
    showTime = getTime(False,0,0)
    if showTime != getTime(False,0,0) and currentMenu == Info_Menu:
        showTime = getTime(False,0,0)
        replaceInfoTime()
    if currentMenu == Settings_Menu:
        replaceSettingsTime()
    if showTime in [Drop1, Drop2, Drop3]:
        dispense()
    
    if screen == False:
        if n != ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value()):
            n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())
            if previous_value != step_pin.value():
                if step_pin.value() == False:
                    if direction_pin.value() == False:
                        screen = True
                        last_pressed = t.ticks_ms()
                        lcd.backlight_on()
                    else:
                        screen = True
                        last_pressed = t.ticks_ms()
                        lcd.backlight_on()
                        
                previous_value = step_pin.value()   

            if button_pin.value() == False and not button_down:
                screen = True
                last_pressed = t.ticks_ms()
                lcd.backlight_on()
                
                button_down = True
            if button_pin.value() == True and button_down:
                button_down = False

    else:
        if n != ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value()):
            n = ("dir", direction_pin.value(), "step", step_pin.value(), "button", button_pin.value())
            if previous_value != step_pin.value():
                if step_pin.value() == False:
                    if direction_pin.value() == False:
                        print("turned left")
                        currentOption = onUp(currentOption)
                        last_pressed = t.ticks_ms()
                    else:
                        print("turned right")
                        currentOption = onDown(currentOption)
                        last_pressed = t.ticks_ms()
                        
                previous_value = step_pin.value()   

            if button_pin.value() == False and not button_down:
                print("button pushed")
                last_pressed = t.ticks_ms()
                button_down = True
            if button_pin.value() == True and button_down:
                button_down = False

            if button_pin.value() == False:
                print("button pressed")
                currentMenu,currentOption = onSelect(currentMenu,currentOption)
                last_pressed = t.ticks_ms()