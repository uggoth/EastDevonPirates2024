# working version 2024/04/17
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# collection of functions for use in PiWars 2024
# they are absolutely dependent upon the rest of the zyderbot code
# It would be nice to have them in a class but thats not happening this week :)
# Obviously I was wrong
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# The following are valid commands to the ESP32 sensor
# WHOU - retrun hostname
# LINE - return 3 line readings, top, centre and bottom
# LINC - return only the centre line
# GETL - rescan and return 3 line readings
# GETC - rescan and return centre line
# FLA+ - turn the light on
# FLA- - turn the light off
# RSET - reset the ESP32
# BLOB - return the current blob location
# LUMI - return the current camera luminance reading (optimum is 100)
# EXPO - update the current camera exposure 0-1200
# GETB - return current blue blob location
# GETG - return current green blob location
# GETR - return current red blob location
# GETY - return current yellow blob location
# GETW - return current white blob location
# PIDS - return stored pid values
import time
class piwars:
    def __init__(self,pico,esp32,serial_start=0):
        self.camera = esp32    # variable for serial interface to esp32 camera
        self.robot = pico      # variable for serial interface to robot interface controller
        self.serial_no = serial_start
        self.turn_time = 0.2
        self.turn_speed = 20
        self.turn_offset = 0.05
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Routines to run challenge level functions
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # universal configuration routine to setup robot for an autonomous challenge
    def challenge(self):
        # challenges covered Eco-disaster, Lava-palaver and Minesweeper
        print('challenge Not yet implemented')
        
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    
    # start/stop routine
    # when start button pressed, challenge starts after a 3 second delay
    # when start button pressed again, after 3 second delay, challenge is stopped
    def start(self):
        # colins code
        print('start Not yet implemented')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # end of challenge level routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # start of movement routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    
    # routine to send stop message to pico

    def stop(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "STOP" 
        print("STOP command sent:" + command)
        try:
            serial_no_back, feedback, data = self.robot.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad pico interaction ****', err)
        return serial_no_back, feedback, data



    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to send formatted speed control command to pico
    def speedControl(self,lf_motor,lr_motor,rf_motor,rr_motor):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        # format the drive parameters
        lf_motor_string = '{:04.0f}'.format(lf_motor)
        lr_motor_string = '{:04.0f}'.format(lr_motor)
        rf_motor_string = '{:04.0f}'.format(rf_motor)
        rr_motor_string = '{:04.0f}'.format(rr_motor)
        # assemble the complete DRVD command
        command = "DRVD" + lf_motor_string + lr_motor_string + rf_motor_string + rr_motor_string
        print("speed command sent:" + command)
        try:
            serial_no_back, feedback, data = self.robot.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad pico interaction ****', err)
        return serial_no_back, feedback, data

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def turn_control(self,spin):
        # format serial number
       # serial_no_string = '{:04.0f}'.format(serial)
        # format the drive parameter
        spin_string = '{:04.0f}'.format(spin)
        # assemble the complete DRIV command
        command = "DRIV" + spin_string + '00000000'  # 0000 as fore/aft and crab not used
        print("Turn command sent:" + command)
        try:
            serial_no_back, feedback, data = self.robot.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad pico interaction ****', err)
        return serial_no_back, feedback, data

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def turn(self,turn_speed):
        # spin left for 45 degrees
        # this is a timed turn to be replaced with an accelerometer in the future
        self.turn_control(turn_speed)
        time.sleep(.4)
        self.stop()
     
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
    def turn_right(self):
        # spin right for 45 degrees
        # this is a timed turn to be replaced with an accelerometer in the future
        self.turn_control(self.turn_speed)
        time.sleep(self.turn_time*45/self.turn_speed + self.turn_offset)
        self.stop()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def turn_angle(self,angle):
        # spin for a number of degrees
        # this is a timed turn to be replaced with an accelerometer in the future
        self.turn_control(self.turn_speed)
        time.sleep(self.turn_time*angle/self.turn_speed + self.turn_offset)
        self.stop()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def rotate_and_check(self,direction):
        # this command issues rotation commands repeatedly until target in view
        print('rotate_and_check Not yet implemented')

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def rotate_from_zone(self):
        # this method rotates the robot away from the zone it has just left a barrel in
        # this is part of the search for the next barrel
        print('rotate_from_zone Not yet implemented')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # end of movement routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # start of servo routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def lift_barrel(self):
        # this method assumes that the barrel has been captured determined by target size
        # and possibly ultrasound
        # the barrel is lifted
        print('lift_barrel Not yet implemented')

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def lower_barrel(self):
        # this method assumes that the robot is infront of a drop zone
        # the barrel is lowered
        print('lower_barrel Not yet implemented')

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # end of servo routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # start of target routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def get_PID_angle(self,target):
        # the method gets the barrel location and calculates the angle of the direct course
        # to the blob from the current robot heading
        # This is to ensure that the angle is low enough for efficient PID control
        if target == 'SafeZone':
            request = 'GETB'
        elif target == 'ToxicZone':
            request = 'GETY'
        elif target == 'ToxicBarrel':
            request = 'GETR'
        elif target == 'SafeBarrel':
            request = 'GETG'
        target_size, targetx, targety, luminance = self.target_locate(request) 
        # calculate the arcTangent of the simple geometry from the centre of the gantry
        return angle

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def get_barrel(self,target):
        # the method gets the closest barrel location and calculates the angle of the direct course
        # to the barrel from the current robot heading
        # This is to ensure that the angle is low enough for efficient PID control
        if target == 'SafeZone':
            request = 'GETB'
        elif target == 'ToxicZone':
            request = 'GETY'
        elif target == 'ToxicBarrel':
            request = 'GETR'
        elif target == 'SafeBarrel':
            request = 'GETG'
        target_size, targetx, targety, luminance = self.target_locate(request) 
        # calculate the arcTangent of the simple geometry from the centre of the gantry
        return angle



    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def target_PID(self, target):
        # drive to the barrel or zone using PID
        # its location shouldn't change much
        print('target_PID Not yet implemented')

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def robot_on_zone(self):
        # determines if robot is close enough to target zone to stop
        # compares current target position with set coordinates
        # these are all around robot in frame view so four comparisons necessary
        # compare front
        if targetx > target_front_x1 and targetx < target_front_x2  and targety > target_front_y1 and targety < target_front_y2:
       
            return true
        # otherwise return false as not found
        else:
            return false
        
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to send blob location command and return blob location and size
    # a location of zeros is returned if a blob cannot be found or in the case of an error
    def target_locate(self,target_type):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        
        # check that blob request is valid
        if target_type == "GETR":
            command = "GETR"
        elif target_type == "GETB":
            command = "GETB"
        elif target_type == "GETG":
            command = "GETG"
        elif target_type == "GETY":
            command = "GETY"
        else:
            return 0,0,0,0 #  return zeros if not valid
        print("blob command sent:" + command)
        try:
            # request current line position
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
            # convert returned strings to integers
            print(data)
            return int(data[0:4]), int(data[4:8]), int(data[8:12]), int(data[12:])
        except Exception as err:
            print ('**** bad esp32 interaction ****', err)
            # if in error return zeros. 
            return 0,0,0,0

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to send line location command and return location
    # a location of zeros is returned is a line cannot be found or in the case of an error
    def line_locate(self,line_type):
        # format serial number
        #serial_no_string = '{:04.0f}'.format(serial)
        
        # check that line request is valid
        if line_type == "LINT":
            command = "LINT"
        elif line_type == "LINC":
            command = "LINC"
        elif line_type == "GETC":
            command = "GETC"
        elif line_type == "GETL":
            command = "GETL"
        elif line_type == "LINB":
            command = "LINB"
        else:
            return 999,999 #  return high values if not valid
        print("line command sent:" + command)
        try:
            # request current line position
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
            # convert returned strings to integers
            print(data)
            return int(data[0:4]), int(data[4:])
        except Exception as err:
            print ('**** bad esp32 interaction ****', err)
            # if in error return zeros. 
            return 999,999
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to send line location command and return location
    # a location of zeros is returned is a line cannot be found or in the case of an error
    def line_locate2(self,line_type):
        # format serial number
        #serial_no_string = '{:04.0f}'.format(serial)
        
        # check that line request is valid
        if line_type == "LINT":
            command = "LINT"
        elif line_type == "LINC":
            command = "LINC"
        elif line_type == "GETC":
            command = "GETC"
        elif line_type == "GETL":
            command = "GETL"
        elif line_type == "LINB":
            command = "LINB"
        else:
            return 999,999,999,999,999,999 #  return high values if not valid
        print("line command sent:" + command)

        try:
            # request current line position
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
            # convert returned strings to integers
            print(data)
            return int(data[0:4]), int(data[4:8]), int(data[8:12]), int(data[12:16]),int(data[16:20]),int(data[20:])
        except Exception as err:
            print ('**** bad esp32 interaction ****', err)
            # if in error return zeros. 
            return 999,999,999,999,999,999 #  return high values if not valid  
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # end of target routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # start of utilities routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    # small bit of code to make generating serial numbers more concise 
    def serial_num(self):
         
        self.serial_no = self.serial_no+1
        if self.serial_no > 9999:
            self.serial_no=0
        return '{:04.0f}'.format(self.serial_no)
        # return '0000'

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to turn on headlight
    def flashon(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "FLA+" 
        print("FLA+ command sent:" + command)
        try:
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad ESP32 interaction ****', err)
        return serial_no_back, feedback, data
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to turn on headlight
    def flashoff(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "FLA-" 
        print("FLA- command sent:" + command)
        try:
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad ESP32 interaction ****', err)
        return serial_no_back, feedback, data
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to turn on headlight
    def lighton(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "HFWD" 
        print("HFWD command sent:" + command)
        try:
            serial_no_back, feedback, data = self.robot.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad pico interaction ****', err)
        return serial_no_back, feedback, data

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # routine to turn on headlight
    def lightoff(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "HOFF" 
        print("HOFF command sent:" + command)
        try:
            serial_no_back, feedback, data = self.robot.send_command(self.serial_num(), command)
        except Exception as err:
            print ('**** bad pico interaction ****', err)
        return serial_no_back, feedback, data

    # line factors gets the current line factors from the ESP32.
    # this is for testing and calibration only and provides line input to allow them to be changed
    def lineFactors(self):
        # format serial number
        # serial_no_string = '{:04.0f}'.format(serial)
        command = "PIDS"
        print("data command sent:" + command)

        try:
            # request current PID factors
           
            serial_no_back, feedback, data = self.camera.send_command(self.serial_num(), command)
            # convert returned strings to integers. they are in fact 4 figure floating point values with two decimal places
            print(data)
            return float(data[0:4])/100, float(data[4:8])/100,float(data[8:])/100
        except Exception as err:
            print ('**** bad esp32 interaction ****', err)
            # if in error return zeros. 
            return 0,0,0
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # end of utilities routines    
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

