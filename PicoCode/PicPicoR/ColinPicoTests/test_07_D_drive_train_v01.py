import ThisPico_F_v10 as ThisPico
import utime

board_object = ThisPico.Kitronik.Kitronik('The Only Board')
my_drive_train = ThisPico.ThisDriveTrain(board_object)

speed = 45
millimetres = 50
sleep_time = 1.0
my_drive_train.fwd(speed,millimetres)
utime.sleep(sleep_time)
my_drive_train.rev(speed,millimetres)
utime.sleep(sleep_time)

speed = 45
degrees = 25
my_drive_train.spl(speed,degrees)
utime.sleep(sleep_time)
my_drive_train.spr(speed,degrees)
utime.sleep(sleep_time)

my_drive_train.stop()
my_drive_train.close()
board_object.close()
