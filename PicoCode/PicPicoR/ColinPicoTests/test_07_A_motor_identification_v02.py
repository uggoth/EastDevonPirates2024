module_name = 'test_07_A_motor_identification_v01.py'
#  run on stand to check rotation speed

import Kitronik_v12 as Kitronik
import utime

print (module_name, 'starting')

utime.sleep(1)

board_object = Kitronik.Kitronik('The Only Board')
# when correct, copy info to ThisPico.ThisDriveTrain
motors = [Kitronik.KitronikMotor('LEFT', board_object, 1),
          Kitronik.KitronikMotor('RIGHT', board_object, 2)]

speed = 50

for motor in motors:
    print (motor.name)
    motor.clk(speed)
    utime.sleep(2)
    motor.stop()
    utime.sleep(1)

for motor in motors:
    motor.close()

print (module_name, 'finished')
