# coded by Paula Taylor 20240410
# code to send magnetic heading to attached serial vi usb for PiWars entry
# added reference code to show turning left or right,forward or back  on led display
from microbit import *
compass.calibrate()

while True:
    # non-blocking print to REPL(ay) or to a serial device ONLY after reboot
    # note: tends to lock program when switching to serial devices otherwise.
    bearing=compass.heading()
    # send event every 0.1 seconds can be less but led scroll blocks
    sleep(100)
    readingx = accelerometer.get_x()

    if readingx > 30:
        display.show("R")   ## level up, twisting right
    elif readingx < -30:
        display.show("L")   ## level up, twisting left
    else:
        display.show("-")
    print(str(bearing))
    needle = ((15 - compass.heading()) // 30) % 12
    display.show(Image.ALL_CLOCKS[needle])