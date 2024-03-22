module_name = 'test_07_C_sides_v03.py'

import ThisPico_F_v07 as ThisPico
import utime

print (module_name, 'starting')

speed = 55

drive_train = ThisPico.ThisDriveTrain()

drive_train.left_side.fwd(speed)
utime.sleep(1)
drive_train.left_side.stop()

utime.sleep(2)

drive_train.right_side.fwd(speed)
utime.sleep(1)
drive_train.right_side.stop()

print (module_name, 'finished')
