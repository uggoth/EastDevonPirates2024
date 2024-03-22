module_name = 'test_00_onboard_led_A.py'

import utime
from machine import Pin

print (module_name, 'starting')

led = Pin('LED', Pin.OUT)

for i in range(40):
    led.toggle()
    utime.sleep(0.15)

led.off()

print (module_name, 'finished')
