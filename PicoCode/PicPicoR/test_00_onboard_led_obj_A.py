module_name = 'test_00_onboard_led_A_obj.py'

print (module_name, 'starting')

import ThisPico_Q_V30 as ThisPico
import utime

obled = ThisPico.ThisOnboardLED()

for i in range(40):
    obled.toggle()
    utime.sleep(0.15)

obled.off()

print (module_name, 'finished')
