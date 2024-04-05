module_prefix = 'test_06_G_posing_nerf'
module_version = '02'
module_name = module_prefix + '_v' + module_version + '.py'

print (module_name, 'starting')

import tkinter as tk
import pigpio
import time
from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
GPIO_version = data_values['GPIO']
GPIO = SourceFileLoader('GPIO', '/home/pi/ColinPiClasses/' + GPIO_version + '.py').load_module()

class RelayButton:
    def __init__(self, name, master, x_origin, y_origin, relay_pin_no):
        self.master = master
        self.name = name
        self.relay_pin_no = relay_pin_no
        gpio.set_mode(relay_pin_no, pigpio.OUTPUT)
        self.name = name
        self.on = 1
        self.off = 0
        self.state = 0
        self.my_var = tk.IntVar()
        self.my_button = tk.Button(master,
                                   text=name,
                                   command=self.button_clicked)
    def button_clicked(self):
        self.state = 1 - self.state
        if self.state == self.on:
            gpio.write(self.relay_pin_no,1)
            print ('on')
        else:
            gpio.write(self.relay_pin_no,0)
            print ('off')
        
class FireButton:
    def __init__(self, name, master, x_origin, y_origin, my_stepper):
        self.master = master
        self.name = name
        self.my_stepper = my_stepper
        self.my_button = tk.Button(master,
                                   text=name,
                                   command=self.button_clicked)
        self.my_stepper.float()
        self.step_ons = 25
        self.pause_microseconds = 2000
    def button_clicked(self):
        print ('Firing')
        for i in range(self.step_ons):
            self.my_stepper.step_on('ANTI', self.pause_microseconds)
        self.my_stepper.float()

class QuarterButton:
    def __init__(self, name, master, x_origin, y_origin, my_stepper):
        self.master = master
        self.name = name
        self.my_stepper = my_stepper
        self.my_button = tk.Button(master,
                                   text=name,
                                   command=self.button_clicked)
        self.my_stepper.float()
        self.step_ons = 3
        self.pause_microseconds = 2000
    def button_clicked(self):
        print ('Turning')
        for i in range(self.step_ons):
            self.my_stepper.step_on('ANTI', self.pause_microseconds)
        #self.my_stepper.float()

        
class AX12ServoSlider:
    def __init__(self, master, x_origin, y_origin, servo):
        self.master = master
        self.servo = servo
        self.my_name = self.servo.name
        self.my_min = -100
        self.my_max = 100
        self.my_var = tk.IntVar()
        self.my_slider = tk.Scale(master, command=self.slider_moved,
                                    from_=self.my_min,
                                    to=self.my_max,
                                    length=650, sliderlength=20, variable=self.my_var,
                                    orient=tk.HORIZONTAL, label=self.servo.name)
        pos = servo.get_position()
        self.my_slider.set(pos)
        self.my_slider.place(x=x_origin,y=y_origin)
        self.previous = {}
        self.previous['POS'] = 0
        self.ok_colour = '#EEEEEE'
        self.bad_colour = '#FF7777'
        self.clock_label = tk.Label(master, text='<<<  ' + self.servo.clockwise_label, bg=self.ok_colour)
        self.clock_label.place(x=x_origin + 150, y=y_origin)
        self.pos_label = tk.Label(master, text='POS: '+str(self.previous['POS']), bg=self.ok_colour)
        self.pos_label.place(x=x_origin + 300, y=y_origin)
        self.anti_label = tk.Label(master, text=self.servo.anticlockwise_label + '  >>>', bg=self.ok_colour)
        self.anti_label.place(x=x_origin + 450, y=y_origin)
        self.passive = False

    def get_pos_text(self, position):
        return 'POS: ' + str(position)
        
    def move_to_position(self, position):
        self.passive = False
        self.my_slider.set(position)

    def slider_moved(self, value):
        if not self.passive:
            self.servo.move_to(value)

    def changed(self):
        pos = self.servo.get_position()
        if pos != self.previous['POS']:
            self.pos_label.configure(text=get_pos_text(pos))
            self.previous['POS'] = pos
        return pos

    def set_slider_to_position(self, position):
        self.passive = True
        self.my_slider.set(position)
        self.passive = False

    def set_slider_to_current(self):
        self.passive = True
        position = self.servo.get_position()
        self.my_slider.set(position)
        self.passive = False

    def set_label_to_position(self, position):
        self.pos_label.configure(text=self.get_pos_text(position))

    def set_label_to_current(self):
        position = self.servo.get_position()
        self.pos_label.configure(text=self.get_pos_text(position))
        
class Calibrator:

    def __init__(self, master, width, height, servo_list):
        self.master = master
        self.frame_width = width
        self.frame_height = height
        self.servo_list = servo_list
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.owning_object = self
        self.frame.pack()
        self.my_stepper = GPIO.L298NStepperShort('Test Stepper', gpio, 19, 8, 7, 12)
        x_left = 10
        y_top = 10
        x_interval = 50
        y_interval = 70
        self.speed = 50
        self.speed_factor = 2
        self.sliders = {}
        x_now = x_left
        y_now = y_top
        for servo in self.servo_list:
            self.sliders[servo.name] = AX12ServoSlider(self.frame, x_now, y_now, servo)
            y_now += y_interval

#       SPEED

        x_now = x_left
        y_now += y_interval
        self.speed_var = tk.IntVar()
        self.speed_slider = tk.Scale(self.frame, command=self.speed_change,
                                        from_=0,
                                        to=100,
                                        length=350, sliderlength=20, variable=self.speed_var,
                                        orient=tk.HORIZONTAL, label='SPEED')
        self.speed_slider.set(50)
        self.speed_slider.place(x=x_now,y=y_now)

        x_now = x_left
        y_now += y_interval
        self.relay_button = RelayButton('Relay', self.frame, x_now, y_now, 21)
        self.relay_button.my_button.place(x=x_now,y=y_now)
        
        x_now = x_left
        y_now += y_interval
        self.fire_button = FireButton('Fire', self.frame, x_now, y_now, self.my_stepper)
        self.fire_button.my_button.place(x=x_now,y=y_now)
        
        x_now = x_left
        y_now += y_interval
        self.quarter_button = QuarterButton('Quarter Turn', self.frame, x_now, y_now, self.my_stepper)
        self.quarter_button.my_button.place(x=x_now,y=y_now)
        
    def get_speed(self):
        return int(self.speed_var.get()) * self.speed_factor

    def speed_change(self, slider_position):
        self.speed = self.get_speed()


def my_loop(my_calibrator):
    for servo in my_calibrator.servo_list:
        my_calibrator.sliders[servo.name].set_label_to_current()
#    my_calibrator.down_ir.set_text()
#    my_calibrator.volts.set_text()
    root.after(10, my_loop, my_calibrator)   # milliseconds

zombie_arm = ThisPi.ZombieArm()
gpio = pigpio.pi()

root = tk.Tk()
root.title('Nerf Posing')
my_calibrator = Calibrator(root, 750, 590, zombie_arm.servo_list)
root.after(10,my_loop, my_calibrator)
root.mainloop()


zombie_arm.close()
print (module_name, 'finished')
