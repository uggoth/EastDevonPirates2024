ZyderBot 11

Pi:   BENJI
Pico: R

Working directory is ColinThisPi
Copy new stuff into ColinBENJI then git push

startup.sh runs main program

-------------- integration ------------------------

lsusb
pico shows up as:  MicroPython Board in FS mode
ESP32 shows up as: QinHeng Electronics CH340 serial converter

ls /dev/tty*
pico shows up as:   /dev/tty/ACM0
ESP32 shows up as:  /dev/tty/USB0 (or possibly USB1)

Use Thonny on Pi for Pico. Works perfectly
Use Arduino 1.8.19 on Pi for ESP32. Compile fails, but serial monitor works
Use Arduino 2.3.0 on PC. Works perfectly (but not available for AMD architecture)

-------------- handshake test ---------------------

handshake pin on Pi is declared:
    pin_no = 18
    gpio.set_mode(pin_no, pigpio.INPUT)
    gpio.set_pull_up_down(pin_no, pigpio.PUD_UP)

handshake pin on ESP32 is declared:
    const int HANDSHAKE_PIN = 12;
    pinMode(HANDSHAKE_PIN, OUTPUT);

ESP32 sets handshake pin HIGH to signal ready to receive a command
sets LOW to indicate busy

Pi reads high pin as 1
low pi as 0
waits for 1 for 1 second, then gives up

Run  /home/pi/EastDevonPirates2024/ESP32CAMCode/HandshakeTestA/HandshakeTestA.ino on the ESP32
Run  /home/pi/ColinPiTests/test_15_A_handshake_esp32.py on the Pi
(Note: ColinPiTests is a GitHub repository to facilitate transfers)

-------------- command stream testing -------------

Run  main_test_command_stream_B_v02.py  on the Pico
Run  /home/pi/ColinThisPi/main_double_test_v01.py  on the Pi
Run  /home/pi/EastDevonPirates2024/ESP32CAMCode/CommandProtocolTestA/CommandProtocolTestA.ino on the ESP32
(Note: EastDevonPirates2024 is a GitHub repository to facilitate transfers)
Turns headlights on and off with Pico
Would turn flashlight on and off on ESP32 if it worked
