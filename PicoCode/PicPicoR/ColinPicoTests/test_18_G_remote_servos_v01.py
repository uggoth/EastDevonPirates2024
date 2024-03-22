module_name = 'test_18_G_remote_servos_v01.py'

import ThisPico_F_v10 as ThisPico
import utime

print (module_name, 'starting')

board_object = ThisPico.Kitronik.Kitronik('The Only Board')
my_drive_train = ThisPico.ThisDriveTrain(board_object)
my_remote_control = ThisPico.ThisRemoteControl(my_drive_train)
utime.sleep_ms(9)
my_arm = ThisPico.ThisArm(board_object)
my_knob = my_remote_control.knob

def get_pose(position):
    if position < -50:
        return 'DOWN'
    elif position < 0:
        return 'SCOOP'
    elif position < 50:
        return 'CARRY'
    else:
        return 'DUMP'

previous_pose = 'UNKNOWN'

for i in range(1000):
    utime.sleep_ms(10)
    position = my_knob.get()
    pose = get_pose(position)
    if pose != previous_pose:
        previous_pose = pose
        my_arm.do_pose(pose)

my_knob.close()
my_arm.close()
my_remote_control.close()
my_drive_train.close()
board_object.close()

print (module_name, 'finished')
