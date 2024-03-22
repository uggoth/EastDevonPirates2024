module_name = 'main_test_command_stream_B_v01.py'
print (module_name, 'starting')

import ThisPico_R_V36 as ThisPico
my_train = ThisPico.ThisDriveTrainWithHeadlights()
my_train.stop()
import CommandStreamPico_V05 as CommandStream
import utime

def array_abs(input):
    output_array = []
    for element in input:
        if element is None:
            output_array.append(0)
        else:
            output_array.append(abs(element))
    return output_array

def mix(inputs):
    logging.write('mix a\n\n')
    len_inputs = len(inputs)
    if ((len_inputs > 3) or (len_inputs < 2)):
        logging.write('mix error\n\n')
        raise ColObjects.ColError('Mixer must have inputs: spin, fore_and_aft, crab[optional]')
    for i in range(len_inputs):
        if inputs[i] is None:
            inputs[i] = 0
    inputs_abs = array_abs(inputs)
    biggest_in = max(inputs_abs)
    total_in = sum(inputs_abs)
    if total_in == 0:
        return 0,0,0,0
    logging.write('mix b\n\n')
    spin = inputs[0]
    fore_and_aft = inputs[1]
    fwd_levels = [fore_and_aft, fore_and_aft, fore_and_aft, fore_and_aft]
    spin_levels = [spin, -spin, spin, -spin]
    fwd_abs = array_abs(fwd_levels)
    spin_abs = array_abs(spin_levels)
    total_out = sum(fwd_abs) + sum(spin_abs)
    crab_levels = [0,0,0,0]
    if len_inputs == 3:
        crab = inputs[2]
        crab_levels = [crab, crab, -crab, -crab]
        crab_abs = array_abs(crab_levels)
        total_out = total_out + sum(crab_abs)
    ratio_a = 1.0
    lf_level = (fwd_levels[0] + spin_levels[0] + crab_levels[0]) * ratio_a
    rf_level = (fwd_levels[1] + spin_levels[1] - crab_levels[1]) * ratio_a
    lb_level = (fwd_levels[2] + spin_levels[2] + crab_levels[2]) * ratio_a
    rb_level = (fwd_levels[3] + spin_levels[3] - crab_levels[3]) * ratio_a
    output_abs = array_abs([lf_level, rf_level, lb_level, rb_level])
    biggest_out = max(output_abs)
    ratio_b = biggest_in / biggest_out
    lf_level = lf_level * ratio_b
    rf_level = rf_level * ratio_b
    lb_level = lb_level * ratio_b
    rb_level = rb_level * ratio_b
    return lf_level, rf_level, lb_level, rb_level

left_side = my_train.left_side
right_side = my_train.right_side

motor_rf = right_side.motor_rf
motor_rb = right_side.motor_rb
motor_lf = left_side.motor_lf
motor_lb = left_side.motor_lb

my_handshake = ThisPico.ThisHandshake()
#my_handshake = None
my_stream = CommandStream.CommandStream('From Pi', my_handshake)
my_headlight = my_train.headlight

logging = open(module_name + '.txt','w')

def log_send(message):
    logging.write('Sending: ' + message + '\n')
    my_stream.send(message)

logging.write(module_name + ' starting' + '\n\n')

print ('*** Close Thonny and start sender on Pi ***')

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
        elif command == 'DRIV':
            try:
                fore_and_aft = int(message[8:12])
                spin = int(message[12:16])
                crab = int(message[16:20])
                log_send(serial_no + 'OKOK')
            except:
                log_send(serial_no + 'BADC')
                continue
            logging.write('spin: {:}, fore_and_aft: {:}, crab: {:}'.format(spin, fore_and_aft, crab))
            lf_level, rf_level, lb_level, rb_level = mix([spin, fore_and_aft, crab])
            logging.write('running a\n')
            motor_lf.run(-lf_level)
            motor_rf.run(rf_level)
            motor_lb.run(-lb_level)
            motor_rb.run(rb_level)
            logging.write('running a\n')
            if sum([lf_level, lb_level]) > sum([rf_level, rb_level]):
                my_headlight.spr()
            elif sum([lf_level, lb_level]) < sum([rf_level, rb_level]):
                my_headlight.spl()
            elif sum([lf_level, rf_level, lb_level, rb_level]) >= 0:
                my_headlight.fwd()
            else:
                my_headlight.rev()
            logging.write('running b\n')
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