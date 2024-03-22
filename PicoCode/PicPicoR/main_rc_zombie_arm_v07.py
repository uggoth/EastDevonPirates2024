module_name = 'main_rc_zombie_arm_v07.py'
print (module_name, 'starting')

import ThisPico_R_V39 as ThisPico
my_drive_train = ThisPico.ThisDriveTrainWithHeadlights()
my_drive_train.stop()
import utime
my_stream = ThisPico.ThisCommandStream()
my_handshake = my_stream.handshake
my_headlight = my_drive_train.headlight
my_dip_1 = ThisPico.ThisDIP_1()

logging = open(module_name + '.txt','w')

def log_send(message):
    logging.write('Sending: ' + message + '\n')
    my_stream.send(message)

logging.write(module_name + ' starting' + '\n\n')

print ('*** Close Thonny and start sender on Pi ***')

testing = True
if testing:
    spin = 0
    fore_and_aft = 50
    crab = 0
    my_drive_train.drive(spin, fore_and_aft, crab)
    utime.sleep(1)
    my_drive_train.stop()

for i in range(100000):
    my_stream.ready()
    utime.sleep_ms(1)
    message = my_stream.get()
    if message:
        my_stream.not_ready()
        logging.write('Received: ' + message + '\n')
        serial_no = message[0:4]
        command = message[4:8]
        if command == 'WHOU':
            log_send(serial_no + 'OKOK' + 'PICOR')
        elif command == 'DRIV':
            fore_and_aft = int(message[8:12])
            spin = int(message[12:16])
            if my_dip_1.get() == 'ON':
                crab = int(message[16:20])
            else:
                crab = 0
            log_send(serial_no + 'OKOK')
            logging.write('spin: {:}, fore_and_aft: {:}, crab: {:}'.format(spin, fore_and_aft, crab))
            my_drive_train.drive(spin, fore_and_aft, crab)
        elif command == 'HREV':
            log_send(serial_no + 'OKOK')
            my_headlight.rev()
        elif command == 'HFWD':
            log_send(serial_no + 'OKOK')
            my_headlight.fwd()
        elif command == 'HOFF':
            log_send(serial_no + 'OKOK')
            my_headlight.off()
        elif command == 'EXIT':
            log_send(serial_no + 'OKOK')
            break
        else:
            log_send(serial_no + 'BADC')

if my_handshake is not None:
    my_handshake.close()
my_stream.close()
my_headlight.close()
logging.write('Exiting')
logging.close()
print (module_name, 'finished')