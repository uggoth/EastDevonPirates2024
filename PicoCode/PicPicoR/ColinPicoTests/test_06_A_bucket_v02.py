import ThisPico_F_v11 as ThisPico
import utime

module_name = 'test_06_A_bucket_v02.py'

print (module_name, "starting")

my_board = ThisPico.Kitronik.Kitronik('The Only Board')
bucket_servo = ThisPico.ThisBucketServo(my_board)

my_speed = 35
bucket_servo.move_to(new_position=90, speed=my_speed)
utime.sleep(1)
bucket_servo.move_to(new_position=100, speed=my_speed)
utime.sleep(3)
bucket_servo.move_to(new_position=90, speed=my_speed)

bucket_servo.close()
my_board.close()

print (module_name, "finished")
