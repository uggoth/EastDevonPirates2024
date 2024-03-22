module_name = 'main_driving_v01.py'
description = 'main program for remote control driving around'
import ThisPico_R_V34 as ThisPico
my_train = ThisPico.ThisDriveTrainWithHeadlights()
my_train.stop()
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
my_throttle = my_sbus.throttle
my_steering = my_sbus.steering
my_switch = my_sbus.switch
my_knob = my_sbus.knob

my_headlight = my_train.headlight
my_rear_light = ThisPico.ThisRearLight()
my_rear_light.fill_sector('rear_light_centre', 'red')
bad_gets = 0
max_bad_gets = 10000
throttle_value = 0
steering_value = 0
while True:
    throttle_value = my_throttle.get()
    steering_value = my_steering.get()
    switch_value = my_switch.get()
    if switch_value is not None:
        if switch_value < 0:
            break
    knob_value= my_knob.get()
    if throttle_value is None:
        bad_gets += 1
        if bad_gets < max_bad_gets:
            continue
        else:
            break
    else:
        my_train.drive(throttle_value, steering_value)
    utime.sleep_ms(10)

print (bad_gets,'bad gets')

my_headlight.off()
my_rear_light.fill_sector('rear_light_centre', 'blue')
my_train.stop()
my_train.close()
my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
