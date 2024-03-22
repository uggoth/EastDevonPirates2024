module_name = 'stop_all_motors_obj.py'
print (module_name)

import ThisPico_R_V38 as ThisPico
import utime

my_drive_train = ThisPico.ThisDriveTrainWithHeadlights()
my_drive_train.stop()
my_drive_train.close()

obled = ThisPico.ThisOnboardLED()

for i in range(25):
    obled.on()
    utime.sleep(0.25)
    obled.off()
    utime.sleep(0.15)

print ("Finished")