module_name = 'main_test_command_stream_A_v01.py'
print (module_name, 'starting')

import ThisPico_R_V36 as ThisPico
import CommandStreamPico_V05 as CommandStream
import utime

my_handshake = ThisPico.ThisHandshake()
#my_handshake = None
my_stream = CommandStream.CommandStream('From Pi', my_handshake)
my_headlight = ThisPico.ThisHeadlight()

print ('*** Close Thonny and start sender on Pi ***')
utime.sleep(9)

logging = open('main_test_command_stream_A.txt','w')

def log_send(message):
    logging.write('Sending: ' + message + '\n')
    my_stream.send(message)

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
            log_send(serial_no + 'PICOR')
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