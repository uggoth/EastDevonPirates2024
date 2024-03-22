module_name = 'test_18_C_joystick_v02.py'

import ThisPico_F_v08 as ThisPico
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrain()
my_remote = ThisPico.ThisRemoteControl(my_drive_train)

throttle = my_remote.left_up_down
steering = my_remote.right_sideways
knob = my_remote.knob

joysticks = [throttle, steering, knob]

for joystick in joysticks:
    print ('testing', joystick)
    previous = 999
    for i in range(20):
        utime.sleep_ms(500)
        value = joystick.get()
        if ((value is not None) and (value != previous)):
            print (joystick, value)
            previous = value
    joystick.close()

print (module_name, 'finished')
