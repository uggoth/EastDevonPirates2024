import ThisPico_F_v09 as ThisPico
import utime

module_name = 'test_06_C_shoulder_and_bucket_v02.py'

print (module_name, "starting")

bucket_servo = ThisPico.ThisBucketServo()
shoulder_servo = ThisPico.ThisShoulderServo()

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

print (module_name, "finished")
