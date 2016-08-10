# -*- coding: utf-8 -*-

"""Pattern recognition

This file provides functions to find well-defined patterns in an image
"""

import numpy as np
import cv2

def cornerPointsChess(img):
    """Find chessboard in image
    
    Args:
        img: An openCV image ndarray in a grayscale or color format.
    """
    NBR_COLUMNS = 5
    NBR_ROWS = 5
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    ret, corners = cv2.findChessboardCorners(gray, (NBR_COLUMNS,NBR_ROWS),None)
    
    
    if ret == True:
        print "Chessboard found!"
        #Find left-top corner value && right-bottom corner value
        xalt[0] = round(corners[0][0][0])
        yalt[0] = round(corners[0][0][1])
        xalt[1] = round(corners[NBR_COLUMNS-1][0][0])
        yalt[1] = round(corners[NBR_COLUMNS-1][0][1])
        xalt[2] = round(corners[NBR_COLUMNS*NBR_ROWS-1][0][0])
        yalt[2] = round(corners[NBR_COLUMNS*NBR_ROWS-1][0][1])
        xalt[3] = round(corners[(NBR_COLUMNS-1)*NBR_ROWS][0][0])
        yalt[3] = round(corners[(NBR_COLUMNS-1)*NBR_ROWS][0][1])        
        for i in range(0, 3):
            sumV[i] = xalt[i] + yalt[i]
        minV = min(sumV)
        maxV = max(maxV)
        for i in range(0, 3):
            if minV==sumV:
                x1 = xalt[i], y1 = yalt[i]
            if maxV==sumV:
                x2 = xalt[i], y2 = yalt[i]
        
        print "Endpoints: ("+str(x1)+","+str(y1)+") ; ("+str(x2)+","+str(y2)+")"
    
        # Draw and display the corners (ADD FRAMES)
        cv2.drawChessboardCorners(img, (NBR_COLUMNS,NBR_ROWS), corners,ret)
        print "Print image"

    else:
        print "Chessboard not found!"
        x1=-1,y1=-1,x2=-1,y2=-1
        
    cv2.imshow('img',img)
    cv2.waitKey(1)
        
    return x1,y1,x2,y2