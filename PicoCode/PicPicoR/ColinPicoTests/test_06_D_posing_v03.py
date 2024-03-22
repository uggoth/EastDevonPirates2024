# Posing Test and Setup

import ThisPico_D_v12 as ThisPico
import utime

module_name = 'test_06_D_posing_v03.py'

print (module_name, "starting")

board_object = ThisPico.Kitronik.Kitronik('The Only Board')
my_arm = ThisPico.ThisArm(board_object)
#my_arm.poses['PARK'] = [[my_arm.shoulder_servo,90],[my_arm.bucket_servo,90]]
#my_arm.poses['UP'] = [[my_arm.shoulder_servo,100],[my_arm.bucket_servo,110]]
#my_arm.poses['DUMP'] = [[my_arm.shoulder_servo,90],[my_arm.bucket_servo,155]]
#my_arm.poses['CARRY'] = [[my_arm.shoulder_servo,90],[my_arm.bucket_servo,1]]
#my_arm.poses['DOWN'] = [[my_arm.shoulder_servo,165],[my_arm.bucket_servo,10]]
#my_arm.poses['SCOOP'] = [[my_arm.shoulder_servo,160],[my_arm.bucket_servo,1]]

def do_pose(pose_id, speed):
    print (pose_id)
    my_arm.do_pose(pose_id, speed)

speed=100
do_pose('PARK', speed)
utime.sleep(1)
#do_pose('DOWN', speed)
#utime.sleep(1)
#do_pose('SCOOP', speed)
#utime.sleep(3)
do_pose('CARRY', speed)
utime.sleep(3)
#do_pose('DUMP', speed)
#utime.sleep(3)
do_pose('PARK', speed)
utime.sleep(1)

my_arm.close()
board_object.close()

print (module_name, "finished")
