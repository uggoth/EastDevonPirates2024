module_prefix = 'main_a_s_a_d'
module_version = '20m'
module_name = module_prefix + '_v' + module_version + '.py'
import utime
start_time = int(utime.ticks_ms() / 1000)
print (module_name, 'starting at ', start_time)

import main_a_s_a_d_constants as constants
print ('This is', constants.PICO_NAME)
import array
import machine
import neopixel
#import _thread
import sys, select

class ColError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ColObj():
    
    allocated = {}
    free_code = 'FREE'
    
    def str_allocated():
        out_string = ('{:18}'.format('NAME') +
                        '{:18}'.format('OBJECT') + '\n')
        for name in sorted(ColObj.allocated):
            if ColObj.allocated[name] != ColObj.free_code:
                obj = ColObj.allocated[name]
                out_string += ('{:18}'.format(obj.name)  +
                                str(obj) + '\n')
        return out_string
    
    def __init__(self, name, description=''):
        self.name = name
        if name in ColObj.allocated:
            if ColObj.allocated[self.name] != ColObj.free_code:
                raise ColError(name + ' already allocated')
        ColObj.allocated[self.name] = self
        self.description = description
        
    def __str__(self):
        return self.name
    
    def close(self):
        ColObj.allocated[self.name] = ColObj.free_code

class CommandStream(ColObj):
    
    in_use = False
    
    def __init__(self, name, handshake_object):
        super().__init__(name, 'Command Stream from Pi')
        if CommandStream.in_use:
            self.valid = False
        else:
            CommandStream.in_use = True
            self.valid = True
        self.handshake_object = handshake_object
        
    def ready(self):
        if self.handshake_object is not None:
            self.handshake_object.set_on()

    def not_ready(self):
        if self.handshake_object is not None:
            self.handshake_object.set_off()

    def close(self):
        self.not_ready()
        CommandStream.in_use = False
        self.valid = False

    def get(self, delay=0.001):
        inputs, outputs, errors = select.select([sys.stdin],[],[],delay)
        if (len(inputs) > 0):
            result = sys.stdin.readline()
        else:
            result = False
        return result

    def get_command(self):
        self.ready()
        sub_result = self.get()
        self.not_ready()
        if not sub_result:
            return None, None, None
        if len(sub_result) < 8:
            return None, None, None
        serial_no = sub_result[0:4]
        command = sub_result[4:8]
        if len(sub_result) > 8:
            data = sub_result[8:]
        else:
            data = None
        return serial_no, command, data

    def send(self, message):
        print (message)
 
    def flush(self):
        no_inputs = 1
        while no_inputs > 0:
            inputs, outputs, errors = select.select([sys.stdin],[],[],0.001)
            if (len(inputs) > 0):
                result = sys.stdin.readline()
            else:
                break

class GPIO(ColObj):

    first_pin_no = 0
    last_pin_no = 29
    free_code = 'FREE'
    allocated = [free_code]*(last_pin_no + 1)
    ids = {}

    def allocate(pin_no, obj):
        if ((pin_no < GPIO.first_pin_no) or (pin_no > GPIO.last_pin_no)):
            raise ColError('pin no {} not in range {} to {}'.format(
                pin_no, GPIO.first_pin_no, GPIO.last_pin_no))
        if GPIO.allocated[pin_no] != GPIO.free_code:
            raise ColError('pin no {} already in use'.format(pin_no))
        GPIO.allocated[pin_no] = obj
        return True

    def deallocate(pin_no):
        GPIO.allocated[pin_no] = GPIO.free_code

    def str_allocated():
        out_string = ''
        for i in range(len(GPIO.allocated)):
            if GPIO.allocated[i] == GPIO.free_code:
                out_string += '{:02} : --FREE--'.format(i) + "\n"
            else:
                obj = GPIO.allocated[i]
                out_string += ('{:02}'.format(i) + ' : ' +
                                '{:18}'.format(obj.name) + "\n")
        return out_string
    
    def get_type_list(type_code):
        type_list = {}
        for obj in GPIO.allocated:
            if obj.type_code == type_code:
                type_list[obj.name] = obj
        return type_list

    valid_type_codes = {'INFRA_RED':'INPUT',
                        'BUTTON':'INPUT',
                        'BUZZER':'OUTPUT',
                        'US_TRIGGER':'OUTPUT',
                        'US_ECHO':'INPUT',
                        'SBUS':'INPUT',
                        'SWITCH':'INPUT',
                        'VOLTS':'INPUT',
                        'ADC':'INPUT',
                        'LED':'OUTPUT',
                        'CONTROL':'INPUT',
                        'INPUT':'INPUT',
                        'OUTPUT':'OUTPUT',
                        'SERVO':'OUTPUT',
                        'MOTOR':'OUTPUT',
                        'NEOPIXEL':'OUTPUT'}
    
    def __init__(self, name, type_code, pin_no):
        super().__init__(name)
        if type_code not in GPIO.valid_type_codes:
            raise ColError (type_code + 'not in' + GPIO.valid_type_codes)
        self.type_code = type_code
        GPIO.allocate(pin_no, self)
        self.pin_no = pin_no
        self.previous = 'UNKNOWN'

    def close(self):
        GPIO.deallocate(self.pin_no)
        super().close()

class DigitalInput(GPIO):
    def __init__(self, name, type_code, pin_no, pullup=machine.Pin.PULL_UP, callback=None):
        super().__init__(name, type_code, pin_no)
        self.pin = machine.Pin(self.pin_no, machine.Pin.IN, pullup)
        if callback is not None:
            self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
        self.state = 'UNKNOWN'
        GPIO.ids[id(self.pin)] = self
    def get(self):
        if self.pin.value() == 0:
            self.state = 'ON'
        elif self.pin.value() == 1:
            self.state = 'OFF'
        else:
            self.state = 'UNKNOWN'
        return self.state

