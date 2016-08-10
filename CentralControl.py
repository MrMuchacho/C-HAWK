# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:48:48 2016

@author: Christian
"""
from PIDController import PID_Controller

class CentralControl(object):
    
    print PID_Controller(1,1,1,"xController")
    
    x_PIDController=PID_Controller(1,1,1,"xController")
    y_PIDController=PID_Controller(1,1,1,"yController")
    bf_PIDController=PID_Controller(1,1,1,"bfController")
    
    