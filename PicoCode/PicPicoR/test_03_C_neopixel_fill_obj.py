module_name = 'test_03_C_neopixel_fill_obj.py'

import ThisPico_Q_V32 as ThisPico
import utime

print (module_name, 'starting')

my_headlight = ThisPico.ThisHeadlight()

my_headlight.fill_sector('front_left_centre','blue')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.fill_sector('front_right_rim','red')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.pixels[8:14] = my_headlight.colours['green']
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.close()
print (module_name, 'finishing')
