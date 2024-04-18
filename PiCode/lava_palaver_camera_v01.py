module_name = 'lava_palaver_camera_v01.py'
print (module_name,'starting')
print ('expects main_a_s_a_d to be running on the Pico')
print ('expects L0cost_robot_01_07 to be running on the ESP32')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ColObjectsVersion = data_values['ColObjects']
col_objects_name = '/home/pi/ColinPiClasses/' + ColObjectsVersion + '.py'
ColObjects = SourceFileLoader('ColObjects', col_objects_name).load_module()
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py').load_module()
import time
import sys
import pigpio
gpio = pigpio.pi()


# general parameters

robot_speed = 20
robot_speed_increase = 10
delay=4
serial_no = 1
max_speed = 50    # speed limit
factorP = 1.0
testLimit = 600   # runaway limiter 200 is about 3.5 metres

# I don't know what pwren is
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)

# start button setup
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# setup connections to pico and esp32-cam
print ('Starting connections ...')
pico_id = 'PICOA'
pico_found = False
gpio = pigpio.pi()
pico_handshake = CommandStream.Handshake('picoa hs', 4, gpio)
my_pico = CommandStream.Pico(pico_name, gpio, pico_handshake)
if my_pico.name != pico_name:
    print ('**** Expected Pico:', pico_name, 'Got:', my_pico.name,'****')
else:
    print ('Connected to Pico OK')
    print (my_pico)
    pico_found = True

esp32_found = False
expected_esp32 = 'LINES'
esp32_handshake = CommandStream.Handshake('ESP32', 18, gpio)
my_esp32 = CommandStream.Pico(expected_esp32, gpio, esp32_handshake)
if my_esp32.name != expected_esp32:
    print ('**** Expected ESP32:', expected_esp32, 'Got:', my_esp32.name,'****')
else:
    print ('Connected to ESP32 OK')
    print (my_esp32)
    esp32_found = True
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    

import piwars_functions_v04 as piwars
lava = piwars.piwars(my_pico, my_esp32)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

print(f"Initialised ({time.time() - t:.1f}s)")
print ('Now waiting for blue button')

while True:
    if wait_for_blue(blue_button, 500000):
        print ('Blue button pressed. Starting ...')
    else:
        print ('Blue button not pressed. Start again')
        continue
    # initialise parameters
    line_errorP = 0.0 # original pid proportional
    testCount = 0     # runaway couter
    testLimiter = testLimit  # runaway limiter 200 is about 3.5 metres
    course_not_complete = 1   # loop terminator
    endtest = 0        # test counter for end of course

    # set robot moving

    new_speedL = robot_speed
    new_speedR = robot_speed
    robot_speed_dynamic = robot_speed

    lava.speedControl(new_speedL,new_speedL,new_speedR,new_speedR)    

    while course_not_complete:

        testCount += 1
        print (testCount)
        if testCount > testlimiter :    # check for runaway condition
            course_not_complete = 0
        line_start = 0
        line_end = 0
        line_startT = 0
        line_endT = 0    
        line_startB = 0
        line_endB = 0
        line_error = 0
       # get line position
        line_startT, line_endT, line_start, line_end, line_startB, line_endB = lava.line_locate2("GETL")
        
        # if continuous blank black surface then end run
        if line_startT ==0 and line_endT == 0 and line_start == 0 and line_end == 0 and line_startB == 0 and line_endB == 0:
            endtest=+1
            if endtest == 5:
                course_not_complete = 0

        if line_start == 0 and line_end == 0:
            lava.stop()
            robot_speed_dynamic = robot_speed
            line_start = previous_line_start
            line_end = previous_line_end
            if line_start > 50:
                lava.turn(40)
            else:
                lava.turn(-40)
        if line_start > 70 or line_end < 30:
            lava.stop()
            robot_speed_dynamic = robot_speed
            if line_start > 50:
                lava.turn(40)
            else:
                lava.turn(-40)
        else:
            endtest = 0 # still following a white line
        # calcuate error, which is the centre position less half the line width  plus the line start
            line_errorP = 50 - (line_start + (line_end-line_start)/2)
            
        # prepare  to increase speed if tight to white line
            if line_errorP < 5:
                robot_speed_dynamic = robot_speed + robot_speed_increase
            else:
                robot_speed_dynamic = robot_speed
            
        # calculate pid value
            pid_value = (factorP*line_errorP) 

        # calculate new speed = current speed + PIDValue
            new_speedL = int(robot_speed_dynamic - pid_value)
            new_speedR = int(robot_speed_dynamic + pid_value)               
        
            print("Left:" + str(new_speedL) + " Right:" + str(new_speedR))
        # adjust speed
            lava.speedControl(new_speedL,new_speedL,new_speedR,new_speedR)
            previous_line_start=line_start
            previous_line_end = line_end
    
    continue

lava.stop()
lava.lightoff()
lava.flashoff()

my_pico.close()
my_esp32.close()
print (module_name, 'finished')
