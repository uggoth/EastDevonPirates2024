from picamera2 import Picamera2
import time
picam2 = Picamera2()
picam2.start_and_capture_file('test.jpg')
picam2.close()
