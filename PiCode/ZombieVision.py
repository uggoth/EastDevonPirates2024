import cv2
import numpy as np
#import math
import csv
import traceback
from time import sleep

__ZOMBIE_DEBUG__ = True     #MUST BE FALSE FOR THE REAL THING
#__ZOMBIE_DEBUG__ = False   #MUST BE FALSE FOR THE REAL THING
class ZombieVision:

    #Get the camera 
    __vid = cv2.VideoCapture(0)
    #Config File Name
    __cfgFileName__ = './zombies.csv'
    __targetsMax__ = 6
    __brightMax__ = 10    #Max number of bright targets we can process

    def __init__(self,cb_LightOn):
        try:
            #HERE Write a log file

            ##################################
            # Paramaters
            ##################################

            #Size, tolerance, Squarness of a bright spot
            self.brightSize = 80    #X and Y must be this size +- Tol
            self.BrightTol = 30
            self.brightSquareness = 10

            #The following are 'about right' default and it is expected that they 
            #are overwritten by data from the config file.
            
            #Crop Size - 0,0 = Top Left
            self.cropYMax = 480
            self.cropYMin = 0
            self.cropXMax = 640
            self.cropXMin = 0
            #Binary threshold  - used for brightest part of image
            self.threshBinLevel = 255
            self.threshBinMax = 250

            #Canny Line detecting
            self.cannyMax = 300.0
            self.cannyMin = 200.0
            #Gausian matrix (must be odd)
            self.gausradiusBright1 = 5
            self.gausradiusBright2 = 5
            #HoughLines https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga8618180a5948286384e3b7ca02f6feeb
            self.houghpixres = 1                #rho (Pixels )
            self.houghangle = np.pi / 180       #theta (Degrees)
            self.houghintersect = None          #threshold
            self.houghmin = 0                   #minLineLength
            self.houghgap = 0                   #maxLineGap   

            self.gaus3radius = 25	#Kadanegaus

            ##################################
            # Paramaters End
            ##################################


            self.targets = np.zeros((self.__brightMax__,3),int)
            self.targetsCount = 0
            self.brightTargets = np.zeros((self.__brightMax__,3),int)
            self.brightTargetsCount = 0
            self.brightSquareMax = self.brightSize + self.BrightTol
            self.brightSquareMin = self.brightSize - self.BrightTol

            self.callbackLight = cb_LightOn

            
            #Read from config file
            self.cfgRead()
        except Exception as e:
            #HERE Log error
            print('__init__:',e)

    def getBrightest(self,frame):
        #Center of brightest part of image 
        try:
            #Remove any we already have
            self.RemoveBrightTargets()
            if not __ZOMBIE_DEBUG__ :
                #Ask are calling code to turn the light on
                self.callbackLight(True)
                #Wait for the humans
                sleep(5)
            #Gaus then global thresh
            gausblurBright = cv2.GaussianBlur(frame,(self.gausradiusBright1,self.gausradiusBright2),0)
            if __ZOMBIE_DEBUG__ :
                cv2.imshow("Gaussian for Brightness",gausblurBright)
            ret3,golbalThreshBright = cv2.threshold(gausblurBright,self.threshBinLevel,self.threshBinMax,cv2.THRESH_BINARY)
            if __ZOMBIE_DEBUG__ :
                cv2.imshow("Global Thresh for Brightness",golbalThreshBright)
            contours, hierarchy = cv2.findContours(golbalThreshBright, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if __ZOMBIE_DEBUG__:
                t=golbalThreshBright.shape
                #brightTarget=np.full((t[0], t[1]), 127, dtype=np.uint8)
                globalThreshContours = cv2.drawContours(frame, contours, -1, (254,0,254), 1)
            #tmpimg = cv2.drawContours(tmp, contours, -1, (254,0,254), 3)
            if len(contours) > 0:
                hierarchy = hierarchy[0]
                cnt = 0
                for component in zip(contours, hierarchy):
                    if cnt < self.__brightMax__ :
                        currentContour = component[0]
                        currentHierarchy = component[1]
                        x,y,w,h = cv2.boundingRect(currentContour)
                        if __ZOMBIE_DEBUG__:
                            cv2.putText(globalThreshContours,str(w) + " " + str(h),(x,y),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_4)
                        #Right Size?
                        if ( w < self.brightSquareMax and w > self.brightSquareMin) and ( h <  self.brightSquareMax and h > self.brightSquareMin):
                            #Square (ish)?
                            #print (x,y,w,h,abs(w-h),x + int (w / 2),y + int (h / 2))
                            diff=abs(w-h)
                            if diff < self.brightSquareness:
                                cv2.rectangle(globalThreshContours,(x,y),(x+w,y+h),(255,255,255),1)
                                self.brightTargets[cnt,0] = (int)(x + int (w / 2))
                                self.brightTargets[cnt,1] = (int)(y + int (h / 2))
                                if __ZOMBIE_DEBUG__:
                                    #print("Bright ",(self.brightTargets[cnt]))
                                    self.crossHair(globalThreshContours,self.brightTargets[cnt])
                                cnt+=1
                self.brightTargetsCount = cnt
                tgc = 0   
                for target in range(0,cnt):
                    # % certintanty - only expecting 1, any more is bad news
                    self.brightTargets[tgc,2] = int(100 / (cnt))
                    tgc+=1
                '''
                            #Hierarchy
                            if currentHierarchy[2] < 0:
                                #Innermost children
                                cv2.rectangle(tmpimg,(x,y),(x+w,y+h),(255,255,255),3)
                                pass
                            elif currentHierarchy[3] < 0:
                                #Outermost parents
                                cv2.rectangle(tmpimg,(x,y),(x+w,y+h),(0,255,0),3)
                            '''
            if not __ZOMBIE_DEBUG__:
                #Request light is turned off
                self.callbackLight(False)
                #Wait for the humans
                sleep(5)
            if __ZOMBIE_DEBUG__ :
                #cv2.imshow("tmpimg",tmpimg)
                cv2.imshow("Brightness contours",globalThreshContours)
                #cv2.imshow("tmpimg",brightTarget)
                #print (" Bright Target Count " + str(self.brightTargetsCount))
        except Exception as e:
            #HERE Log error
            print('__getBrightest__:',e)
            if __ZOMBIE_DEBUG__ :
                print(traceback.format_exc())
                quit()

    def RemoveBrightTargets(self):
        self.brightTargets.fill(0)
        self.brightTargetsCount = 0

    def GetScene(self):
        #Capture and Analyse the scene
        try:
            #Aquire Image
            _, frame = self.__vid.read()
            #HERE - this for fixed image
#            frame = cv2.imread("box.jpg",cv2.IMREAD_COLOR)

            if __ZOMBIE_DEBUG__ :
                frameDisp = frame.copy()
                cv2.imshow("frameDisp", frameDisp)          # Original Frame
            #Crop
            if __ZOMBIE_DEBUG__ :
                Original = frame.copy()
                cv2.imshow("Original", Original)          # Original Frame
            #HERE Colour Detect
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame=self.cropBlack(frame,self.cropYMin,self.cropYMax,self.cropXMin,self.cropXMax)
            if __ZOMBIE_DEBUG__ :
                frameGrey = frame.copy()
                cv2.imshow("frameGrey", frameGrey)          # To Grayscale
            golbalThreshBright = self.getBrightest(frame)
            self.targets = self.ProcessTargets()
            

    ###
#            #Blur and threshold
#            #HERE needs to be paramaraterised for tuning
#            #Gaussian filtering -> Otsu's thresholding after 
#            gausblur2 = cv2.GaussianBlur(frame,(self.gausradiusBright1,self.gausradiusBright2),0)
#            ret3,th3 = cv2.threshold(gausblur2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#            cv2.imshow("Gaussian -> OTSU",th3)

#            #Edge Detect
#            #Canny Edge Detection
#            EdgeDet=cv2.Canny(frame,self.cannymax,self.cannymin)
#            cv2.imshow("edgdet",EdgeDet)

            #Line Detect
    #		linesP = cv2.HoughLinesP(EdgeDet, 1, np.pi / 180, 50, None, 50, 10)
#            lines = cv2.HoughLinesP(EdgeDet, 1, np.pi / 180, 10, None, 10, 10)
            
            #Display it
 #           LineDet = cv2.cvtColor(EdgeDet, cv2.COLOR_GRAY2BGR)
    #        cdstP = np.copy(cdst)
 #           if lines is not None:
 #               for i in range(0, len(lines)):
 #                   l = lines[i][0]
 #                   cv2.line(LineDet, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

        #	cv2.imshow("Source", EdgeDet)
#            cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", LineDet)


            #Square Detect
            

            #Largest Square

            #Squares Inside Largest

            #Brightest Part Of Image

            #Analyse 
                #Is Brightest Inside Building Target? 
            #Repeat if we don't have a target?
                #Limit Time?
                #Best Guess?
        except Exception as e:
            #HERE Log error
            print('GetScene:', e)
            if __ZOMBIE_DEBUG__ :
                quit()

    #Tuning Callbacks
    def cb_threshBinLevel(self,val):
        self.threshBinLevel = (float)(val) 
    def cb_CropYMax(self,val):
        if self.cropYMin < val:
            self.cropYMax = val
    def cb_CropYMin(self,val):
        if self.cropYMax > val:
            self.cropYMin = val
    def cb_CropXMax(self,val):
        if self.cropXMin < val:
            self.cropXMax = val
    def cb_CropXMin(self,val):
        if self.cropXMax > val:
            self.cropXMin = val
    def cb_threshBinMax(self,val):
        if self.threshBinLevel < val:
            self.threshBinMax = val
    def cb_threshBinLevel(self,val):
        if self.threshBinMax > val:
            self.threshBinLevel = val
    def cb_CannyMax(self,val):
        if self.cannyMin < val:
            self.cannyMax = val
    def cb_CannyMin(self,val):
        if self.cannyMax > val:
            self.cannyMin = val

    def tune(self):
        #Tune paramaters - interactive
        try:
            state = 1
            tuning = False
            while state != 0 :
                _, frame = self.__vid.read()            
                cv2.imshow("Original",frame)
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow("Grey",grey)
                #Don't crop the pixels - we might need them, turn them to black
                crop = self.cropBlack(grey,self.cropYMin,self.cropYMax,self.cropXMin,self.cropXMax)
                if state == 1:
                    #HERE Add Rotate ?
                    cv2.imshow("Crop",crop)
                    if (not tuning):
                        blank = np.full((100, 640), 127, dtype=np.uint8)
                        cv2.imshow("Crop Paramaters",blank)
                        cv2.createTrackbar("Max Y","Crop Paramaters",self.cropYMax,480,self.cb_CropYMax)
                        cv2.createTrackbar("Min Y","Crop Paramaters",self.cropYMin,480,self.cb_CropYMin)
                        cv2.createTrackbar("Max X","Crop Paramaters",self.cropXMax,640,self.cb_CropXMax)
                        cv2.createTrackbar("Min X","Crop Paramaters",self.cropXMin,640,self.cb_CropXMin)
                        tuning = True
                    else:
                        cv2.setTrackbarPos("Max Y","Crop Paramaters",self.cropYMax)
                        cv2.setTrackbarPos("Min Y","Crop Paramaters",self.cropYMin)
                        cv2.setTrackbarPos("Max X","Crop Paramaters",self.cropXMax)
                        cv2.setTrackbarPos("Min X","Crop Paramaters",self.cropXMin)
                        keyCode = cv2.waitKey(1)
                        #Pi opencv build has bug for WND_PROP_VISIBLE state
                        if ((cv2.getWindowProperty("Crop", cv2.WND_PROP_VISIBLE) == 0) or (cv2.getWindowProperty("Crop", cv2.WND_PROP_ASPECT_RATIO) < 0) ) or ((cv2.getWindowProperty("Crop Paramaters", cv2.WND_PROP_VISIBLE) == 0) or  (cv2.getWindowProperty("Crop Paramaters", cv2.WND_PROP_ASPECT_RATIO) < 0)):
                            #One of then i sclosed but Pi can't detect which one - kill them both will raise Error
                            try:
                                cv2.destroyWindow("Crop Paramaters")
                            except:
                                pass
                            try:
                                cv2.destroyWindow("Crop")
                            except:
                                pass
                            state += 1
                            tuning = False
                if state == 2:
                    #Gaus then global threshold
                    gausblur2 = cv2.GaussianBlur(crop,(5,5),0)
                    ret3,th3 = cv2.threshold(gausblur2,self.threshBinLevel,self.threshBinMax,cv2.THRESH_BINARY)
                    cv2.imshow("Gaussian -> Global Thresh",th3)
                    if not tuning :
                        cv2.createTrackbar("Threshold Level","Gaussian -> Global Thresh",self.threshBinLevel,255,self.cb_threshBinLevel)
                        cv2.createTrackbar("Threshold Max","Gaussian -> Global Thresh",self.threshBinMax,255,self.cb_threshBinMax)
                        tuning = True
                    else:
                        cv2.setTrackbarPos("Threshold Level","Gaussian -> Global Thresh",self.threshBinLevel)
                        cv2.setTrackbarPos("Threshold Max","Gaussian -> Global Thresh",self.threshBinMax)
                        cv2.waitKey(10) 
                        if ((cv2.getWindowProperty("Gaussian -> Global Thresh", cv2.WND_PROP_VISIBLE) == 0) or (cv2.getWindowProperty("Gaussian -> Global Thresh", cv2.WND_PROP_ASPECT_RATIO) < 0) ):
                            try:
                                cv2.destroyWindow("Gaussian -> Global Thresh")
                            except:
                                pass
                            state += 1
                            tuning = False
                if state == 3:
                    #Canny Edge Detection
                    #grey=grey[self.cropYMin:self.cropYMax,self.cropXMin:self.cropXMax]
                    cannyEdge=cv2.Canny(crop,self.cannyMax,self.cannyMin)
                    cv2.imshow("Canny",cannyEdge)
                    if not tuning:
                        cv2.createTrackbar("Canny Max","Canny",(int)(self.cannyMax),1000,self.cb_CannyMax)
                        cv2.createTrackbar("Canny Min","Canny",(int)(self.cannyMin),1000,self.cb_CannyMin)
                        tuning = True
                    else:
                        cv2.setTrackbarPos("Canny Max","Canny",(int)(self.cannyMax))
                        cv2.setTrackbarPos("Canny Min","Canny",(int)(self.cannyMin))
                        cv2.waitKey(10) 
                        if ((cv2.getWindowProperty("Canny", cv2.WND_PROP_VISIBLE) == 0) or (cv2.getWindowProperty("Canny", cv2.WND_PROP_ASPECT_RATIO) < 0) ):
                            try:
                                cv2.destroyWindow("Canny")
                            except:
                                pass
                            state += 1
                            tuning = False
                if state == 4:
                    state = 0
                    cv2.destroyWindow("Grey")
    

            #print(self.threshBinLevel)
            #Write cfg file
            #self.cfgWrite()

        except Exception as e:
            #HERE Log error
            tuning = True
            print('tune:', e)
            if __ZOMBIE_DEBUG__ :
                print(traceback.format_exc())
                quit()

    def cropBlack(self, grey, YMin, YMax, XMin, XMax):
        #Add black around the image , don't reduce the actual size
        #crop=grey[self.cropYMin:self.cropYMax,self.cropXMin:self.cropXMax]
        crop=grey.copy()
        y,x=crop.shape
        crop[0:YMin,] = 0
        crop[YMax:y-1,] = 0
        crop[0:y-1,0:XMin] = 0
        crop[0:y-1,XMax:x-1] = 0
        return crop

    def cfgRead(self):
        try:
            with open(self.__cfgFileName__, 'r') as file:
                reader = csv.reader(file)
                for  row in reader:
                    cfgArray = row
                self.cropYMax = (int)(cfgArray[0])
                self.cropYMin = (int)(cfgArray[1])
                self.cropXMax = (int)(cfgArray[2])
                self.cropXMin = (int)(cfgArray[3])

                self.threshBinLevel = (int)(cfgArray[4])
                self.threshBinMax = (int)(cfgArray[5])

                 #Canny Line detecting
                self.cannyMax = (float)(cfgArray[6])
                self.cannyMin = (float)(cfgArray[7])
                #Gausian matrix (must be odd)
                self.gausradiusBright1 = (int)(cfgArray[8])
                self.gausradiusBright2 = (int)(cfgArray[9])
                self.houghpixres = (int)(cfgArray[10]) #rho (Pixels )
                self.houghangle = (float)(cfgArray[11])  #theta (Degrees)
                self.houghintersect = None                  #threshold - Note not written
                self.houghmin = (int)(cfgArray[12])    #minLineLength
                self.houghgap = (int)(cfgArray[13])    #maxLineGap 

                self.gaus3radius = cfgArray[14] #Kadanegaus
        except Exception as e:
            #HERE Log
            print ("cfgRead:", e)
            #if __DBUG__ :
            #    quit()       

    def cfgWrite(self):
        try:
            with open(self.__cfgFileName__, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.cropYMax,self.cropYMin, self.cropXMax,self.cropXMin, 
                                self.threshBinLevel,self.threshBinMax,
                                self.cannyMax,self.cannyMin,
                                self.gausradiusBright1,self.gausradiusBright2,self.houghpixres,
                                self.houghangle,self.houghmin, self.houghgap,
                                self.gaus3radius])
        except Exception as e:
            print('cfgWriteL:',e)
            if __ZOMBIE_DEBUG__ :
                quit()
       
    def crossHair(self,image,point):
        try:
            #print(point[0],point[1])
            cv2.line(image,(point[0]-5,point[1]),
                    (point[0]+5,point[1]),
                        (0,255,0), 1)
            cv2.line(image,(point[0],point[1]-5),
                        (point[0],point[1]+5),
                        (0,0,255), 1)
        except Exception as e:
            print('crossHair:',e)
            if __ZOMBIE_DEBUG__ :
                quit()

    def ProcessTargets(self):
        self.targets = self.brightTargets
        self.targetsCount = self.brightTargetsCount
        return self.targets





####################################
#Add to main Code
####################################

#Light On Callback
def zombie_LightOnRequest(on):
    try:
        #Request from ZompieVision to tuen the external light on or off.
        #Singalling that the target should be illuminated
        if on:
            #Turn the External LED on
            print ("ZombieVision requests light on ")
        else:
            #Turn the External LED off
            print ("ZombieVision requests light off ")
    except(e):
        print('zombie_LightOnRequest:',e)
        if __ZOMBIE_DEBUG__ :
                    quit()       


try:     
    zombies = ZombieVision(zombie_LightOnRequest) 
    zombies.tune()
    zombies.cfgWrite()
    while(True):
        zombies.GetScene()
        if zombies.targetsCount > 0 :
            print ("Bright Found " + str(zombies.targetsCount)) 
            print ("numpy X, numpy Y, %% certainty")        
            #ERROR HERE THESE ARE CURRENTLY CROPPED CORDINATES - WILL CONVERT THEM FOR WHOLE IMAGE
            for x in range(0,zombies.targetsCount):
                print (zombies.targets[x])
        cv2.waitKey(10)      

except Exception as e:
    #HERE log it
    print('main:',e)
    if __ZOMBIE_DEBUG__ :
                quit()       
