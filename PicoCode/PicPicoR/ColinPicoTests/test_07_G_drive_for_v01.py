module_name = 'test_07_G_drive_for_v01.py'

import ThisPico_D_v13 as ThisPico
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrainPlus()

throttle_value = -50
steering_value = 0
milliseconds=1000

sub_result = my_drive_train.drive_for(throttle_value, steering_value, milliseconds)
print (sub_result)

my_drive_train.stop()
my_drive_train.close()

print (module_name, 'finished')
