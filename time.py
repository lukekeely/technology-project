import time

def getTime():
    millis = int(time.ticks_ms())
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    hours = int(hours)
    
    if len(str(minutes)) < 2:
        minutes = "0"+ str(minutes)
        
    if len(str(hours)) < 2:
        if len(str(hours)) < 1:
            hours = "00"+ str(hours)
        hours = "0"+ str(hours)
        
    return (f"{hours}:{minutes}")

print(getTime())
