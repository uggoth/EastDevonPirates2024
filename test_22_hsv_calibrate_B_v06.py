module_name = 'test_22_hsv_calibrate_B_v05.py'
print (module_name,'starting')

import tkinter as tk
import colorsys
import cv2
import time
from picamera2 import Picamera2
import imutils

def hsv_to_hex(hsv_in): #  hsv_in is an array [h,s,v] 0<h<255
                        #  result is a string of form: '#rrggbb'
        stage_2 = [0] * 3
        for i in range(3):
            stage_2[i] = hsv_in[i] / 255.0
        stage_3 = colorsys.hsv_to_rgb(stage_2[0], stage_2[1], stage_2[2])
        stage_4 = [0] * 3
        for i in range(3):
            stage_4[i] = abs(int(stage_3[i] * 255))
        stage_5 = '#{:02x}{:02x}{:02x}'.format(stage_4[0], stage_4[1], stage_4[2])
        return stage_5
        
class Slider(tk.Scale):
    def callback(self, position):
        # print (self.name, position)
        self.frame.display_swatches()
    def __init__(self, master, frame, name, low, high, x, y, start):
        self.master = master
        self.frame = frame
        self.name = name
        self.my_var = tk.IntVar()
        super().__init__(master, from_=low, to=high, length=500, sliderlength=20,
                         variable=self.my_var, orient=tk.HORIZONTAL, label=name,
                         command = self.callback)
        self.set(start)
        self.place(x=x, y=y)

class Calibrator:
    def __init__(self, master):
        self.master = master
        self.frame_width = 800
        self.frame_height = 700
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.pack()

        x_left = 20
        x_now = x_left
        x_interval = 100
        y_now = 20
        y_interval = 80

        self.hue_low = Slider(master, self, 'Hue Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.saturation_low = Slider(master, self, 'Saturation Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.value_low = Slider(master, self, 'Value Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval * 2
        self.hue_high = Slider(master, self, 'Hue High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.saturation_high = Slider(master, self, 'Saturation High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.value_high = Slider(master, self, 'Value High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.canvas = tk.Canvas(master, height=400, width=100)
        self.low_swatch = self.canvas.create_rectangle(10,10,90,60)
        self.high_swatch = self.canvas.create_rectangle(10,300,90,360)
        self.canvas.place(x=600, y=150)
        self.canvas.itemconfig(self.low_swatch, fill='black')
        self.canvas.itemconfig(self.high_swatch, fill='white')

    def display_swatches(self):
        global timer_previous, loop_counter
        hl = self.hue_low.get()
        sl = self.saturation_low.get()
        vl = self.value_low.get()
        lows_hsv = [hl, sl, vl]
        lows_hsv_2 = (hl, sl, vl)
        lows_rgb_hex = hsv_to_hex(lows_hsv)
        self.canvas.itemconfig(self.low_swatch, fill=lows_rgb_hex)
        hh = self.hue_high.get()
        sh = self.saturation_high.get()
        vh = self.value_high.get()
        highs_hsv = [hh, sh, vh]
        highs_hsv_2 = (hh, sh, vh)
        highs_rgb_hex = hsv_to_hex(highs_hsv)
        self.canvas.itemconfig(self.high_swatch, fill=highs_rgb_hex)
        timer_now = time.time()
        if (timer_now - timer_previous) > timer_interval:
                timer_previous = timer_now
                im00 = picam2.capture_array()
                im10 = imutils.rotate(im00,180)
                im20 = cv2.GaussianBlur(im10, (11, 11), 0)
                im30 = cv2.cvtColor(im20, cv2.COLOR_BGR2HSV)
                im40 = cv2.inRange(im30, lows_hsv_2, highs_hsv_2)
                im50 = cv2.erode(im40, None, iterations=2)
                im60 = cv2.dilate(im50, None, iterations=2)
                cnts = cv2.findContours(im60.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                center = None
                if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        if radius > 10:
                                cv2.circle(im10, (int(x), int(y)), int(radius),
                                        (0, 255, 255), 2)
                                cv2.circle(im10, center, 5, (0, 0, 255), -1)

                loop_counter += 1
                cv2.putText(im10,str(loop_counter),
                            (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,
                            (255,255,0),
                            2,cv2.LINE_AA)
                cv2.imshow('Capture',im10)
        

root = tk.Tk()
root.title('Calibrate CSV')
my_calibrator = Calibrator(root)
cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
timer_previous = time.time()
timer_interval = 2.0
loop_counter = 0
root.mainloop()
