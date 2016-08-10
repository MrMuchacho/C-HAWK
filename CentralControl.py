# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:48:48 2016

@author: Christian
"""
from PIDController import PID_Controller
from libardrone import libardrone
import patternRecognition 
import time

class CentralControl(object):
    
    x_PIDController=PID_Controller(1,1,1,"xController")
    y_PIDController=PID_Controller(1,1,1,"yController")
    bf_PIDController=PID_Controller(1,1,1,"bfController")
    
    
    
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
        
       # self.drone.takeoff()
        
        running=True
        counter=0
        while counter<3000:#running:
        
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
            # Actuate
                self.actuateX(x_PIDValue)
                self.actuateY(y_PIDValue)
                self.actuateBF(bf_PIDValue)
                break
            else:
                #drone.hover()
                pass
            
            counter+=1
            
            time.sleep(0.01)

        #drone.land()    
        print "Drone landed"     
         
        print("Shutting down...")
        drone.halt()
        print("Ok.")
            
        
    def actuateX(self, x_PIDValue):
        pass

    def actuateY(self, y_PIDValue):
        pass
        
    def actuateBF(self, bf_PIDValue):
        pass
        

control=CentralControl(320,180,115)
control.controlLoop()
        
        
    