module_name = 'test_00_B_onboard_led_flash_v01.py'

import PicoBotF_v03 as ThisPico
import utime

print (module_name, 'starting')

my_led = ThisPico.onboard_led

for i in range(40):
    my_led.on()
    utime.sleep(0.15)
    my_led.off()
    utime.sleep(0.05)
    
print (module_name, 'finished')
