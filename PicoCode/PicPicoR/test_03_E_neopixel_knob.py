module_name = 'test_03_E_neopixel_knob.py'

import PicoA_v16 as PicoA
import utime

print (module_name, 'starting')

my_headlight = PicoA.ThisRunningLights()
my_knob = PicoA.ThisKnob()

my_headlight.clear()
utime.sleep(0.5)

old_pos = 999

for i in range(9000):
    pos = my_knob.get()
    if pos != old_pos:
        print ('new', pos)
        old_pos = pos
        if pos < 1:
            my_headlight.all_off()
        elif pos < 2:
            my_headlight.rims_off()
            my_headlight.centres_on()
            my_headlight.blues_off()
        elif pos < 3:
            my_headlight.rims_on()
            my_headlight.centres_on()
            my_headlight.blues_off()
        elif pos < 4:
            my_headlight.rims_orange()
            my_headlight.centres_on()
            my_headlight.blues_off()
        else:
            my_headlight.rims_orange()
            my_headlight.centres_on()
            my_headlight.blues_blue()
        my_headlight.show()
    utime.sleep_ms(1)

my_headlight.close()
my_knob.close()

print (module_name, 'finished')
