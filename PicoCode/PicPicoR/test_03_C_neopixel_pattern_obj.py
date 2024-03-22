module_name = 'test_03_C_neopixel_pattern_obj.py'

import ThisPico_R_V38 as ThisPico
import utime

print (module_name, 'starting')

my_headlight = ThisPico.ThisHeadlight()
utime.sleep_ms(100)
my_headlight.set_sector_to_pattern('front_left_rim','mixed')
my_headlight.show()
utime.sleep_ms(1500)
my_headlight.clear()
utime.sleep_ms(500)
my_headlight.set_sector_to_pattern('front_right_rim','mixed')
my_headlight.show()
utime.sleep_ms(1500)
my_headlight.close()
print (module_name, 'finishing')
