module_name = 'test_19_Kitronik_v01.py'

import GPIOPico_v22 as GPIO
ColObjects = GPIO.ColObjects
import PicoRobotics
import math
import utime

class Kitronik(ColObjects.ColObj):
    allocated = False
    def __init__(self, name):
        if Kitronik.allocated:
            raise ColObjects.ColError('Can only have one Kitronik instance')
        Kitronik.allocated = True
        super().__init__(name)
        self.board = PicoRobotics.KitronikPicoRobotics()
        self.sda = GPIO.Reserved('Kitronik SDA', 'CONTROL', 8)
        self.scl = GPIO.Reserved('Kitronik SCL', 'CONTROL', 9)
        self.last_servo = 8
        self.free_code = 'FREE'
        self.servo_list = [self.free_code]*(self.last_servo + 1)
        self.servo_list[0] = 'NOT_USED'
        self.last_motor = 4
        self.motor_list = [self.free_code]*(self.last_motor + 1)
        self.motor_list[0] = 'NOT_USED'
    def str_servo_list(self):
        output = ''
        for i in range(1,len(self.servo_list)):
            output += str(i) + '  ' + self.servo_list[i] + '\n'
        return output
    def str_motor_list(self):
        output = ''
        for i in range(1,len(self.motor_list)):
            output += str(i) + '  ' + self.motor_list[i] + '\n'
        return output
    def close(self):
        self.sda.close()
        self.scl.close()
        self.board.swReset()
        Kitronik.allocated = False

print (module_name, 'starting')

board = Kitronik('b1')
#board2 = Kitronik('b2')
utime.sleep_ms(100)
print (GPIO.GPIO.str_allocated())
board.close()
print (GPIO.GPIO.str_allocated())
board2 = Kitronik('b3')
print (board2.str_motor_list())
print (board2.str_servo_list())
print (module_name, 'finished')