class Button(DigitalInput): 
    button_list = []
    def __init__(self, name, pin_no):
        super().__init__(name, 'BUTTON', pin_no)
        self.pin = machine.Pin(self.pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
        Button.button_list.append(self)
    def wait(self, seconds=100, LED=None):
        flash_iterations = 100
        flip_flop = True
        loops = seconds * 1000
        for i in range(loops):   #  wait maximum of 100 seconds
            if LED is not None:
                if i % flash_iterations == 0:
                    if flip_flop:
                        LED.on()
                    else:
                        LED.off()
                    flip_flop = not flip_flop
            response = self.get()
            if self.state == 'ON':
                if LED is not None:
                    LED.off()
                return True
            utime.sleep_ms(1)
        if LED is not None:
            LED.off()
        return False
        
class BlueButton(Button):
    def __init__(self):
        super().__init__('Blue Button', constants.BLUE_BUTTON_PIN_NO)

class TheseButtons(ColObj):
    def __init__(self):
        super().__init__('Buttons','List of all buttons')
        self.blue_button = BlueButton()
        self.list = [self.blue_button]

class Switch(DigitalInput):
    switch_list = []
    def __init__(self, name, pin_no):
        super().__init__(name, 'SWITCH', pin_no)
        self.pin = machine.Pin(self.pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
        Switch.switch_list.append(self)
    def get(self):
        if self.pin.value() == 0:
            self.state = 'ON'
        elif self.pin.value() == 1:
            self.state = 'OFF'
        else:
            self.state = 'UNKNOWN'
        return self.state

class DIP_1(Switch):
    def __init__(self):
        super().__init__('DIP_1', constants.DIP_1_PIN_NO)

class DIP_5(Switch):
    def __init__(self):
        super().__init__('DIP_5', constants.DIP_5_PIN_NO)

class DIP_6(Switch):
    def __init__(self):
        super().__init__('DIP_6', constants.DIP_6_PIN_NO)

class TheseSwitches(ColObj):
    def __init__(self):
        super().__init__('Switches','List of all switches')
        self.dip_1 = DIP_1()
        self.dip_5 = DIP_5()
        self.dip_6 = DIP_6()
        self.list = [self.dip_1, self.dip_5, self.dip_6]

class SBUSReceiver:
    def __init__(self, uart):
        self.sbus = uart
        # constants
        self.START_BYTE = b'0f'
        self.END_BYTE = b'00'
        self.SBUS_FRAME_LEN = 25
        self.SBUS_NUM_CHAN = 18
        self.OUT_OF_SYNC_THD = 10
        self.SBUS_NUM_CHANNELS = 18
        self.SBUS_SIGNAL_OK = 0
        self.SBUS_SIGNAL_LOST = 1
        self.SBUS_SIGNAL_FAILSAFE = 2

        # Stack Variables initialization
        self.validSbusFrame = 0
        self.lostSbusFrame = 0
        self.frameIndex = 0
        self.resyncEvent = 0
        self.outOfSyncCounter = 0
        self.sbusBuff = bytearray(1)  # single byte used for sync
        self.sbusFrame = bytearray(25)  # single SBUS Frame
        self.sbusChannels = array.array('H', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # RC Channels
        self.isSync = False
        self.startByteFound = False
        self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

    def get_rx_channels(self):
        """
        Used to retrieve the last SBUS channels values reading
        :return:  an array of 18 unsigned short elements containing 16 standard channel values + 2 digitals (ch 17 and 18)
        """
        return self.sbusChannels

    def get_rx_channel(self, num_ch):
        """
        Used to retrieve the last SBUS channel value reading for a specific channel
        :param: num_ch: the channel which to retrieve the value for
        :return:  a short value containing
        """
        return self.sbusChannels[num_ch]

    def get_failsafe_status(self):
        """
        Used to retrieve the last FAILSAFE status
        :return:  a short value containing
        """
        return self.failSafeStatus

    def get_rx_report(self):
        """
        Used to retrieve some stats about the frames decoding
        :return:  a dictionary containg three information ('Valid Frames','Lost Frames', 'Resync Events')
        """

        rep = {}
        rep['Valid Frames'] = self.validSbusFrame
        rep['Lost Frames'] = self.lostSbusFrame
        rep['Resync Events'] = self.resyncEvent

        return rep

    def decode_frame(self):

        # TODO: DoubleCheck if it has to be removed
        for i in range(0, self.SBUS_NUM_CHANNELS - 2):
            self.sbusChannels[i] = 0

        # counters initialization
        byte_in_sbus = 1
        bit_in_sbus = 0
        ch = 0
        bit_in_channel = 0

        for i in range(0, 175):  # TODO Generalization
            if self.sbusFrame[byte_in_sbus] & (1 << bit_in_sbus):
                self.sbusChannels[ch] |= (1 << bit_in_channel)

            bit_in_sbus += 1
            bit_in_channel += 1

            if bit_in_sbus == 8:
                bit_in_sbus = 0
                byte_in_sbus += 1

            if bit_in_channel == 11:
                bit_in_channel = 0
                ch += 1

        # Decode Digitals Channels

        # Digital Channel 1
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 0):
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 0

        # Digital Channel 2
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 1):
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 0

        # Failsafe
        self.failSafeStatus = self.SBUS_SIGNAL_OK
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 2):
            self.failSafeStatus = self.SBUS_SIGNAL_LOST
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 3):
            self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

    def get_sync(self):

        if self.sbus.any() > 0:

            if self.startByteFound:
                if self.frameIndex == (self.SBUS_FRAME_LEN - 1):
                    self.sbus.readinto(self.sbusBuff, 1)  # end of frame byte
                    if self.sbusBuff[0] == 0:  # TODO: Change to use constant var value
                        self.startByteFound = False
                        self.isSync = True
                        self.frameIndex = 0
#                        return("found sync")
                else:
                    self.sbus.readinto(self.sbusBuff, 1)  # keep reading 1 byte until the end of frame
                    self.frameIndex += 1
#                    return("start byte found no sync")
            else:
                self.frameIndex = 0
                self.sbus.readinto(self.sbusBuff, 1)  # read 1 byte
                if self.sbusBuff[0] == 15:  # TODO: Change to use constant var value
                    self.startByteFound = True
                    self.frameIndex += 1

    def get_new_data(self):
        """
        This function must be called periodically according to the specific SBUS implementation in order to update
        the channels values.
        For FrSky the period is 300us.
        """

        if self.isSync:
            if self.sbus.any(): # uart.any() returns a 0 or a 1 in this implementation which 'self.sbus.any() >= self.SBUS_FRAME_LEN' would never be true. 3 days working on this. 
                self.sbus.readinto(self.sbusFrame, self.SBUS_FRAME_LEN)  # read the whole frame
                if (self.sbusFrame[0] == 15 and self.sbusFrame[
                    self.SBUS_FRAME_LEN - 1] == 0):  # TODO: Change to use constant var value
                    self.validSbusFrame += 1
                    self.outOfSyncCounter = 0
                    self.decode_frame()
                    return("decode")
                else:
                    self.lostSbusFrame += 1
                    self.outOfSyncCounter += 1

                if self.outOfSyncCounter > self.OUT_OF_SYNC_THD:
                    self.isSync = False
                    self.resyncEvent += 1
                    
            return("is synced")       
        else:
            self.get_sync()

