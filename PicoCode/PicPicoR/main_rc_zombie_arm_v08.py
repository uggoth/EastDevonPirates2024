module_title = 'main_rc_zombie_arm'
module_name = module_title + '_v08.py'
print (module_name, 'starting')

import ThisPico_R_V39 as ThisPico
my_drive_train = ThisPico.ThisDriveTrainWithHeadlights()
my_mixer = my_drive_train.mixer
motor_lf = my_drive_train.motor_lf
motor_lb = my_drive_train.motor_lb
motor_rf = my_drive_train.motor_rf
motor_rb = my_drive_train.motor_rb

motor_list = [motor_lf, motor_lb, motor_rf, motor_rb]

for motor in motor_list:
    motor.stop()

ColObjects = ThisPico.ColObjects
my_pico = ThisPico.ThisPico()
my_name = my_pico.name
my_description = my_pico.description
my_receiver = ThisPico.ThisSbusReceiver()
import CommandStreamPico_V05 as CommandStream
import utime
import sys

mecanum_switch = ThisPico.ThisDIP_1()
my_stream = ThisPico.ThisCommandStream()

uart_no = 0
tx_pin_no = 0
rx_pin_no = 1
baud_rate = 100000
no_attempts = 100
receiver_found = False
for i in range(no_attempts):
    utime.sleep_us(300)
    channel_values = my_receiver.get()
    if channel_values[0] < 15:  #  ignore bad values
        continue
    else:
        receiver_found = True
        break

if receiver_found:
    print ('*** Close Thonny and start  ',module_title,'  on the Pi ***')
else:
    print ('******** Could not open ',my_receiver.name,'receiver ***************')
    sys.exit(1)
logging = open(module_name + '.txt','w')
logging.write(module_name + ' starting\n\n')

i = 0
motor_interval = 10
command_interval = 20
exiting = False
#finished = False

while True:
#    if finished:
#        break
    i += 1
    utime.sleep_us(300)
    channel_values = my_receiver.get()
    if channel_values[0] < 15:  #  ignore bad values
        continue
    if (((i % motor_interval) == 0) and not exiting):
        switch_raw = channel_values[4]
        switch_in = my_receiver.switch_interpolator.interpolate(switch_raw)
        if switch_in < 0:
            logging.write ('STOPPING')
            exiting = True
            motor_lf.run(0)
            motor_rf.run(0)
            motor_lb.run(0)
            motor_rb.run(0)
            continue
        spin_raw = channel_values[1]
        spin_in = my_receiver.spin_interpolator.interpolate(spin_raw)
        fore_and_aft_raw = channel_values[2]
        fore_and_aft_in = my_receiver.fore_and_aft_interpolator.interpolate(fore_and_aft_raw)
        if mecanum_switch.get() == 'ON':
            crab_raw = channel_values[3]
            crab_in = my_receiver.crab_interpolator.interpolate(crab_raw)
        else:
            crab_in = 0
        if switch_in > 0:
            temp = crab_in
            crab_in = -spin_in
            spin_in = -temp
        lf_level, rf_level, lb_level, rb_level = my_mixer.mix(spin_in, fore_and_aft_in, crab_in)
        #print (lf_level, rf_level, lb_level, rb_level)
        motor_lf.run(-lf_level)
        motor_rf.run(rf_level)
        motor_lb.run(-lb_level)
        motor_rb.run(rb_level)
        
    if ((i % command_interval) == 0):
        my_stream.ready()
        utime.sleep_ms(1)
        message = my_stream.get()
        if message:
            my_stream.not_ready()
            serial_no = message[0:4]
            command = message[4:8]
            if command == 'WHOU':
                my_stream.send('0000OKOK' + my_name)
                logging.write('Command WHOU\n')
            elif command == 'SBUS':
                if exiting:
                    feedback = 'EXIT'
                    finished = True
                else:
                    feedback = 'OKOK'
                response = serial_no + feedback
                for channel_value in channel_values:
                    channel_string = '{:04.0f}'.format(channel_value)
                    response += channel_string
                my_stream.send(response)
            elif command == 'EXIT':
                my_stream.send('9999OKOK')
                logging.write('Command EXIT\n\n')
                break
            else:
                my_stream.send('BADC Only understand WHOU and EXIT')
                logging.write('Command not WHOU, EXIT\n')

utime.sleep_ms(1)
my_stream.not_ready()
utime.sleep_ms(1)
my_stream.send('9999EXIT')
if my_handshake is not None:
    my_handshake.close()
my_stream.close()

logging.write(module_name + ' finished\n\n')
logging.close()
