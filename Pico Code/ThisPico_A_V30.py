module_name = 'ThisPico_A_V30.py'

if __name__ == "__main__":
    print (module_name, 'starting\n')

module_creation_date = '09/Nov/2023'
import GPIOPico_V29 as GPIO
ColObjects = GPIO.ColObjects
import Motor_V03 as Motor
import NeoPixel_v12 as NeoPixel
import sbus_receiver_3 as sbus_receiver
import utime
import machine
import _thread

class ThisPico():
    opened = {}
    def add(this_object):
        ThisPico.opened[this_object.name] = this_object  
    def remove(this_object):
        del ThisPico.opened[this_object.name]  
    def str_opened():
        output = ''
        for this_name in sorted(ThisPico.opened):
            output += this_name + '\n'
        return output
    def close_all():
        for this_name in ThisPico.opened:
            ThisPico.opened[this_name].close()


class ThisVSYS(GPIO.Volts):
    def __init__(self):
        super().__init__('VSYS',29)
        ThisPico.add(self)
    def close(self):
        ThisPico.remove(self)
        super().close()


class ThisLeftSide(Motor.Side):
    def __init__(self):
        self.lf_speed_pin_no     = 2   # blue
        self.lf_pulse_pin_no     = 3   # green
        self.lf_direction_pin_no = 4   # yellow
        self.motor_lf = Motor.FIT0441Motor('Left Front', self.lf_direction_pin_no,
                                              self.lf_speed_pin_no, self.lf_pulse_pin_no)
        self.lb_speed_pin_no     = 10
        self.lb_pulse_pin_no     = 11
        self.lb_direction_pin_no = 12
        self.motor_lb = Motor.FIT0441Motor('Left Back', self.lb_direction_pin_no,
                                              self.lb_speed_pin_no, self.lb_pulse_pin_no)
        self.motor_list = [self.motor_lf, self.motor_lb]
        super().__init__('Left Side', 'L', self.motor_list)
    def close(self):
        for motor in self.motor_list:
            motor.close()
        super().close()
        
class ThisRightSide(Motor.Side):
    def __init__(self):
        self.right_front_speed_pin_no     = 6  # blue
        self.right_front_pulse_pin_no     = 7  # green
        self.right_front_direction_pin_no = 8  # yellow
        self.motor_right_front = Motor.FIT0441Motor('Right Front', self.right_front_direction_pin_no,
                                                       self.right_front_speed_pin_no, self.right_front_pulse_pin_no)
        self.motor_right_front.name = 'Right Front'

        self.right_back_speed_pin_no     = 21
        self.right_back_pulse_pin_no     = 20
        self.right_back_direction_pin_no = 19
        self.motor_right_back = Motor.FIT0441Motor('Right Back', self.right_back_direction_pin_no,
                                                      self.right_back_speed_pin_no, self.right_back_pulse_pin_no)
        self.motor_right_back.name = 'Right Back'
        self.motor_list = [self.motor_right_front, self.motor_right_back]
        super().__init__('Right Side', 'R', self.motor_list)
    def close(self):
        for motor in self.motor_list:
            motor.close()
        super().close()


