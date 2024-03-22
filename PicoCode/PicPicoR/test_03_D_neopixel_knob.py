module_name = 'test_03_D_neopixel_knob.py'

import ThisPico_Q_V32 as ThisPico
import utime

print (module_name, 'starting')

my_headlight = ThisPico.ThisHeadlight()
my_knob = ThisPico.ThisKnob()

my_headlight.clear()
utime.sleep(0.1)

for i in range(50):
    diff = my_knob.get()
    my_headlight.set_sector_to_pattern('front_left_rim', 'mixed', diff)
    my_headlight.show()
    utime.sleep(0.2)

my_headlight.close()
my_knob.close()

print (module_name, 'finished')
