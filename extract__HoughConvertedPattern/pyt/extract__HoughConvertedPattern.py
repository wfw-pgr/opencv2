import cv2
import math, os, sys
import numpy as np
import matplotlib.pyplot as plt

# ========================================================= #
# ===  extract__HoughConvertedPattern.py                === #
# ========================================================= #

def extract__HoughConvertedPattern():

    x0_, y0_, ra_, = 0, 1, 2
    
    # jpgFile        = "jpg/bolt_holes.jpg"
    # jpgFile        = "jpg/sockets.jpg"
    jpgFile        = "jpg/ontable.jpg"
    outFile        = jpgFile.replace( ".jpg", "_{0:04}.jpg" )

    # ------------------------------------------------- #
    # --- [0] parameters                            --- #
    # ------------------------------------------------- #
    th1, th2             = 90, 110
    param1, param2       = max( th1,th2 ), 50.0
    minDist, dp          = 0.10, 1.2
    minRadius, maxRadius = 0.05, 0.25
    GaussSize            = 15
    extractMargin        = 1.2

    # ------------------------------------------------- #
    # --- [1] preparation                           --- #
    # ------------------------------------------------- #
    img_bgr   = cv2.imread  ( jpgFile )
    Lx, Ly    = img_bgr.shape[1], img_bgr.shape[0]
    refLength = np.min( [Lx,Ly] )
    minDist   = refLength * minDist
    minRadius = int( refLength * minRadius )
    maxRadius = int( refLength * maxRadius )
    
    # ------------------------------------------------- #
    # --- [1] load jpg picture                      --- #
    # ------------------------------------------------- #
    img_rgb   = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB  )
    img_gray  = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2GRAY )
    img_gauss = cv2.GaussianBlur( img_gray, (GaussSize,GaussSize), 0 )
    img_canny = cv2.Canny( img_gauss, threshold1=th1, threshold2=th2 )
    circles   = cv2.HoughCircles( img_canny, cv2.HOUGH_GRADIENT, minDist=minDist, \
                                  param1=param1, param2=param2, \
                                  dp=dp, minRadius=minRadius, maxRadius=maxRadius )
    if ( circles is not None ):
        circles        = circles[0]
        nCircles       = circles.shape[0]
        for circle in circles:
            x, y, r    = int( circle[0] ), int( circle[1] ), int( circle[2] )
            img_show   = cv2.circle( img_rgb, (x, y), r, (255, 255, 0), 4 )
    else:
        img_show = np.copy( img_canny )
    print( circles.shape )
    print( circles )

    # ------------------------------------------------- #
    # --- [2] extract data                          --- #
    # ------------------------------------------------- #
    if ( circles is not None ):

        halfWidth     = np.ceil( circles[:,ra_] * extractMargin )
        x0, y0        = np.rint( circles[:,x0_] ), np.rint( circles[:,y0_] )
        xFrom, xTill  = x0-halfWidth, x0+halfWidth
        yFrom, yTill  = y0-halfWidth, y0+halfWidth
        xFrom[np.where( xFrom <  1 )] = 1
        xTill[np.where( xTill > Lx )] = Lx
        yFrom[np.where( yFrom <  1 )] = 1
        yTill[np.where( yTill > Ly )] = Ly
        xFrom,xTill   = np.array( xFrom-1, dtype=np.int ), np.array( xTill, dtype=np.int )
        yFrom,yTill   = np.array( yFrom-1, dtype=np.int ), np.array( yTill, dtype=np.int )
        
        for ik in range( nCircles ):
            print( ik )
            print( xFrom[ik], xTill[ik] )
            print( yFrom[ik], yTill[ik] )
            print()
            extractedImage = img_bgr[yFrom[ik]:yTill[ik],xFrom[ik]:xTill[ik],:]
            cv2.imwrite( outFile.format( ik+1 ), extractedImage )

    # plt.imshow( img_show )
    # plt.show()

    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    extract__HoughConvertedPattern()
