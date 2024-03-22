import PicoBotF_v03 as ThisPico
import utime

module_name = 'test_06_B_shoulder_v02.py'

print (module_name, "starting")

test_servo = ThisPico.ThisShoulderServo()

my_speed = 35
test_servo.move_to(new_position=80, speed=my_speed)
utime.sleep(1)
test_servo.move_to(new_position=90, speed=my_speed)
utime.sleep(1)
test_servo.move_to(new_position=155, speed=my_speed)
utime.sleep(1)
test_servo.move_to(new_position=90, speed=my_speed)
utime.sleep(1)

print (module_name, "finished")
