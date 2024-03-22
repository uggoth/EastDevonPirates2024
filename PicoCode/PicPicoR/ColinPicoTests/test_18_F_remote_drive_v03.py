module_name = 'test_18_F_remote_drive_v02.py'

import ThisPico_F_v08 as ThisPico
GPIOPico = ThisPico.GPIO
ColObjects = GPIOPico.ColObjects
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrain()
my_remote_control = ThisPico.ThisRemoteControl(my_drive_train)
utime.sleep_ms(9)
throttle = my_remote_control.left_up_down
print ('After Allocate')
print (ColObjects.ColObj.str_allocated())

for i in range(1000):
    utime.sleep_ms(10)
    my_remote_control.drive()

my_remote_control.stop()

utime.sleep_ms(9)
my_remote_control.close()

print ('After Close')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')