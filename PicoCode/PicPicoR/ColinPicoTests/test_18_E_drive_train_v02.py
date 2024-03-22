module_name = 'test_18_E_drive_train_v02.py'

import ThisPico_F_v08 as ThisPico
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrain()
my_drive_train.fwd(95,200)
my_drive_train.stop()
my_drive_train.rev(95,200)

utime.sleep_ms(100)
my_drive_train.close()

print (module_name, 'finished')
