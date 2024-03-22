module_name = 'test_08_Drive_A_v02.py'

import ThisPico_R_V39 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_drive_train = ThisPico.ThisDriveTrainWithHeadlights()
print ('--- AFTER INSTANTIATION --')
print (ColObjects.ColObj.str_allocated())

def runit(fore_and_aft, spin, duration=2):
    print ("{:4.0f}  {:4.0f}".format(fore_and_aft, spin))
    my_drive_train.drive(fore_and_aft, spin, 0)  #  assume no mecanum
    utime.sleep(duration)
    my_drive_train.stop()
    utime.sleep(1)

print (" F&A   SPN")
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