class ThisDriveTrain(ColObjects.ColObj):
    def __init__(self):
        super().__init__('Pico A Drive Train')
        self.left_side = ThisLeftSide()
        self.right_side = ThisRightSide()
        self.all_motors = []
        for motor in self.left_side.motor_list:
            self.all_motors.append(motor)
        for motor in self.right_side.motor_list:
            self.all_motors.append(motor)
        self.min_throttle = -100
        self.max_throttle = 100
        self.min_steering = -100
        self.max_steering = 100
        self.mode = 'CAR'
        self.millimetre_factor = 30
        self.degree_factor = 30
        self.pulse_factor = 1
        #self.pulse_motor = ThisLeftSide.motor_lb   #  arbitrary
        
    def constrain(self, n, lowest, highest):
        if n > highest:
            a = highest
        elif n < lowest:
            a = lowest
        else:
            a = n
        return a
        
    def drive(self, throttle, steering):
        if self.mode == 'TANK':
            left = self.constrain (throttle, self.min_throttle, self.max_throttle)
            right = self.constrain (steering, self.min_steering, self.max_steering)
        else:
            left = self.constrain (throttle + steering, self.min_throttle, self.max_throttle)
            right = self.constrain (throttle - steering, self.min_throttle, self.max_throttle)
        self.left_side.drive(left)
        self.right_side.drive(right)

    def convert_millimetres_to_milliseconds(self, millimetres, speed):
        milliseconds = int (float(millimetres) * self.millimetre_factor * (100.0 / float(speed)))
        return milliseconds

    def convert_degrees_to_milliseconds(self, millimetres, speed):
        milliseconds = int (float(millimetres) * self.degree_factor * (100.0 / float(speed)))
        return milliseconds

    def convert_millimetres_to_pulses(self, millimetres):
        return int(millimetres * pulse_factor)

    def fwd(self, speed=50, millimetres=50):
        self.left_side.fwd(speed)
        self.right_side.fwd(speed)
        if millimetres > 0:
            ms = self.convert_millimetres_to_milliseconds(millimetres, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    
    def fwd_pulses(self, speed, no_pulses):
        for motor in self.all_motors:
            start = motor.get_pulses()
            motor.pulse_endpoint = start + no_pulses
        for motor in self.all_motors:
            motor.clk()
        
    def rev(self, speed=50, millimetres=50):
        self.left_side.rev(speed)
        self.right_side.rev(speed)
        if millimetres > 0:
            ms = self.convert_millimetres_to_milliseconds(millimetres, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def spl(self, speed=90, degrees=90):
        self.left_side.rev(speed)
        self.right_side.fwd(speed)
        if degrees > 0:
            ms = self.convert_degrees_to_milliseconds(degrees, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def spr(self, speed=90, degrees=90):
        self.left_side.fwd(speed)
        self.right_side.rev(speed)
        if degrees > 0:
            ms = self.convert_degrees_to_milliseconds(degrees, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def stop(self):
        self.left_side.stop()
        self.right_side.stop()
    def close(self):
        self.left_side.close()
        self.right_side.close()
        super().close()
        
class ThisSbusReceiver(ColObjects.ColObj):
    def __init__(self):
        super().__init__('MicroZone mc6c')
        self.tx_pin_no = 0
        self.rx_pin_no = 1
        self.uart_no = 0
        self.baud_rate = 100000
        self.uart = machine.UART(self.uart_no, self.baud_rate, tx = machine.Pin(self.tx_pin_no), rx = machine.Pin(self.rx_pin_no), bits=8, parity=0, stop=2)
        self.sbus = sbus_receiver.SBUSReceiver(self.uart)
        self.steering_index = 0   #  NOTE: array index starts at zero
        self.throttle_index = 1   #        channel numbers start at one
        self.raise_index = 2
        self.swing_index = 3
        self.switch_index = 4
        self.throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [100, 201, 900, 1090, 1801, 2000],
                                                [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 693, 1080, 1250, 1500, 2000],
                                                [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.switch_interpolator = ColObjects.Interpolator('Switch 5 Interpolator',
                                                [100, 393, 980, 1220, 1390, 2000],
                                                [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.thread_enable = True
        self.thread_running = False
        self.joystick_raws = [0,0,0,0,0,0]
        self.my_thread = _thread.start_new_thread(self.thread_code, ())

    def __str__(self):
        outstring = self.name + '\n'
        outstring += str(self.throttle_interpolator) + '\n'
        outstring += str(self.steering_interpolator) + '\n'
        return outstring

    def thread_code(self):
        self.thread_running = True
        while True:
            if not self.thread_enable:
                break
            utime.sleep_us(300)
            self.sbus.get_new_data()
            self.joystick_raws = self.sbus.get_rx_channels()[0:5]
        self.thread_running = False

    def get(self):
        max_attempts = 15
        for i in range(max_attempts):
            utime.sleep_us(400)
            steering_raw = self.joystick_raws[self.steering_index]
            if steering_raw > 15:
                break
        if i == max_attempts:
            return None, None
        throttle_raw = self.joystick_raws[self.throttle_index]
        switch_raw = self.joystick_raws[self.switch_index]
        throttle_value = self.throttle_interpolator.interpolate(throttle_raw)
        steering_value = self.steering_interpolator.interpolate(steering_raw)
        switch_value = self.switch_interpolator.interpolate(switch_raw)
        return throttle_value, steering_value, switch_value
        
    def close(self):
        self.throttle_interpolator.close()
        self.steering_interpolator.close()
        self.switch_interpolator.close()
        self.thread_enable = False
        utime.sleep_ms(100)
        if self.thread_running:
            print ('error thread not closed')
        super().close()

class ThisHeadlight(NeoPixel.NeoPixel):
    def __init__(self):
        super().__init__(name='headlights', pin_no=18, no_pixels=14, mode='GRB')
        self.sectors['front_right_centre'] = [0,0]
        self.sectors['front_right_rim'] = [1,6]
        self.sectors['front_left_centre'] = [7,7]
        self.sectors['front_left_rim'] = [8,13]

class ThisDriveTrainWithHeadlights(ThisDriveTrain):
    def __init__(self):
        super().__init__()
        self.headlight = ThisHeadlight()
        self.headlight.fill_sector('front_right_centre','white')
        self.headlight.fill_sector('front_left_centre','white')
        self.headlights_enable = True
        #  Note: pulse counting not needed for remote control
        for motor in self.left_side.motor_list:
            motor.pulse_pin.irq(None)
        for motor in self.right_side.motor_list:
            motor.pulse_pin.irq(None)
    def drive(self, throttle_value, steering_value):
        super().drive(throttle_value, steering_value)
        if not self.headlights_enabled:
            self.headlight.off()
            return
        if throttle_value > 0:
            self.headlight.fill_sector('front_right_rim','white')
            self.headlight.fill_sector('front_left_rim','white')
            self.headlight.show()
        elif throttle_value < 0:        
            self.headlight.fill_sector('front_right_rim','red')
            self.headlight.fill_sector('front_left_rim','red')
            self.headlight.show()
        else:
            self.headlight.fill_sector('front_right_rim','off')
            self.headlight.fill_sector('front_left_rim','off')
            self.headlight.show()
    def close(self):
        self.headlight.close()
        super().close()

class BlueButton(GPIO.Button):
    def __init__(self):
        super().__init__('Blue Button', 5)

class ReversingBuzzer(GPIO.Buzzer):
    def __init__(self):
        super().__init__('Reversing Buzzer',17)

class LRIR(GPIO.IRSensor):
    def __init__(self):
        super().__init__('Left Rear IR',27)

class RRIR(GPIO.IRSensor):
    def __init__(self):
        super().__init__('Right Rear IR',26)

if __name__ == "__main__":
    test_dt = ThisDriveTrainWithHeadlights()
    test_sbus = ThisSbusReceiver()
    #test_headlight = ThisHeadlight()
    utime.sleep(1)
    test_dt.close()
    test_sbus.close()
    #test_headlight.close()
    print ('--- AFTER CLOSE --')
    print (ColObjects.ColObj.str_allocated())
    print (module_name, 'finished')
