from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum

def getEnv():
    pin = Pin(26, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t  = (sensor.temperature)
    h = (sensor.humidity)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    return((sensor.temperature),(sensor.humidity))
    
print(getEnv())