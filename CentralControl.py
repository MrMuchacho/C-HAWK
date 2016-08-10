# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:48:48 2016

@author: Christian
"""
import PIDController

class CentralControl(object):
    
    x_PIDController=PIDController(1,1,1,"xController")
    y_PIDController=PIDController(1,1,1,"yController")
    bf_PIDController=PIDController(1,1,1,"bfController")
    
    