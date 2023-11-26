module_name = 'main_zyderbot_v08.py'
description = 'pico only radio controlled for sheep herding'
import ThisPico_A_V30 as ThisPico
ColObjects = ThisPico.ColObjects
import utime
import machine

my_sbus = ThisPico.ThisSbusReceiver()
#print (my_sbus)
my_train = ThisPico.ThisDriveTrain()
my_train.stop()
#print (my_train)
my_headlight = ThisPico.ThisHeadlight()
my_blue_button = ThisPico.BlueButton()
my_buzzer = ThisPico.ReversingBuzzer()
lrir = ThisPico.LRIR()
rrir = ThisPico.RRIR()
my_irs = [lrir, rrir]

headlights_enabled = True

def show(l_colour, r_colour):
    global headlights_enabled
    if headlights_enabled:
        my_headlight.fill_sector('front_left_rim',l_colour)
        my_headlight.fill_sector('front_left_centre','white')
        my_headlight.fill_sector('front_right_rim',r_colour)
        my_headlight.fill_sector('front_right_centre','white')
    else:
         my_headlight.clear()
    my_headlight.show()

def show_red():
    show('red','red')

def show_green():
    show('green','green')

def show_blue():
    show('blue','blue')

def show_white():
    show('white','white')

def show_left():
    show('orange','green')

def show_right():
    show('green','orange')

def show_black():
    my_headlight.clear()
    my_headlight.show()

def do_buzzer(throttle_value, steering_value, switch_value, all_off, flip_flop):
    keep_going = True
    if ((throttle_value < 0) and (switch_value > 0)):
        if all_off:
            octave = 1
            note = 3
        else:
            octave = 2
            note = 7
            keep_going = False
        if flip_flop:
            my_buzzer.play_note(octave,note,0)
        else:
            my_buzzer.note_off()
    else:
        my_buzzer.note_off()
    return keep_going

def do_lights(throttle_value, steering_value, switch_value, all_off, flip_flop):
    if switch_value > 0:
        keep_going = True
        if steering_value < -10:
            show_left()
        elif steering_value > 10:
            show_right()
        elif throttle_value < 0:
            if all_off:
                show_red()
            else:
                keep_going = False
                if flip_flop:
                    show_red()
                else:
                    show_blue()
        else:
            show_white()
    else:
        keep_going = False
        show_black()
    return keep_going

def do_sensors():
    all_off = True
    for sensor in my_irs:
        current = sensor.get()
        if current != 'OFF':
            all_off = False
    return all_off                

sbus_started = False

interval = 50
for i in range(10000):
    utime.sleep_ms(10)
    j = int(i/interval)
    if j%2 == 0:
        show_green()
    else:
        show_blue()
        print ('waiting',i/100)
    throttle_value, steering_value, switch_value = my_sbus.get()
    if throttle_value is not None:
        sbus_started = True
        break

if not sbus_started:
    show_red()
else:
    show_white()

flip_duration = 10
i = 0
flip_flop = False

while True:
    utime.sleep_ms(10)
    throttle_value, steering_value, switch_value = my_sbus.get()
    if ((switch_value < 0) or (not sbus_started)):
        break
    if throttle_value is None:
        continue
    else:
        i += 1
        if i%flip_duration == 0:
            flip_flop = not flip_flop
        all_off = do_sensors()
        do_buzzer(throttle_value, steering_value, switch_value, all_off, flip_flop)
        keep_going = do_lights(throttle_value, steering_value, switch_value, all_off, flip_flop)
        if not keep_going:
            throttle_value = 0
        my_train.drive(throttle_value, steering_value)

print ('------ stopping --------')
show_black()
my_train.stop()
headlights_enabled = True
flash_duration = 0.15
for i in range(5):
    show_red()
    utime.sleep(flash_duration)
    show_green()
    utime.sleep(flash_duration)

my_blue_button.close()
my_headlight.close()
my_train.close()
my_sbus.close()
my_buzzer.close()
for ir in my_irs:
    ir.close()
print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')