import ThisPico_D_v13 as ThisPico
import utime

module_name = 'test_01_B_IR_Sensors_v01.py'

print (module_name, "starting")

my_ids = ThisPico.GPIO.GPIO.ids

def ir_callback(my_pin):
    my_pin.irq(None)
    print (my_ids[id(my_pin)], my_pin.value())
    utime.sleep_ms(1500)  #  debounce
    my_pin.irq(ir_callback)

my_irs = ThisPico.TheseIRSensors(ir_callback,ir_callback)

print (my_ids)

for sensor in my_irs.ir_list:
    sensor.previous = 'UNKNOWN'
    sensor.pin.irq(ir_callback)

for i in range(1900):
    utime.sleep(0.01)

print (module_name, "finished")
