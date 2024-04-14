# accelerometer output only, no magnetometer.
# coded by Paula Taylor 20240414 for PiWars 2024
from microbit import *


# Code in a 'while True:' loop repeats forever
while True:
    readingx = accelerometer.get_x()
    readingy = accelerometer.get_y()
    if readingx < -200:
        display.show(Image.ARROW_W)
    elif readingx > 200:
        display.show(Image.ARROW_E)
    elif readingy < -200:
        display.show(Image.ARROW_S)
    elif readingy > 200:
        display.show(Image.ARROW_N)
    else:
       display.show(Image("+"))
    # Use below code on actual robot
    # to give you sensible values for stationary and movement values
    #x_strength = accelerometer.get_x()
    #print(x_strength)
    #y_strength = accelerometer.get_y()
    #print(x_strength,y_strength)
    # once decided use below to print to serial
    print(readingx," ",readingy)
