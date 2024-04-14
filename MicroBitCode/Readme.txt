Instructions for compiling to run on a Microbit.

Please note that the modulus notation for the direction needle will not 
compile on Mu Editor 1.2 on MacOS, but fine on the online python.MicroBit.org 
site and on Thonny 4.1.3 as at 20240410

compass-with-turn-indication-main.py 

Calibrates the compass by twisting in 3-axes until all the display LEDs are lit, 
then after a few seconds delay, gives a smiley on the LEDs, with a 115200 8-n-1 
output of degrees from north to the usb port, whilst using the accelerometer to 
Indicate a right or left turn on the LEDs.

Compass-needle-main.py
 
Is an extension to the above, replacing the accelerometer output with a bar 
Indicator on the LED’s pointing to North. this is a direct copy from the API documents.
 
WARNING does not compile on MU Editor v1.2 as it fails to recognise modulus symbol!

Compass-needle.hex is test code

Compass-needle-2.hex is the operational hex file to be copied to the MicroBit’s 
internal folder.

Paula Taylor East Devon Pirates 20240411

added
 
accelerometer-only-v1-main.py

accelerometer-only-v1.hex


Gives indication of change in direction to LEDS and printed output to serial port.

Paula 20240414 




