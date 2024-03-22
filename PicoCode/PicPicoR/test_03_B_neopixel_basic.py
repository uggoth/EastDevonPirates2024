module_name = 'test_03_A_neopixel_basic.py'

import machine
import neopixel
import utime
no_pixels = 7
state_machine = 5
pin=15
mode = 'GRBW'
pixels = neopixel.Neopixel(no_pixels, state_machine, pin, mode)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255,255,255)

for i in range(2):
    for color in [red, green, blue]:
        pixels.fill(color)
        pixels.show()
        utime.sleep(0.5)
pixels.clear()
pixels.show()
utime.sleep(0.5)

for i in range(2):
    for hue in range(0, 65535, 500):
        color = pixels.colorHSV(hue, 255, 255)
        pixels.fill(color)
        pixels.show()
        utime.sleep(0.02)
pixels.clear()
pixels.show()
utime.sleep(0.5)

pixels[0] = white
pixels[2] = red
pixels[4] = green
pixels[6] = blue
pixels.show()
utime.sleep(1.5)

pixels.clear()
pixels.show()
utime.sleep(0.5)
