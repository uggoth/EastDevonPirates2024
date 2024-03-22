#  test_01_G_PIO_read_PWM_v02.py

import utime
import rp2
from machine import Pin

@rp2.asm_pio()
def measure():
    wrap_target()
    wait(0,pin,0)  #  don't start in the middle of a pulse
    wait(1,pin,0)
    mov(x,invert(null))
    label('loop')    
    jmp(x_dec,'pin_on') #  Note: x will never be zero. We just want the decrement
    nop()  
    label('pin_on')
    jmp(pin, 'loop')
    mov(isr,invert(x))
    push(noblock)
    wrap()

sm_hertz = 100000  #  with my radio gives 50 to 100 range for pulse width

sm0_start_pin = Pin(4, Pin.IN, Pin.PULL_DOWN)
sm0 = rp2.StateMachine(0, measure, freq=sm_hertz, in_base=sm0_start_pin, jmp_pin=sm0_start_pin)

sm1_start_pin = Pin(5, Pin.IN, Pin.PULL_DOWN)
sm1 = rp2.StateMachine(1, measure, freq=sm_hertz, in_base=sm1_start_pin, jmp_pin=sm1_start_pin)

sm_list = [sm0,sm1]
previous_list = []

for i in range(len(sm_list)):
    sm_list[i].active(1)
    previous_list.append(99999)

for i in range(100):  #  arbitrary test duration
    utime.sleep_ms(100)
    for i in range(len(sm_list)):
        sm = sm_list[i]
        if sm.rx_fifo():
            y = sm.get()
            if y != previous_list[i]:
                print ('sm',i,y)
                previous_list[i] = y

for sm in sm_list:
    sm.active(0)
