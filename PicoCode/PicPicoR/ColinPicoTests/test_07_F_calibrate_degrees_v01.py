import ThisPico_F_v07 as ThisPico
import utime

my_drive_train = ThisPico.ThisDriveTrain()

my_drive_train.spr(speed=90,degrees=90)
utime.sleep(3)
my_drive_train.spl(speed=90,degrees=90)
