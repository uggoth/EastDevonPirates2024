module_name = 'test_06_A_servo_posing_v01.py'

import Kitronik_v13 as Kitronik
import utime

my_board = Kitronik.Kitronik('Only Board')
servo_no = 5
up_position = 110
down_position = 75
park_position = 90

delay = 3000
speed = 0

lift_servo = Kitronik.Servo('Lift Servo', my_board, servo_no, up_position, down_position)
lift_servo.move_to(park_position, speed=speed)
utime.sleep_ms(delay)
lift_servo.move_to(down_position, speed=speed)
utime.sleep_ms(delay)
lift_servo.move_to(up_position, speed=speed)
utime.sleep_ms(delay)
lift_servo.move_to(park_position, speed=speed)
utime.sleep_ms(delay)

lift_servo.close()
my_board.close()
