module_name = 'test_02_A_waiting_v02.py'

import PicoBotF_v03 as ThisPico
import utime

print (module_name, 'starting')

buttons = ThisPico.TheseButtons()
yellow_button = buttons.yellow_button
onboard_led = ThisPico.onboard_led

for i in range(2):
    if yellow_button.wait(10, onboard_led):
        print (yellow_button.name, 'pressed')

print ('Finished')