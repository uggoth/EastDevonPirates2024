module_name = 'test_01_C_buttons_irq_v02.py'

import ThisPico_D_v13 as ThisPico
GPIO = ThisPico.GPIO
import utime

print (module_name, 'starting')

def ir_callback(my_pin):
    my_pin.irq(None)
    print (my_ids[id(my_pin)], my_pin.value())
    utime.sleep_ms(500)  #  debounce
    my_pin.irq(ir_callback)

my_buttons = ThisPico.TheseButtons()
my_ids = ThisPico.GPIO.GPIO.ids

out_string = "\nList of all buttons:\n"
for button in GPIO.Button.button_list:
    out_string += '   ' + button.name + "\n"
print (out_string)

out_string = "List of TheseButtons:\n"
for button in my_buttons.button_list:
    button.previous = 'UNKNOWN'
    button.pin.irq(ir_callback)
    out_string += '   ' + button.name + "\n"
print (out_string)

for i in range(100):
    utime.sleep(0.1)

print (module_name, 'finished')
