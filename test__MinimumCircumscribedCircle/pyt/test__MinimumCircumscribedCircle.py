import cv2
import os, sys
import numpy as np


# ========================================================= #
# ===  test__MinimumCircumscribedCircle                 === #
# ========================================================= #

def test__MinimumCircumscribedCircle():

    # ------------------------------------------------- #
    # --- [1] prepare image                         --- #
    # ------------------------------------------------- #

    lower_color = np.array( [130,  80,  80] )
    upper_color = np.array( [200, 255, 255] )
    th1, th2    = 220, 255

    inpFile     = "jpg/balls.jpg"
    outFile     = "jpg/out.jpg"
    
    #  -- [1-1]  prepare image                      --  #
    img_bgr     = cv2.imread  ( inpFile )
    img_hsv     = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2HSV  )
    img_gray    = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2GRAY )
    img_gauss   = cv2.GaussianBlur( img_gray, (5,5), 0 )
    _,img_thres = cv2.threshold( img_gauss, th1, th2, cv2.THRESH_BINARY_INV )
    
    #  -- [1-2]  Noise reduction by Opening-Closing --  #
    element8    = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
    img_input   = cv2.morphologyEx( img_thres, cv2.MORPH_OPEN , element8 )
    img_input   = cv2.morphologyEx( img_input, cv2.MORPH_CLOSE, element8 )

    
    # ------------------------------------------------- #
    # --- [2] find contours                         --- #
    # ------------------------------------------------- #
    contours, hierarchy = cv2.findContours( img_input, cv2.RETR_EXTERNAL, \
                                            cv2.CHAIN_APPROX_SIMPLE )
    contours = list( contours )
    print( " #. of contours :: {}".format( len(contours) ) )

    if ( len(contours) > 0 ):

        contours =   list( contours )
        contours = sorted( contours,  key=cv2.contourArea, reverse=True )

        # 最小外接円を用いて円を検出する
        img_write = np.copy( img_bgr )
        for ik,cnt in enumerate(contours):
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center         = (int(x), int(y))
            radius         = int(radius)
            img_write      = cv2.circle( img_write, center, int(radius*0.9), (0, 0, 255), 2 )
            
        cv2.imwrite( outFile, img_write )
        print( " outFile :: {}".format( outFile ) )
        
    else:
        print( "cannot find contours." )

    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    test__MinimumCircumscribedCircle()
    
