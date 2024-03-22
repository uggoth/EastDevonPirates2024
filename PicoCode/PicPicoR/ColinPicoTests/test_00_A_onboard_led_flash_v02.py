module_name = 'test_00_A_onboard_led_flash_v02.py'

import utime
from machine import Pin
from os import uname

print (module_name, 'starting')

if 'W' in uname()[4]:
    print ('running on a Pico W with WiFi')
    led = Pin('LED', Pin.OUT)
else:
    print ('running on a Pico with no WiFi')
    led = Pin(25, Pin.OUT)

for i in range(40):
    led.toggle()
    utime.sleep(0.15)

led.off()

print (module_name, 'finished')
