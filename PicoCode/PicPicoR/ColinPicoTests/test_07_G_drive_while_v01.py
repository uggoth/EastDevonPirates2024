module_name = 'test_07_G_drive_while_v01.py'

import ThisPico_D_v13 as ThisPico
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrainPlus()
my_rear_centre_ir = my_drive_train.rear_left_ir
my_front_left_ir = my_drive_train.front_left_ir

throttle_value = -50
steering_value = 0

sub_result = my_drive_train.drive_while(throttle_value, steering_value,
                            [[my_rear_centre_ir, 'OFF'],[my_front_left_ir, 'ON']])
print (sub_result)

my_drive_train.stop()
my_drive_train.close()

print (module_name, 'finished')
