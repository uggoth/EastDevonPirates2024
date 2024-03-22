module_name = 'test_01_E_ultrasonic_v03.py'

import ThisPico_D_v13 as ThisPico
import utime

print (module_name, 'starting')

front_ultrasonic = ThisPico.ThisHCSR04()

print (front_ultrasonic.trigger_object.name, front_ultrasonic.trigger_object.pin_no)
print (front_ultrasonic.echo_object.name, front_ultrasonic.echo_object.pin_no)

distance = front_ultrasonic.millimetres()
utime.sleep(1)
print (front_ultrasonic.name,',  critical distance',front_ultrasonic.critical_distance)

for i in range(10):
    print("Iteration " + str(i+1))
    status = front_ultrasonic.get()
    distance = front_ultrasonic.last_distance_measured
    if distance == 0:
        print (front_ultrasonic.error_message)
    else:
        print("The distance from object is ",distance,"mm,  critical distance is",status)
    utime.sleep(1)

print (module_name, 'finished')
