import PicoBotF_v03 as ThisPico
import utime

module_name = 'test_06_E_shoulder_and_bucket_v02.py'

print (module_name, "starting")

bucket_servo = ThisPico.ThisBucketServo()
shoulder_servo = ThisPico.ThisShoulderServo()

def exercise():
    shoulder_servo.park()
    bucket_servo.park()
    utime.sleep(1)

    my_speed = 45
    shoulder_servo.up(my_speed)
    bucket_servo.up(my_speed)
    utime.sleep(3)

    shoulder_servo.down(my_speed)
    bucket_servo.down(my_speed)
    utime.sleep(3)

    shoulder_servo.park()
    bucket_servo.park()
    utime.sleep(1)

for i in range(8):
    exercise()

print (module_name, "finished")