class Interpolator(ColObj):
    def __init__(self, name, keys, values): # arrays of matching pairs
                                            # keys ascending integers
                                            # values any floats
        super().__init__(name)
        self.keys = keys
        self.values = values
    def interpolate(self, in_key):  #  input is integer
        if in_key is None:
            return None
        below_ok = False
        above_ok = False
        for i in range(len(self.keys)):
            if in_key == self.keys[i]:
                return self.values[i]
            if in_key > self.keys[i]:
                below_key = self.keys[i]
                below_value = self.values[i]
                below_ok = True
            if in_key < self.keys[i]:
                above_key = self.keys[i]
                above_value = self.values[i]
                above_ok = True
                break
        if above_ok and below_ok:
            out_value = below_value + (((in_key - below_key) / (above_key - below_key)) * (above_value - below_value))
            return out_value
        else:
            return None


class SBUSReceiverMC6C(ColObj):
    def __init__(self):
        super().__init__('MicroZone mc6c')
        self.tx_pin_no = constants.UART_TX_PIN_NO
        self.rx_pin_no = constants.UART_RX_PIN_NO
        self.uart_no = constants.UART_NO
        self.baud_rate = constants.UART_BAUD_RATE
        self.uart = machine.UART(self.uart_no, self.baud_rate, tx = machine.Pin(self.tx_pin_no), rx = machine.Pin(self.rx_pin_no), bits=8, parity=0, stop=2)
        self.sbus = SBUSReceiver(self.uart)
        ############################################################################
        self.steering_index = 0   #  NOTE: array index starts at zero
        self.throttle_index = 1   #        channel numbers start at one
        self.updown_index = 2
        self.crab_index = 3
        self.switch_index = 4
        self.knob_index = 5
        ##########################################################################
        self.no_channels = 6
        ################ Obtain these values from test_18_SBUS_A   ########################
        self.mins = [ 689,  633,  201,  569,  201,  201]
        self.mids = [1091, 1025, 1052,  976, 1001, 1060]
        self.maxs = [1486, 1433, 1801, 1369, 1801, 1801]
        ################# Adjust for a bit of leeway #####################################
        mida = 20
        enda = 10
        self.default_results = [100.0, 100.0, 0.0, 0.0, -100.0, -100.0]
        self.inverse_results = [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0]
        
        minv = 689
        midv = 1091
        maxv = 1486
        self.steering_interpolator = Interpolator('Steering Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.default_results)
        minv = 633
        midv = 1025
        maxv = 1433
        self.throttle_interpolator = Interpolator('Throttle Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.inverse_results)
        minv = 201
        midv = 1052
        maxv = 1801
        self.updown_interpolator = Interpolator('Up-Down Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.default_results)
        minv = 569
        midv = 976
        maxv = 1369
        self.crab_interpolator = Interpolator('Crab Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.default_results)
        minv = 201
        midv = 1001
        maxv = 1801
        self.switch_interpolator = Interpolator('Switch Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.default_results)
        minv = 201
        midv = 1060
        maxv = 1801
        self.knob_interpolator = Interpolator('Knob Interpolator',
                [0, minv+enda, midv-mida, midv+mida, maxv-enda, 2000], self.default_results)
        self.thread_enable = True
        self.thread_running = False
        self.joystick_raws = [0] * 18
        self.old_mix_values = [0] * 4
        self.nones_count = 0
        self.zeroes_count = 0

    def __str__(self):
        outstring = self.name + '\n'
        outstring += str(self.throttle_interpolator) + '\n'
        outstring += str(self.steering_interpolator) + '\n'
        return outstring

    def get_raws(self):
        max_attempts = 15
        for i in range(max_attempts):
            utime.sleep_us(400)
            self.sbus.get_new_data()
            self.joystick_raws = self.sbus.get_rx_channels()
            first_raw = self.joystick_raws[0]
            if abs(first_raw) > 15:
                break
        if i >= max_attempts:
            return None, None, None, None, None, None
        steering_raw = self.joystick_raws[self.steering_index]
        throttle_raw = self.joystick_raws[self.throttle_index]
        updown_raw = self.joystick_raws[self.updown_index]
        crab_raw = self.joystick_raws[self.crab_index]
        switch_raw = self.joystick_raws[self.switch_index]
        knob_raw = self.joystick_raws[self.knob_index]
        return steering_raw, throttle_raw, updown_raw, crab_raw, switch_raw, knob_raw

    def get(self):
        steering_raw, throttle_raw, updown_raw, crab_raw, switch_raw, knob_raw = self.get_raws()
        if steering_raw is None:
            return None, None, None, None, None, None
        steering_value = self.steering_interpolator.interpolate(steering_raw)
        throttle_value = self.throttle_interpolator.interpolate(throttle_raw)
        updown_value = self.steering_interpolator.interpolate(updown_raw)
        crab_value = self.steering_interpolator.interpolate(crab_raw)
        switch_value = self.switch_interpolator.interpolate(switch_raw)
        knob_value = self.steering_interpolator.interpolate(knob_raw)
        return steering_value, throttle_value, updown_value, crab_value, switch_value, knob_value

    def array_abs(self, input_array):
        output_array = []
        for element in input_array:
            if element is not None:
                output_array.append(abs(element))
            else:
                output_array.append(0)
        return output_array

    def close(self):
        self.steering_interpolator.close()
        self.throttle_interpolator.close()
        self.updown_interpolator.close()
        self.crab_interpolator.close()
        self.switch_interpolator.close()
        self.knob_interpolator.close()
        self.thread_enable = False
        utime.sleep_ms(100)
        if self.thread_running:
            print ('error thread not closed')
        super().close()

class Mixer(ColObj):
    def __init__(self, name):
        super().__init__(name)
    def array_abs(self, input_array):
        output_array = []
        for element in input_array:
            if element is None:
                output_array.append(0)
            else:
                output_array.append(abs(element))
        return output_array

    def mix(self, spin, fore_and_aft, crab=0):  #  expects values in range -100 to +100
        inputs_abs = self.array_abs([spin, fore_and_aft, crab])
        biggest_in = max(inputs_abs)
        total_in = sum(inputs_abs)
        if total_in == 0:
            return 0,0,0,0
        fwd_levels = [fore_and_aft, fore_and_aft, fore_and_aft, fore_and_aft]
        spin_levels = [spin, -spin, spin, -spin]
        fwd_abs = self.array_abs(fwd_levels)
        spin_abs = self.array_abs(spin_levels)
        total_out = sum(fwd_abs) + sum(spin_abs)
        crab_levels = [0,0,0,0]
        if crab != 0:
            crab_levels = [crab, crab, -crab, -crab]
            crab_abs = self.array_abs(crab_levels)
            total_out = total_out + sum(crab_abs)
        ratio_a = 1.0
        lf_level = (fwd_levels[0] + spin_levels[0] + crab_levels[0]) * ratio_a
        rf_level = (fwd_levels[1] + spin_levels[1] - crab_levels[1]) * ratio_a
        lb_level = (fwd_levels[2] + spin_levels[2] + crab_levels[2]) * ratio_a
        rb_level = (fwd_levels[3] + spin_levels[3] - crab_levels[3]) * ratio_a
        output_abs = self.array_abs([lf_level, rf_level, lb_level, rb_level])
        biggest_out = max(output_abs)
        ratio_b = biggest_in / biggest_out
        lf_level = lf_level * ratio_b
        rf_level = rf_level * ratio_b
        lb_level = lb_level * ratio_b
        rb_level = rb_level * ratio_b
        return -lf_level, -rf_level, -lb_level, -rb_level

class Motor(ColObj):
    def __init__(self, name, description=''):
        super().__init__(name, description)
    def clk(self, speed):
        raise ColError('**** Must be overriden')
    def anti(self, speed):
        raise ColError('**** Must be overriden')
    def stop(self):
        raise ColError('**** Must be overriden')

class FIT0441BasicMotor(Motor):  #  cut down for R/C
    def __init__(self, name, direction_pin_no, speed_pin_no):
        super().__init__(name)
        self.direction_pin_GPIO = GPIO(pin_no=direction_pin_no, type_code='MOTOR', name=name+'_direction_'+str(direction_pin_no))
        self.direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)
        self.speed_pin_GPIO = GPIO(pin_no=speed_pin_no, type_code='MOTOR', name=name+'_speed_'+str(speed_pin_no))
        self.speed_pin = machine.PWM(machine.Pin(speed_pin_no))
        self.speed_pin.freq(25000)
        self.duty = 0
        self.stop_duty = 65534
        self.min_speed_duty = 65000
        self.max_speed_duty = 0
        self.clockwise = 1
        self.anticlockwise = 0

    def __str__(self):
        outstring = self.name
        outstring += ', speed pin: ' + str(self.speed_pin_GPIO.pin_no)
        outstring += ', direction pin: ' + str(self.direction_pin_GPIO.pin_no)
        return outstring

    def clk(self, speed):  #  speed is from 0 to 100
        self.direction_pin.value(self.clockwise)
        self.set_speed(speed)

    def anti(self, speed):
        self.direction_pin.value(self.anticlockwise)
        self.set_speed(speed)

    def run(self, speed):  #  speed is from -100 to +100
        if speed == 0:
            self.stop()
            return
        if speed > 0:
            self.clk(speed)
        else:
            self.anti(-speed)

    def stop(self):
        duty = self.stop_duty
        self.speed_pin.duty_u16(duty)
        utime.sleep_ms(1)
        
    def close(self):
        self.direction_pin_GPIO.close()
        self.speed_pin_GPIO.close()
        super().close()

    def set_speed(self, speed):  #  as a percentage
        self.duty = (self.min_speed_duty
                     - int(float(self.min_speed_duty - self.max_speed_duty)
                        * (float(speed) / 100.0)))
        self.speed_pin.duty_u16(self.duty)
    
    def set_direction(self, direction):  # 1 = clockwise, 0 = anticlockwise
        if direction == 1:
            self.direction_pin.value(self.clockwise)
        elif direction == 0:
            self.direction_pin.value(self.anticlockwise)

class ThisDriveTrain(ColObj):
    def __init__(self):
        super().__init__('PicoA Drive Train')
        self.lf_speed_pin_no     = constants.LF_SPEED_PIN_NO   # blue
        self.lf_pulse_pin_no     = constants.LF_PULSE_PIN_NO   # green
        self.lf_direction_pin_no = constants.LF_DIRECTION_PIN_NO   # yellow
        self.motor_lf = FIT0441BasicMotor('Left Front', self.lf_direction_pin_no,
                                              self.lf_speed_pin_no)
        self.lb_speed_pin_no     = constants.LB_SPEED_PIN_NO   # blue
        self.lb_pulse_pin_no     = constants.LB_PULSE_PIN_NO   # green
        self.lb_direction_pin_no = constants.LB_DIRECTION_PIN_NO   # yellow
        self.motor_lb = FIT0441BasicMotor('Left Back', self.lb_direction_pin_no,
                                              self.lb_speed_pin_no)
        self.rf_speed_pin_no     = constants.RF_SPEED_PIN_NO   # blue
        self.rf_pulse_pin_no     = constants.RF_PULSE_PIN_NO   # green
        self.rf_direction_pin_no = constants.RF_DIRECTION_PIN_NO   # yellow
        self.motor_rf = FIT0441BasicMotor('Right Front', self.rf_direction_pin_no,
                                                self.rf_speed_pin_no)
        self.rb_speed_pin_no     = constants.RB_SPEED_PIN_NO   # blue
        self.rb_pulse_pin_no     = constants.RB_PULSE_PIN_NO   # green
        self.rb_direction_pin_no = constants.RB_DIRECTION_PIN_NO   # yellow
        self.motor_rb = FIT0441BasicMotor('Right Back', self.rb_direction_pin_no,
                                                self.rb_speed_pin_no)
        self.motor_list = [self.motor_rf, self.motor_rb, self.motor_lf, self.motor_lb]
        self.mixer = Mixer('Full Mixer')

    def close(self):
        for motor in self.motor_list:
            motor.close()
        self.mixer.close()
        super().close()
        
    def stop(self):
        for motor in self.motor_list:
            motor.stop()
        
    def drive(self, steering, throttle, crab):
        lf_level, rf_level, lb_level, rb_level = self.mixer.mix(steering, throttle, crab)
        self.motor_lf.run(lf_level)
        self.motor_rf.run(rf_level)
        self.motor_lb.run(lb_level)
        self.motor_rb.run(rb_level)
        if sum([lf_level, lb_level]) > sum([rf_level, rb_level]):
            my_headlight.spr()
        elif sum([lf_level, lb_level]) < sum([rf_level, rb_level]):
            my_headlight.spl()
        elif sum([lf_level, rf_level, lb_level, rb_level]) >= 0:
            my_headlight.fwd()
        else:
            my_headlight.rev()

# <<<<<<<<<<<<<<<<<<<<<<<<<<drived created by JOHN to facilitate easier PID control 2024/04/11
# constrain created to limit motor drives to +-100
    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))
           #   result = my_drive_train.drived(left_front, left_rear, right_front,right_rear)         
    def drived(self, left_front, left_rear, right_front, right_rear):
    
        self.motor_lf.run(-self.constrain(left_front,-100,100))
        self.motor_rf.run(self.constrain(right_front,-100,100))
        self.motor_lb.run(-self.constrain(left_rear,-100,100))
        self.motor_rb.run(self.constrain(right_rear,-100,100))
        return 0
#         if sum([lf_level, lb_level]) > sum([rf_level, rb_level]):
#             my_headlight.spr()
#         elif sum([lf_level, lb_level]) < sum([rf_level, rb_level]):
#             my_headlight.spl()
#         elif sum([lf_level, rf_level, lb_level, rb_level]) >= 0:
#             my_headlight.fwd()
#         else:
#             my_headlight.rev()

class DigitalOutput(GPIO):
    def __init__(self, name, type_code, pin_no):
        super().__init__(name, type_code, pin_no)
        self.pin = machine.Pin(pin_no, machine.Pin.OUT)
    def set(self, new_state):
        if new_state == 'ON':
            self.pin.value(0)
            return True
        elif new_state == 'OFF':
            self.pin.value(1)
            return True
        return False

class PIO(ColObj):
    
    allocated = {}
    free_code = '--FREE--'
    pio_no = 0
    for i in range(2):  #  There are two blocks. Block 0 is conventionally used for remote control
                        #                        Block 1 is conventionally used for neopixels
                        #  This avoids running out of code space as code gets re-used
                        #  On the Pico W, state machine 4 is used for wireless
        allocated[i] = {}
        for j in range(4):   #  each block has 4 PIOs
            allocated[i][j] = {'PIO':pio_no,'NAME':free_code}
            pio_no += 1
    allocated[1][0]['NAME'] = 'WIRELESS'
    
    def str_allocated():
        out_string = ('{:3}'.format('PIO') +
                      '  {:18}'.format('NAME') + '\n')
        for i in range(2):
            for j in range(4):
                out_string += ('{:3}'.format(PIO.allocated[i][j]['PIO'])  +
                               '  {:18}'.format(PIO.allocated[i][j]['NAME']) + '\n')
        return out_string

    def allocate(name, block):
        for j in range(4):
            if PIO.allocated[block][j]['NAME'] == PIO.free_code:
                PIO.allocated[block][j]['NAME'] = name
                return PIO.allocated[block][j]['PIO']
        return None        
        
    def deallocate(pio_no):
        for i in range(2):
            for j in range(4):
                if PIO.allocated[i][j]['PIO'] == pio_no:
                    PIO.allocated[i][j]['NAME'] = PIO.free_code
                    return True
        return False

    def __init__(self, name, block_no):
        super().__init__(name)
        self.block_no = block_no
        self.pio_no = PIO.allocate(name, block_no)
        if self.pio_no is None:
            print (PIO.str_allocated())
            raise ColError('**** Could not get PIO')

    def __str__(self):
        out_string = 'PIO: ' + self.name
        out_string += ', state_machine_no: ' + str(self.pio_no)
        out_string += ', block: ' + str(self.block_no)
        return out_string

    def close(self):
        PIO.deallocate(self.pio_no)
        super().close()


class NeoPixel(DigitalOutput):
    def __init__(self, name, pin_no, no_pixels, mode):
        super().__init__(name, 'NEOPIXEL', pin_no)
        self.valid = False
        self.state_machine_no = PIO.allocate(name,1)
        #GPIOPico.GPIO.allocate(pin_no, self)
        self.no_pixels = no_pixels
        self.mode = mode
        self.pixels = neopixel.Neopixel(self.no_pixels, self.state_machine_no, self.pin_no, self.mode)
        #  The following definitions are examples which can be overriden or augmented
        self.colours = {'red':(255, 0, 0),
                        'dim_red':(63,0,0),
                        'orange':(255, 45, 0),
                        'yellow':(200,130,0),
                        'green':(0, 155, 0),
                        'dim_green':(0,23,0),
                        'blue':(0, 0, 255),
                        'dim_blue':(0,0,23),
                        'white':(255,255,255),
                        'dim_white':(3,3,3),
                        'on':(255,255,255),
                        'off':(0,0,0)}
        self.patterns = {'off':['off'],
                         'on':['white'],
                         'red':['red'],
                         'orange':['orange'],
                         'blue':['blue'],
                         'mixed':['red','blue','green','white']}
        self.sectors = {}

    def set_sector_to_pattern(self, sector, pattern, offset=0):
        start = self.sectors[sector][0]
        end = self.sectors[sector][1]
        slen = end - start + 1
        plen = len(self.patterns[pattern])
        j = 0
        for i in range(slen):
            where = start + ((i + offset) % slen)
            colour = self.colours[self.patterns[pattern][j]]
            self.pixels[where] = colour
            j += 1
            j = j % plen

    def set_pixel(self, where, colour):
        self.pixels[where] = colour
        self.pixels.show()

    def fill(self, colour):
        self.pixels.fill(colour)

    def fill_sector(self, sector, colour):
        start = self.sectors[sector][0]
        end = self.sectors[sector][1]
        self.pixels[start:end+1] = self.colours[colour]

    def clear_sector(self, sector):
        start = self.sectors[sector][0]
        end = self.sectors[sector][1]
        self.pixels[start:end+1] = self.colours['off']

    def show(self):
        self.pixels.show()
        
    def clear(self):
        self.pixels.clear()
        self.pixels.show()

    def close(self):
        self.clear()
        utime.sleep_ms(100)
        super().close()
        utime.sleep_ms(100)
        PIO.deallocate(self.state_machine_no)

    def on(self, colour=(120, 100, 0)):
        self.pixels.fill(colour)
        self.pixels.show()
    
    def off(self):
        self.clear()

class ThisRearLight(NeoPixel):
    def __init__(self):
        super().__init__(name='Rear Light', pin_no=15, no_pixels=7, mode='GRBW')
        self.sectors['centre'] = [0,0]
        self.sectors['rim'] = [1,6]
    def OK(self):
        self.fill_sector('centre','blue')
        self.clear_sector('rim')
        self.show()
    def bad(self):
        self.fill_sector('centre','blue')
        self.fill_sector('rim','red')
        self.show()
    def running(self, on=True):
        if not on:
            self.set_pixel(0,self.colours['dim_white'])
        else:
            self.set_pixel(0,self.colours['blue'])
    def obey_radio(self, on=True):
        if not on:
            self.set_pixel(1,self.colours['dim_white'])
        else:
            self.set_pixel(1,self.colours['blue'])
    def mecanum(self, on=True):
        if not on:
            self.set_pixel(2,self.colours['dim_white'])
        else:
            self.set_pixel(2,self.colours['yellow'])
    def obey_pi(self, on=True):
        if not on:
            self.set_pixel(3,self.colours['dim_white'])
        else:
            self.set_pixel(3,self.colours['green'])
    
class ThisHeadlight(NeoPixel):
    def __init__(self):
        super().__init__(name='headlights', pin_no=18, no_pixels=14, mode='GRB')
        self.sectors['front_right_centre'] = [0,0]
        self.sectors['front_right_rim'] = [1,6]
        self.sectors['front_left_centre'] = [7,7]
        self.sectors['front_left_rim'] = [8,13]
    def fwd(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','white')
        self.fill_sector('front_left_rim','white')
        self.show()
    def rev(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','red')
        self.fill_sector('front_left_rim','red')
        self.show()
    def spl(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','red')
        self.fill_sector('front_right_rim','white')
        self.fill_sector('front_left_rim','red')
        self.show()
    def spr(self):
        self.fill_sector('front_right_centre','red')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','red')
        self.fill_sector('front_left_rim','white')
        self.show()        

class ThisHandshake(DigitalOutput):   #  Note pin_value of zero = 'ON', 1 = 'OFF'
    def __init__(self):                    
        super().__init__('Pi Handshake','OUTPUT',constants.HANDSHAKE_PIN_NO)
    def set_on(self):
        self.pin.value(0)
    def set_off(self):
        self.pin.value(1)


class CommandStream(ColObj):
    
    in_use = False
    
    def __init__(self, name, handshake_object):
        super().__init__(name, 'Command Stream from Pi')
        if CommandStream.in_use:
            self.valid = False
        else:
            CommandStream.in_use = True
            self.valid = True
        self.handshake_object = handshake_object
        
    def ready(self):
        if self.handshake_object is not None:
            self.handshake_object.set_on()

    def not_ready(self):
        if self.handshake_object is not None:
            self.handshake_object.set_off()

    def close(self):
        self.not_ready()
        CommandStream.in_use = False
        self.valid = False

    def get(self, delay=0.01):
        inputs, outputs, errors = select.select([sys.stdin],[],[],delay)
        if (len(inputs) > 0):
            result = sys.stdin.readline()
        else:
            result = False
        return result

    def get_command(self):
        self.ready()
        sub_result = self.get()
        self.not_ready()
        if not sub_result:
            return None, None, None
        if len(sub_result) < 8:
            return None, None, None
        serial_no = sub_result[0:4]
        command = sub_result[4:8]
        if len(sub_result) > 8:
            data = sub_result[8:]
        else:
            data = None
        return serial_no, command, data

    def send(self, message):
        print (message)
 
    def flush(self):
        no_inputs = 1
        while no_inputs > 0:
            inputs, outputs, errors = select.select([sys.stdin],[],[],0.001)
            if (len(inputs) > 0):
                result = sys.stdin.readline()
            else:
                break

def run_motors(steering, throttle, duration):
    lf_level, rf_level, lb_level, rb_level = my_drive_train.mixer.mix(steering, throttle)
    my_drive_train.motor_lf.run(-lf_level)
    my_drive_train.motor_rf.run(rf_level)
    my_drive_train.motor_lb.run(-lb_level)
    my_drive_train.motor_rb.run(rb_level)
    if duration > 0:
        utime.sleep_ms(duration)
        my_drive_train.stop()

def process_command(serial_no, command, data, 
                   steering_value, throttle_value, updown_value, crab_value, switch_value, knob_value):
    if 'WHOU' == command:
        my_stream.send(serial_no + 'OKOK' + constants.PICO_NAME)   ########### Col 11/Apr
        my_rear_light.OK()
        log(command + 'OK')
        return True
    elif 'EXIT' == command:
        my_stream.send(serial_no + 'OKOK' + 'Exiting')
        log(command + 'OK')
        return False
    elif 'SGRN' == command:
        my_stream.send(serial_no + 'OKOK')
        my_rear_light.set_pixel(6, my_rear_light.colours['green'])
        my_rear_light.show()
        return True
    elif 'SRED' == command:
        my_stream.send(serial_no + 'OKOK')
        my_rear_light.set_pixel(6, my_rear_light.colours['red'])
        my_rear_light.show()
        return True
    elif 'SBLU' == command:
        my_stream.send(serial_no + 'OKOK')
        my_rear_light.set_pixel(6, my_rear_light.colours['blue'])
        my_rear_light.show()
        return True
    elif 'SOFF' == command:
        my_stream.send(serial_no + 'OKOK')
        my_rear_light.set_pixel(6, my_rear_light.colours['off'])
        my_rear_light.show()
        return True
    elif 'SBUS' == command:
        values = '{:4}{:4}{:4}{:4}{:4}{:4}'.format(  
            int(steering_value),
            int(throttle_value),
            int(updown_value),
            int(crab_value),
            int(switch_value),
            int(knob_value))
        if obey_radio:
            values += '   1'
        else:
            values += '   0'
        if obey_pi:
            values += '   1'
        else:
            values += '   0'
        my_stream.send(serial_no + 'OKOK' + values)
        my_rear_light.OK()
        log(command + 'OK')
        return True
    elif 'WAIT' == command:
        my_stream.send(serial_no + 'OKOK' + 'Waiting')
        duration = int(data[0:4])
        utime.sleep_ms(duration)
        log(command + 'OK')
        return True
    elif command == 'HREV':                          ###OLD commands added by JOHN
        my_stream.send(serial_no + 'OKOK')
        log(serial_no + 'OKOK')
        my_headlight.rev()
        return True
    elif command == 'TRNL':
        if ((data is None) or (len(data) < 4)):
            my_stream.send(serial_no + 'BADC')
            my_rear_light.bad()
            ermsg = '*** Bad TRNR parms ***'
            log(ermsg)
            my_drive_train.stop()
            return True
        else:
            try:
                duration = int(data[0:4])
            except ValueError:
                my_stream.send(serial_no + 'TRNR duration not integer')
                my_rear_light.bad()
                ermsg = '*** Bad DRIV parms ***'
                log(ermsg)
                my_drive_train.stop()
                return True
        steering = 100
        throttle = 0
        my_stream.send(serial_no + 'OKOK')
        log (command + ' ' + str(steering) + ' ' + str(throttle) + ' ' + data)
        run_motors(steering, throttle, duration)
        return True
    elif command == 'TRNR':
        if ((data is None) or (len(data) < 4)):
            my_stream.send(serial_no + 'BADC')
            my_rear_light.bad()
            ermsg = '*** Bad TRNR parms ***'
            log(ermsg)
            my_drive_train.stop()
            return True
        else:
            try:
                duration = int(data[0:4])
            except ValueError:
                my_stream.send(serial_no + 'TRNR duration not integer')
                my_rear_light.bad()
                ermsg = '*** Bad DRIV parms ***'
                log(ermsg)
                my_drive_train.stop()
                return True
        steering = -100
        throttle = 0
        my_stream.send(serial_no + 'OKOK')
        log (command + ' ' + str(steering) + ' ' + str(throttle) + ' ' + data)
        run_motors(steering, throttle, duration)
        return True
    elif command == 'FSTP':
        my_stream.send(serial_no + 'OKOK')
        log(serial_no + 'OKOK')
        my_drive_train.stop()
        my_headlight.off()
        return True
    elif command == 'STOP':
        my_stream.send(serial_no + 'OKOK')
        log(serial_no + 'OKOK')
        my_drive_train.stop()
        return True
   #     my_headlight.off()   # INTERFERES WITH THE LINE DETECTION
    elif command == 'HFWD':
        my_stream.send(serial_no + 'OKOK')
        log(serial_no + 'OKOK')
        my_headlight.fwd()
        return True
    elif command == 'HOFF':
        my_stream.send(serial_no + 'OKOK')
        log(serial_no + 'OKOK')
        my_headlight.off()
        return True
    elif 'DRIV' == command:
        if ((data is None) or (len(data) < 8)):
            errmsg = 'BADC *** No DRIV parms ***'
            my_stream.send(serial_no + errmsg)
            my_rear_light.bad()
            log(errmsg)
            my_drive_train.stop()
            return True
        else:
            try:
                throttle = int(data[0:4])
            except ValueError:
                errmsg = 'BADV throttle not integer ****'
                my_stream.send(serial_no + errmsg)
                my_rear_light.bad()
                log(errmsg)
                my_drive_train.stop()
                return True
            try:
                steering = int(data[4:8])
            except ValueError:
                errmsg = 'BADV steering not integer ****'
                my_stream.send(serial_no + errmsg)
                my_rear_light.bad()
                log(errmsg)
                my_drive_train.stop()
                return True
            if len(data) > 8:
                try:
                    delay = int(data[8:12])
                except ValueError:
                    errmsg = 'BADV delay not integer ****'
                    my_stream.send(serial_no + errmsg)
                    my_rear_light.bad()
                    log(errmsg)
                    my_drive_train.stop()
                    return True
            else:
                delay = 0
            my_stream.send(serial_no + 'OKOK' + 'Driving')
            my_rear_light.OK()
            log('before DRIV: ' + command + ' ' + data)
            crab = 0
            result = my_drive_train.drive(steering, throttle, crab)
            if delay > 0:
                utime.sleep_ms(delay)
                my_drive_train.stop()
            log('after DRIV: ' + str(result))
        return True
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Following section added by John 20240407<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<provides for easier translation from PID information. Is just direct motor control
    elif 'DRVD' == command:
        my_stream.send(serial_no + 'OKOK' + 'Driving')
        if ((data is None) or (len(data) < 8)):
            #my_stream.send(serial_no + 'BADC')
            #my_rear_light.bad()
            ermsg = '*** No DRIV parms ***'
            log(ermsg)
            my_drive_train.stop()
            return True
        else:
            try:
                left_front = int(data[0:4])
                left_rear = int(data[4:8])
                right_front = int(data[8:12])
                right_rear = int(data[12:])
                log(serial_no + 'OKOK')

            except ValueError:
                #my_stream.send(serial_no + 'BADV throttle not integer')
                my_rear_light.bad()
                ermsg = '*** Bad DRIV parms ***'
                log(ermsg)
                my_drive_train.stop()
                return True
            my_rear_light.OK()
            log('before DRIV' + command + data)
            log('Left front: {:}, Left rear {:}, Right front: {:}, Right rear: {:}'.format(left_front, left_rear, right_front,right_rear))
            result = my_drive_train.drived(left_front, left_rear, right_front,right_rear)
            log('after DRIV' + str(result))
       #     if delay > 0:
       #         utime.sleep_ms(delay)
        return True
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Previous section added by John 20240407<<<<<<<<<<<<<<<<<<<<<<
    else:
        ermsg = command + '*** Not Known ***'
        log(ermsg)
        my_stream.send(serial_no + 'BADC')
        return True

def log(msg):
    return False
    global logfile_name
    logging = open(logfile_name,'a')
    logging.write(msg + '\n')
    logging.close()
    return True

logfile_name = module_prefix + '_log.txt'
logging = open(logfile_name,'w')
logging.write('Logfile Starts\n\n')
logging.close()

log (module_name + ' starting at ' + str(start_time) + '\n')

my_rear_light = ThisRearLight()
my_buttons = TheseButtons()
my_switches = TheseSwitches()
my_dip_1 = my_switches.dip_1
my_dip_5 = my_switches.dip_5
my_dip_6 = my_switches.dip_6
my_drive_train = ThisDriveTrain()
my_drive_train.stop()
my_headlight  = ThisHeadlight()

if my_dip_1.get() == 'ON':
    mecanum = True
    log ('Mecanum Wheels Fitted')
else:
    mecanum = False
    log ('Standard Wheels Fitted')
my_rear_light.mecanum(mecanum)

if my_dip_5.get() == 'ON':
    obey_radio = True
else:
    obey_radio = False
my_rear_light.obey_radio(obey_radio)

if my_dip_6.get() == 'ON':
    obey_pi = True
else:
    obey_pi = False
my_rear_light.obey_pi(obey_pi)

if obey_radio:
    my_sbus = SBUSReceiverMC6C()
    log ('obey_radio')

testing_radio = False

if testing_radio:
    keys = [0, 633, 1015, 1035, 1433, 2000]
    values = [-100, -100, 0, 0, 100, 100]
    test_interpolator = Interpolator('Test', keys, values)
    print ('Testing Radio')
    for i in range(5):
        steering_raw, throttle_raw, updown_raw, swing_raw, switch_raw, knob_raw = my_sbus.get_raws()
        if steering_raw is None:
            continue
        steering_value, throttle_value, updown_value, swing_value, switch_value, knob_value = my_sbus.get()
    if steering_value is None:
        print ('NoNo')
    else:
        print (throttle_raw)
        print (test_interpolator.interpolate(throttle_raw))
        print (my_sbus.throttle_interpolator.interpolate(throttle_raw))
        print (test_interpolator.keys)
        print (test_interpolator.values)
        print (my_sbus.throttle_interpolator.keys)
        print (my_sbus.throttle_interpolator.values)
        print ('throttle', throttle_value)
    sys.exit(0)

testing_commands = False

if obey_pi or testing_commands:
    my_handshake = ThisHandshake()
    my_stream = CommandStream('HEBE Commands', my_handshake)
    log ('obey_pi')

################# pre commands for testing ########################

if testing_commands:
    pre_commands = [['SGRN', '0000', 1000],
                    ['SRED', '0000', 1000],
                    ['SBLU', '0000', 1000],
                    ['DRIV', '000000300500', 2000],
                    #['TRNR', '100 0 0040', 2000],
                    ['SOFF', '0000', 1000]]
    serial_no = 0
    for command_set in pre_commands:
        serial_no += 1
        serial_no_string = '{:04}'.format(serial_no)
        command = command_set[0]
        data = command_set[1]
        duration = command_set[2]
        keep_going = process_command(serial_no_string, command, data, 0, 0, 0, 0, 0, 0)
        if not keep_going:
            break
        utime.sleep_ms(duration)

###################################################################

max_throttle_value = 0

if not obey_pi and obey_radio:
    print ('Running under just radio control')
    my_rear_light.running()
    while True:
        utime.sleep_us(300)
        if my_dip_5.get() != 'ON':
            break
        my_sbus.sbus.get_new_data()
        steering_value, throttle_value, updown_value, crab_value, switch_value, knob_value = my_sbus.get()
        if steering_value is None:
            continue
        crab_value_to_use = 0
        my_drive_train.drive(throttle_value, steering_value, crab_value_to_use)
        if throttle_value > max_throttle_value:
            max_throttle_value = throttle_value
            print (max_throttle_value)

elif not obey_radio and obey_pi:
    print ('Running autonomously')
    i=0
    print ('Close Thonny and run command program on the Pi')
    while True:
        utime.sleep_us(300)
        i += 1
        if my_dip_6.get() != 'ON': # <<<<<<<<<<<<<<<<<<<<<<< comment out to allow testing-John
            break
        serial_no, command, data = my_stream.get_command()
        if serial_no is not None:
            log(serial_no + command)
            keep_going = process_command(serial_no, command, data,0,0,0,0,0,0)
            if not keep_going:
                log('*** keep_going not set ***')
                break

elif obey_radio and obey_pi:
    msg = 'Running with both pico and pi under radio control'
    print (msg)
    log(msg)
    i=0
    sbus_frequency = 20
    print ('Close Thonny and run command program (main_rc_zombie_arm) on the Pi')
    while True:
        utime.sleep_us(300)
        i += 1
        if my_dip_6.get() != 'ON':
            break
        if my_dip_5.get() != 'ON':
            break
        my_sbus.sbus.get_new_data()
        steering_value, throttle_value, updown_value, crab_value, switch_value, knob_value = my_sbus.get()
        if steering_value is None:
            continue
        if mecanum:
            crab_value_to_use = crab_value
        else:
            crab_value_to_use = 0
        ######### temp expedient, swap joysticks
        #  my_drive_train.drive(steering_value, throttle_value, crab_value_to_use)
        my_drive_train.drive(throttle_value, steering_value, crab_value_to_use)
        if i%sbus_frequency == 0:
            serial_no, command, data = my_stream.get_command()
            if serial_no is not None:
                log(serial_no + command)
                keep_going = process_command(serial_no, command, data,
                                             steering_value, throttle_value, updown_value, crab_value, switch_value, knob_value)
                if not keep_going:
                    log('*** keep_going not set ***')
                    break
else:
    print ('Nothing to do')
    log ('Nothing to do')

my_buttons.close()
my_switches.close()
my_drive_train.stop()
utime.sleep_ms(250)
my_drive_train.close()
my_rear_light.off()
my_rear_light.close()
if obey_radio:
    my_sbus.close()
if obey_pi:
    my_stream.close()
    my_handshake.close()
logging.close()