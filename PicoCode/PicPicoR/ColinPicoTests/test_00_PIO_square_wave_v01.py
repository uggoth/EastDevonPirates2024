module_name = 'test_00_PIO_square_wave_v01.py'

import time
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def square():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

square_wave_frequency = 5000

sm = rp2.StateMachine(0, square, freq=square_wave_frequency*2, set_base=Pin(16))

sm.active(1)
time.sleep(39)
sm.active(0)