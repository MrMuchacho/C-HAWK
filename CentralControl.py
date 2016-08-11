# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:48:48 2016

@author: Christian
"""
from PIDController import PID_Controller
from libardrone import libardrone
import patternRecognition 
import time
import cv2
import numpy as np

class CentralControl(object):
    
    x_PIDController=PID_Controller(1,0.0,2.5,"xController")
    y_PIDController=PID_Controller(1.5,0.0,2.25,"yController")
    bf_PIDController=PID_Controller(1,0.0,3,"bfController")
    
    speedRange = [0.15,0.15,0.15]
    maxPIDValue = [100,200,200]
    
    #imgrecognition class
    
    #actuator class?
    
    
    
#    standardSize=2
#    standardXCoordLU=22
#    standardYCoordLU=22
#    standardXCoordRD=22 #wird wahrscheinlich nicht gebraucht
#    standardYCoordRD=22 #wird wahrscheinlich nicht gebraucht
    
    def __init__(self,standardXCoord,standardYCoord,standardSize):
        self.standardXCoord=standardXCoord
        self.standardYCoord=standardYCoord
        self.standardSize=standardSize
        
    
    #Image Recognition returns left upper corner coordinates and right downer corner coordinates
    
    def computeSize(self,xCoordinate_leftUpperCorner,yCoordinate_leftUpperCorner,xCoordinate_rightDownerCorner,yCoordinate_rightDownerCorner):
        return ((xCoordinate_leftUpperCorner-xCoordinate_rightDownerCorner)**2+(yCoordinate_leftUpperCorner-yCoordinate_rightDownerCorner)**2)**0.5
    
    def reciprocalSize(self,desiredValue,actualValue):
        if actualValue<desiredValue:
            return 2*desiredValue-(desiredValue**2)/actualValue
        else:
            return actualValue
    
    def controlLoop(self):
        drone=libardrone.ARDrone(True)        
        drone.reset()
#        drone.speed = 0.1
#        waiting = True

#        while waiting:
#            key=cv2.waitKey(1000)
#            if key==32:
#                waiting = False
#                print "End Waiting"  
#                 
#            else:
#                print "Waiting"
#                print "Key: "+str(key)
#                time.sleep(1)
        frame=drone.get_image()
        cv2.imshow('img',frame)
        print "Draw Image"
        cv2.waitKey(0)
        
#        print "Key: "+str(key)
        drone.takeoff()
        print "Takeoff"
        
        logFilePIDPath="logFilePID.log"
        logFilePID=open(logFilePIDPath,"a")
        logFileCmdPath="logFileCmd.log"
        logFileCmd=open(logFileCmdPath,"a")

        logFilePID.write("\n\n=================================================================================\n")
        logFileCmd.write("\n\n=================================================================================\n")
        
        running=True
        counter=0
        while counter<3000:#running:
            key=cv2.waitKey(5)
            if key==32:
                drone.land()
            
            frame=drone.get_image()
            
        # call imageRec
            xlu,ylu,xrd,yrd=patternRecognition.cornerPointsChess(frame,logFileCmd)
            if not(xlu==-1 and ylu==-1 and xrd==-1 and yrd==-1):    
            # computeSize
                currentsize=self.computeSize(xlu,ylu,xrd,yrd)
                recipSize = self.reciprocalSize(self.standardSize,currentsize)
                xAvg = (xlu+xrd)/2.0
                yAvg = (ylu+yrd)/2.0
            # call PIDController
                x_PIDValue=self.x_PIDController.pidControl(self.standardXCoord,xAvg)
                y_PIDValue=self.y_PIDController.pidControl(self.standardYCoord,yAvg)
                bf_PIDValue=self.bf_PIDController.pidControl(self.standardSize,recipSize)
                print "x_PID: "+str(x_PIDValue)
                self.logFileWrite(logFileCmd,"x_PID: "+str(x_PIDValue))
                print "y_PID: "+str(y_PIDValue)
                self.logFileWrite(logFileCmd,"y_PID: "+str(y_PIDValue))
                print "bf_PID: "+str(bf_PIDValue)
                self.logFileWrite(logFileCmd,"bf_PID: "+str(bf_PIDValue))
                
                self.logFileWrite(logFilePID,str(x_PIDValue)+","+str(y_PIDValue)+","+str(bf_PIDValue))
            # Actuate
                maxPIDValue = max(abs(x_PIDValue),abs(y_PIDValue),abs(bf_PIDValue))
#                self.actuateX(x_PIDValue,drone)
#                if abs(x_PIDValue)==abs(maxPIDValue):
#                    self.actuateX(x_PIDValue,drone)
#                elif abs(y_PIDValue)==abs(maxPIDValue):
#                    self.actuateY(y_PIDValue,drone)
#                else:
#                    self.actuateBF(bf_PIDValue,drone)
                    
                xSpeed,ySpeed,bfSpeed = self.calcSpeed(x_PIDValue,y_PIDValue,bf_PIDValue)
                self.actuateAll(xSpeed,ySpeed,bfSpeed,drone)
            else:
                #drone.hover()
                pass
            
            counter+=1
            
            time.sleep(0.01)
            

        logFilePID.close    
    
        #drone.land()    
        print "Drone landed"     
         
        print("Shutting down...")
        drone.halt()
        print("Ok.")
            
        
    def actuateX(self, x_PIDValue,drone):
        drone.speed = 0.1
        if x_PIDValue>0:
            print "Turn left"
            drone.turn_left()
        elif x_PIDValue<0:
            print "Turn right"
            drone.turn_right()
        else:
            pass
        time.sleep(0.1)

    def actuateY(self, y_PIDValue,drone):
        drone.speed = 0.1
        if y_PIDValue>0:
            print "Move up"
            drone.move_up()
        elif y_PIDValue<0:
            print "Move down"
            drone.move_down()
        else:
            pass
        time.sleep(0.1)
        
    def actuateBF(self, bf_PIDValue,drone):
        drone.speed = 0.1
        if bf_PIDValue>0:
            print "Move forward"
            drone.move_forward()
        elif bf_PIDValue<0:
            print "Move backward"
            drone.move_backward()
        else:
            pass
        time.sleep(0.1)

    def calcSpeed(self,x_PIDValue,y_PIDValue,bf_PIDValue):
        # x-speed: change sign PIDValue>0 <=> speed<0
        if abs(x_PIDValue)>self.maxPIDValue[0]:        
            xSpeed=-np.sign(x_PIDValue)*self.speedRange[0]
        else:
            xSpeed=-x_PIDValue/self.maxPIDValue[0]*self.speedRange[0]
        # y-speed: keep sign PIDValue>0 <=> speed>0
        if abs(y_PIDValue)>self.maxPIDValue[1]:        
            ySpeed=np.sign(y_PIDValue)*self.speedRange[1]
        else:
            ySpeed=y_PIDValue/self.maxPIDValue[1]*self.speedRange[1]
        # bf-speed: change sign PIDValue>0 <=> speed<0
        if abs(bf_PIDValue)>self.maxPIDValue[2]:        
            bfSpeed=-np.sign(bf_PIDValue)*self.speedRange[2]
        else:
            bfSpeed=-bf_PIDValue/self.maxPIDValue[2]*self.speedRange[2]
        return xSpeed,ySpeed,bfSpeed
        
        
    def actuateAll(self,xSpeed,ySpeed,bfSpeed,drone):
        print "z-Speed:"+str(-bfSpeed)+", x-Speed: "+str(xSpeed)+", y-Speed: "+str(ySpeed)
        drone.at(libardrone.at_pcmd, True, 0, bfSpeed, ySpeed, xSpeed)
       
    def logFileWrite(self,file,msg):
        file.write("%s,%s\n" % (str(time.time()), msg))
        
  #  logfile = '/var/log/logfile.log'

## function to save log messages to specified log file
#def log(msg):
#
#  # open the specified log file
#  file = open(logfile,"a")
#
#  # write log message with timestamp to log file
#  file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
#
#  # close log file
#  file.close


control=CentralControl(320,180,80)     #115
control.controlLoop()
        
        
    