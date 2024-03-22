module_name = 'test_18_SBUS_D_v03.py'
print (module_name)

import utime
import _thread
import sbus_receiver_3 as sbus_receiver
import ColObjects_V14 as ColObjects

tx_pin_no = 0
rx_pin_no = 1
uart_no = 0
baud_rate = 100000
uart = machine.UART(uart_no, baud_rate, tx = machine.Pin(tx_pin_no), rx = machine.Pin(rx_pin_no), bits=8, parity=0, stop=2)
my_sbus = sbus_receiver.SBUSReceiver(uart)

throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [100, 201, 1000, 1090, 1801, 2000], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 393, 1180, 1220, 1990, 2000], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])

def thread_1_code():
    global joystick_raws, thread_enable
    while True:
        if not thread_enable:
            break
        utime.sleep_us(300)
        my_sbus.get_new_data()
        joystick_raws = my_sbus.get_rx_channels()[0:5]
    print ('thread ending')

joystick_raws = []
thread_enable = True

thread_1 = _thread.start_new_thread(thread_1_code, ())

for i in range(9):
    utime.sleep(1)
    throttle_value = throttle_interpolator.interpolate(joystick_raws[2])
    steering_value = steering_interpolator.interpolate(joystick_raws[0])
    print('{:9.1f}{:9.1f}'.format(throttle_value,steering_value))

thread_enable = False
utime.sleep(1)
print (module_name, 'finished')