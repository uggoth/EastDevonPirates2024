module_name = 'test_19_B_GPIO_v02.py'

import GPIOPico_v19 as GPIO
ColObjects = GPIO.ColObjects

print (module_name)
print ('------ Allocated GPIOs ---------')
print (GPIO.GPIO.str_allocated())
#dummy1 = GPIOPico.LED('expected to fail',55)
dummy2 = GPIO.GPIOServo('test servo 2', 2)
#dummy4 = GPIOPico.GPIOServo('test servo 4', 2)
#dummy3 = GPIOPico.LED('expected to fail', 52)
print (GPIO.GPIO.str_allocated())
dummy2.close()
print (GPIO.GPIO.str_allocated())
