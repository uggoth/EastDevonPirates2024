import PicoBotF_v03 as ThisPico
import utime

my_left_headlight = ThisPico.ThisLeftHeadlight().headlight
my_right_headlight = ThisPico.ThisRightHeadlight().headlight

headlights = [my_left_headlight, my_right_headlight]

for headlight in headlights:
    print (headlight.name)
    for i in range(3):
        headlight.on()
        utime.sleep(0.25)
        headlight.off()
        utime.sleep(0.25)

utime.sleep(1)

for headlight in headlights:
    print (headlight.name)
    for i in range(3):
        headlight.red()
        utime.sleep(0.25)
        headlight.off()
        utime.sleep(0.25)
        headlight.green()
        utime.sleep(0.25)
        headlight.off()
        utime.sleep(0.25)
        headlight.blue()
        utime.sleep(0.25)
        headlight.off()
        utime.sleep(0.25)
        headlight.purple()
        utime.sleep(0.25)
        headlight.off()
        utime.sleep(0.25)
