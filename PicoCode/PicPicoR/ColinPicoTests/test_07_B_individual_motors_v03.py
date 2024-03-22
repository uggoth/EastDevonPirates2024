module_name = 'test_07_B_individual_motors_v03.py'
#  run on stand to check rotation speed

import Kitronik_v08 as Kitronik
import utime

print (module_name, 'starting')

utime.sleep(1)

# when correct, copy info to ThisPico.ThisDriveTrain
motors = [Kitronik.KitronikMotor('FRONT_LEFT', Kitronik.board, 4),
          Kitronik.KitronikMotor('REAR_LEFT', Kitronik.board, 1),
          Kitronik.KitronikMotor('FRONT_RIGHT', Kitronik.board, 3),
          Kitronik.KitronikMotor('REAR_RIGHT', Kitronik.board, 2)]

speed = 50

print ('Rotation should be clockwise')
for motor in motors:
    print (motor.name)
    motor.clk(speed)
    utime.sleep(2)
    motor.stop()
    utime.sleep(1)

print ('Rotation should be anticlockwise')
for motor in motors:
    print (motor.name)
    motor.anti(speed)
    utime.sleep(2)
    motor.stop()
    utime.sleep(1)

for motor in motors:
    motor.close()
print (module_name, 'finished')
