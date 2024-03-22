module_name = 'test_18_D_tank_steering_V02.py'

import RemoteControl_v15 as RemoteControl
GPIO = RemoteControl.GPIO
import utime

def pos_to_speed(pos):
    if pos is None:
        speed = 0
    else:
        speed = int(int((75 - pos) / 5) * 24)  #  remove jitter
    return speed

print (module_name, 'starting')
print ('before allocation\n', RemoteControl.StateMachine.str_allocated())

front_left_motor = GPIOPico.L298NMotor('Front Left Motor', clk_pin_no=14, anti_pin_no=15)
back_left_motor = GPIOPico.L298NMotor('Back Left Motor', clk_pin_no=12, anti_pin_no=13)
left_side = DriveTrain.Side('Left Side','L',[front_left_motor, back_left_motor])

front_right_motor = GPIOPico.L298NMotor('Front Right Motor', clk_pin_no=16, anti_pin_no=17)
back_right_motor = GPIOPico.L298NMotor('Back Right Motor', clk_pin_no=18, anti_pin_no=19)
right_side = DriveTrain.Side('Right Side','R',[front_right_motor, back_right_motor])

drive_train = DriveTrain.DriveTrain('Drive Train', left_side, right_side)

state_machines = []
state_machines.append(RemoteControl.StateMachine('left_up_down', 'MEASURE', 6))
#state_machines.append(RemoteControl.StateMachine('left_sideways', 'MEASURE', 9))
state_machines.append(RemoteControl.StateMachine('right_up_down', 'MEASURE', 8))
#state_machines.append(RemoteControl.StateMachine('right_sideways', 'MEASURE', 7))

previous = [999]*4

for i in range(20):
    utime.sleep_ms(100)
    for i in range(len(state_machines)):
        sm = state_machines[i]
        speed = pos_to_speed(sm.get_latest())
        if speed != previous[i]:
            previous[i] = speed
            name = sm.name
            if name == 'left_up_down':
                print (name, speed)
                left_side.drive(speed)
            elif name == 'right_up_down':
                print (name, speed)
                right_side.drive(speed)

left_side.stop()
right_side.stop()

for i in range(len(state_machines)):
    print (state_machines[i].name)
    state_machines[i].close()

drive_train.close()

print ('after allocation\n', RemoteControl.StateMachine.str_allocated())
print (module_name, 'finished')