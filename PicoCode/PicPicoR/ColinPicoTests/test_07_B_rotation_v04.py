module_name = 'test_07_B_rotation_v04.py'
#  run on stand to check rotation

import ThisPico_F_v09 as ThisPico
import utime

print (module_name, 'starting')

my_drive_train = ThisPico.ThisDriveTrain()
print (my_drive_train)
print (my_drive_train.left_side)
print (my_drive_train.left_side.my_motors)
print (my_drive_train.right_side)
utime.sleep(1)

speed = 50

print ('Forwards')
my_drive_train.fwd(50,150)

print ('Reverse')
my_drive_train.rev(50,150)

print ('Spin Left')
my_drive_train.spl(50,150)

print ('Spin Right')
my_drive_train.spr(50,150)

my_drive_train.close()
print (module_name, 'finished')
