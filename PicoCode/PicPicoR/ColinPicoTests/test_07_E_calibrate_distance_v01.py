import ThisPico_F_v07 as ThisPico
import utime

my_drive_train = ThisPico.ThisDriveTrain()

my_drive_train.fwd(speed=50, millimetres=100)
utime.sleep(2)
my_drive_train.rev(speed=50, millimetres=100)
