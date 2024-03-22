module_name = 'test_18_A_radio_control_v02.py'

import RemoteControl_v15 as RemoteControl
import utime

print (module_name, 'starting')

tsm3 = RemoteControl.StateMachine(name='Throttle SM', code='MEASURE', pin_no=3)
tsm4 = RemoteControl.StateMachine(name='Aileron SM', code='MEASURE', pin_no=4)
tsm5 = RemoteControl.StateMachine(name='Flap SM', code='MEASURE', pin_no=5)

int_standard = RemoteControl.Interpolator('Standard Interpolator', [40, 50, 74, 76, 100, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])

int_t = RemoteControl.Interpolator('Throttle Interpolator', [40, 50, 70, 73, 96, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
int_s = RemoteControl.Interpolator('Steering Interpolator', [40, 56, 74, 76, 93, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
int_k = RemoteControl.Interpolator('Knob Interpolator', [40, 50, 74, 76, 101, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])

my_throttle = RemoteControl.Joystick('Throttle', tsm3)
my_steering = RemoteControl.Joystick('Steering', tsm4)
my_knob = RemoteControl.Joystick('Knob', tsm5)

my_sticks = [my_throttle, my_steering, my_knob]
print ('------- NO interpolation ----------')
for i in range(30):
    utime.sleep_ms(500)
    output = ''
    for stick in my_sticks:
        output += "{:}: {:3}   ".format(str(stick), int(stick.get()))
    print (output)

for stick in my_sticks:
    stick.close()
    
my_throttle = RemoteControl.Joystick('IThrottle', tsm3, int_t)
my_steering = RemoteControl.Joystick('ISteering', tsm4, int_s)
my_knob = RemoteControl.Joystick('IKnob', tsm5, int_k)

my_sticks = [my_throttle, my_steering, my_knob]
print ('------- WITH interpolation ----------')
for i in range(40):
    utime.sleep_ms(500)
    output = ''
    for stick in my_sticks:
        output += "{:}: {:3}   ".format(str(stick), int(stick.get()))
    print (output)

for stick in my_sticks:
    stick.close()
    
print (module_name, 'finished')
