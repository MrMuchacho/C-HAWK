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

class CentralControl(object):
    
    x_PIDController=PID_Controller(1,0.1,2,"xController")
    y_PIDController=PID_Controller(1.5,0.1,2.25,"yController")
    bf_PIDController=PID_Controller(1,0.1,2.25,"bfController")
    
    
    
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
    
    def controlLoop(self):
        drone=libardrone.ARDrone(True)        
        drone.reset()
        drone.speed = 0.1
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
        
        running=True
        counter=0
        while counter<3000:#running:
            key=cv2.waitKey(5)
            if key==32:
                drone.land()
            
            frame=drone.get_image()
            
        # call imageRec
            xlu,ylu,xrd,yrd=patternRecognition.cornerPointsChess(frame)
            if not(xlu==-1 and ylu==-1 and xrd==-1 and yrd==-1):    
            # computeSize
                currentsize=self.computeSize(xlu,ylu,xrd,yrd)
                xAvg = (xlu+xrd)/2.0
                yAvg = (ylu+yrd)/2.0
            # call PIDController
                x_PIDValue=self.x_PIDController.pidControl(self.standardXCoord,xAvg)
                y_PIDValue=self.y_PIDController.pidControl(self.standardYCoord,yAvg)
                bf_PIDValue=self.bf_PIDController.pidControl(self.standardSize,currentsize)
                print "x_PID: "+str(x_PIDValue)
                print "y_PID: "+str(y_PIDValue)
                print "bf_PID: "+str(bf_PIDValue)
                
                self.logFileWrite(logFilePID,str(x_PIDValue))
            # Actuate
                maxPIDValue = max(abs(x_PIDValue),abs(y_PIDValue),abs(bf_PIDValue))
#                self.actuateX(x_PIDValue,drone)
                if abs(x_PIDValue)==abs(maxPIDValue):
                    self.actuateX(x_PIDValue,drone)
                elif abs(y_PIDValue)==abs(maxPIDValue):
                    self.actuateY(y_PIDValue,drone)
                else:
                    self.actuateBF(bf_PIDValue,drone)
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
        
        
    