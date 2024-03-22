program_name = 'test_08_FIT0441_A_v01.py'
description = 'test basic movement'

print (program_name, 'starting')

import machine
import utime

speed_pin_no = 2
pulse_pin_no = 3
direction_pin_no = 4

speed_pin = machine.PWM(machine.Pin(speed_pin_no))
speed_pin.freq(25000)
pulse_pin = machine.Pin(pulse_pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)
direction_pin.off()

speed_pin.duty_u16(16000)
utime.sleep(1)
speed_pin.duty_u16(65535)
utime.sleep(1)
direction_pin.on()
speed_pin.duty_u16(16000)
utime.sleep(1)
speed_pin.duty_u16(65535)

print (program_name, 'finished')

