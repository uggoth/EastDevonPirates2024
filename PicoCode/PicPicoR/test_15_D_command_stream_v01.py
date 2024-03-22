module_name = 'test_15_D_command_stream_v01.py'
print (module_name, 'starting')

import CommandStreamPico_V05 as CommandStream
import utime

my_stream = CommandStream.CommandStream()

print ('*** Close Thonny and start sender on Pi ***')
utime.sleep(9)

logging = open('test_15_D.txt','w')

for i in range(10000):
    utime.sleep_ms(1)
    message = my_stream.get()
    if message:
        logging.write(message)
        if 'WHOU' == message[0:4]:
            my_stream.send('PICOA')
            logging.write('WHOU')