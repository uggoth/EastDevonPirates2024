module_name = 'lava_palaver_v04.py'
# working version 2024/04/17
print (module_name, 'starting')
print ('**** Expects  main_a_s_a_d_v20  to be running on the Pico')
print ('**** Expects  ESP32 to be running as LINES and LINESTA configuration')

# version created by John for the Lava Palver challenge in PiWars 2024
# this version uses the DRVD command on the pico to directly control the wheel speeds

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
CommandStream = ThisPi.CommandStream
AX12Servo = ThisPi.AX12Servo
ColObjects = ThisPi.ColObjects
pico_name = data_values['PICO_NAME']
import time
import pigpio


testlimit = 300
robot_speed = 20

print ('Starting connections ...')
pico_found = False
gpio = pigpio.pi()
pico_handshake = CommandStream.Handshake('PicoR', 4, gpio)
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


import piwars_functions_v03 as piwars
lava = piwars.piwars(my_pico, my_esp32)

print ('Starting line follower ...')

        
    
line_follower = 1 # for testing, there may be multiple challenge routines coded
not_calibrated = 1   # when set to zero, line follower is calibrated
course_not_complete = 1
max_speed = 50    # speed limit
factorP = 1.0

testCount = 0;
time.sleep(1)
while line_follower:
    # dummy routine to be replaced by calibration code
    while not_calibrated:
        print("Calibrating.....")
        not_calibrated = 0

    # set robot moving

    new_speedL = robot_speed
    new_speedR = robot_speed
    new_spin = 0
 
    lava.speedControl(new_speedL,new_speedL,new_speedR,new_speedR)   
    # initialise parameters
    line_errorP = 0.0

    # the following line is there for testing and manual calibration

    while course_not_complete:

        # get line position
        testCount += 1
        print (testCount)
        if testCount >testlimit :
            course_not_complete = 0
            line_follower = 0
        line_start = 0
        line_end = 0
        line_startT = 0
        line_endT = 0    
        line_startB = 0
        line_endB = 0
        line_error = 0

        line_startT, line_endT, line_start, line_end, line_startB, line_endB = lava.line_locate2("GETL")

        if line_start == 0 and line_end == 0:
            lava.stop()
            line_start = previous_line_start
            line_end = previous_line_end
        if line_start > 70 or line_end < 30:
            lava.stop()
            if line_start > 50:
                lava.turn(40)
            else:
                lava.turn(-40)
        else:
            
        # calcuate error, which is the centre position less half the line width  plus the line start
            line_errorP = 50 - (line_start + (line_end-line_start)/2)
             
        # calculate pid value

            pid_value = (factorP*line_errorP) 

        # calculate new speed = current speed + PIDValue

            new_speedL = int(robot_speed - pid_value)
            new_speedR = int(robot_speed + pid_value)               
  
            print("Left:" + str(new_speedL) + " Right:" + str(new_speedR))
        # adjust speed
            lava.speedControl(new_speedL,new_speedL,new_speedR,new_speedR)
            previous_line_start=line_start
            previous_line_end = line_end
            
lava.stop()
lava.lightoff()
lava.flashoff()

my_pico.close()
my_esp32.close()

print (module_name, 'finished')
