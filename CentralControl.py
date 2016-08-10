# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:48:48 2016

@author: Christian
"""
from PIDController import PID_Controller
import libardrone
import patternRecognition

class CentralControl(object):
    
    x_PIDController=PID_Controller(1,1,1,"xController")
    y_PIDController=PID_Controller(1,1,1,"yController")
    bf_PIDController=PID_Controller(1,1,1,"bfController")
    
    drone=libardrone.ARDrone(True)
    
    #imgrecognition class
    
    #actuator class?
    
    
    
#    standardSize=2
#    standardXCoordLU=22
#    standardYCoordLU=22
#    standardXCoordRD=22 #wird wahrscheinlich nicht gebraucht
#    standardYCoordRD=22 #wird wahrscheinlich nicht gebraucht
    
    def __init__(self,standardXCoordLU,standardYCoordLU,standardXCoordRD,standardYCoordRD):
        self.standardXCoordLU=standardXCoordLU
        self.standardYCoordLU=standardYCoordLU
        self.standardXCoordRD=standardXCoordRD
        self.standardYCoordRD=standardYCoordRD
        self.standardSize=self.computeSize(standardXCoordLU,standardYCoordLU,standardXCoordRD,standardYCoordRD)
        
    
    #Image Recognition returns left upper corner coordinates and right downer corner coordinates
    
    def computeSize(self,xCoordinate_leftUpperCorner,yCoordinate_leftUpperCorner,xCoordinate_rightDownerCorner,yCoordinate_rightDownerCorner):
        return ((xCoordinate_leftUpperCorner-xCoordinate_rightDownerCorner)**2+(yCoordinate_leftUpperCorner-yCoordinate_rightDownerCorner)**2)**0.5
    
    def controlLoop(self):
        self.drone.reset()
        
        self.drone.takeoff()
        
        running=True
        while running:
            frame=self.drone.get_image()
            
        # call imageRec
            xlu,ylu,xrd,yrd=patternRecognition.cornerPointsChess(frame)
        # computeSize
            currentsize=self.computeSize(xlu,ylu,xrd,yrd)
        # call PIDController
            x_PIDValue=self.x_PIDController.pidControl(self.standardXCoordLU,xlu)
            y_PIDValue=self.y_PIDController.pidControl(self.standardYCoordLU,ylu)
            bf_PIDValue=self.bf_PIDController.pidControl(self.standardSize,currentsize)
        # Actuate
            self.actuateX(x_PIDValue)
            self.actuateY(y_PIDValue)
            self.actuateBF(bf_PIDValue)

    drone.land()    
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
        
        
        
        
    