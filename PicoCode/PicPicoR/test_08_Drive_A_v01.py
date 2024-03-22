module_name = 'test_08_Drive_A_v01.py'

import ThisPico_R_V36 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_drive_train = ThisPico.ThisDriveTrainWithHeadlights()
print ('--- AFTER INSTANTIATION --')
print (ColObjects.ColObj.str_allocated())

def runit(speed, steering, duration=2):
    print ("{:4.0f}  {:4.0f}".format(speed, steering))
    my_drive_train.drive(speed, steering)
    utime.sleep(duration)
    my_drive_train.stop()
    utime.sleep(1)

print (" SPD   STR")
runit(50,0,2)
runit(-50,0,2)
runit(-100,0,2)
runit(0,0,2)
runit(100,0,2)
runit(10,0,2)

my_drive_train.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
