module_name = 'main_led_flash.py'
import machine
import utime

print (module_name,'starting')

print ('rp2-pico-w-20221108-unstable-v1.19.1-617-g43dd3ea74.uf2')

led = machine.Pin('LED', machine.Pin.OUT)

for i in range(50):
    led.on()
    utime.sleep_ms(100)
    led.off()
    utime.sleep_ms(30)

print (module_name,'finished')
