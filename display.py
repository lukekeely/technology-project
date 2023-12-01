from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum

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
            t  = '19C'
            h = '65%'
    return(t,h)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

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

time = input("Set time: ")
date = input("Set date: ")

led_level = "100"
buzzer_level = "100"
stepper_steps = "22"

Drop1 = "09:00"
Drop2 = "18:00"
Drop3 = "21:00"

Temp, Humidity = getEnv()

Info_Menu = ["Main Menu",
             f"T:{time} D:{date}",
             f"La:{Drop1} Ne:{Drop2}",
             f"Temp:{Temp} Hmd:{Humidity}"]

Main_Menu = ["Information","Settings","Config","About","Dispense Next"]

Settings_Menu = ["Main Menu",
                 f"Time :{time}",
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
           print_menu(currentMenu,currentOption)
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
           print("Dispensing")
           
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

# while True:
#     option = int(input("Choose an input: "))
#     if option == 8:
#         currentOption = onUp(currentOption)
#     elif option == 2:
#         currentOption = onDown(currentOption)
#     elif option == 6:
#         currentMenu,currentOption = onSelect(currentMenu,currentOption)
        
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
                    currentOption = onUp(currentOption)
                else:
                    print("turned right")
                    currentOption = onDown(currentOption)
                    
            previous_value = step_pin.value()   

        if button_pin.value() == False and not button_down:
            print("button pushed") 
            button_down = True
        if button_pin.value() == True and button_down:
            button_down = False

        if button_pin.value() == False:
            print("button pressed")
            currentMenu,currentOption = onSelect(currentMenu,currentOption)