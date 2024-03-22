module_name = 'test_18_SBUS_B_v02.py'
module_description = 'Calibrating joysticks. Part 1'
print (module_name, 'starting')

import sbus_receiver_3 as sbus_receiver
import machine
import utime
import ColObjects_V14 as ColObjects

tx_pin_no = 0
rx_pin_no = 1
uart_no = 0
baud_rate = 100000
uart = machine.UART(uart_no, baud_rate, tx = machine.Pin(tx_pin_no), rx = machine.Pin(rx_pin_no), bits=8, parity=0, stop=2)
my_sbus = sbus_receiver.SBUSReceiver(uart)

throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [100, 201, 900, 1090, 1801, 2000], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 693, 1080, 1120, 1500, 2000], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
interval = 800

for i in range(20000):
    utime.sleep_us(300)
    my_sbus.get_new_data()
    if i%interval == 0:
        joysticks = my_sbus.get_rx_channels()[0:5]
        steering_raw = joysticks[0]
        if steering_raw < 15:
            continue
        throttle_raw = joysticks[2]
        throttle_value = throttle_interpolator.interpolate(throttle_raw)
        steering_value = steering_interpolator.interpolate(steering_raw)
        print ('{:9.1f}{:9.1f}{:13.1f}{:9.1f}'.format(throttle_raw, throttle_value, steering_raw, steering_value))

print (module_name, 'finished')