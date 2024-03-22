program_name = 'test_08_FIT0441_A_v03.py'
description = 'test basic movement'

print (program_name, 'starting')

import machine
import utime

#  speed, pulse, direction
motors = {'Left Front':[21,20,19],
          'Right Front':[10,11,12],
          'Right Back':[6,7,8],
          'Left Back':[2,3,4]}

def identify(which_motor):
    print (which_motor)

    speed_pin_no = motors[which_motor][0]
    direction_pin_no = motors[which_motor][2]

    speed_pin = machine.PWM(machine.Pin(speed_pin_no))
    speed_pin.freq(25000)
    direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)

    print ('anticlockwise')
    direction_pin.off()
    speed_pin.duty_u16(16000)
    utime.sleep(2)
    speed_pin.duty_u16(65535)
    utime.sleep(1)

    print ('clockwise')
    direction_pin.on()
    speed_pin.duty_u16(16000)
    utime.sleep(2)
    speed_pin.duty_u16(65535)

identify('Left Front')
identify('Right Front')
identify('Right Back')
identify('Left Back')

print (program_name, 'finished')

