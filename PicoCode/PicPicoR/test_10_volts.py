import GPIOPico_V30 as GPIO

volts_pin = 29
voltmeter = GPIO.Volts('Volt Meter',volts_pin)

print (voltmeter.read())