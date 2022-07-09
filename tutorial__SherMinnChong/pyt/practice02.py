import os, sys, cv2
import numpy as np
import matplotlib.pyplot as plt


# ========================================================= #
# ===  find contour by binarying                        === #
# ========================================================= #

def find__contourByBinaryImage( img=None, jpgFile=None, threshold=100, maxColor=255 ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice02.py] img / jpgFile == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] graying / gaussian bluring            --- #
    # ------------------------------------------------- #
    img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    img = cv2.GaussianBlur( img, (5,5), 0 )

    # ------------------------------------------------- #
    # --- [3] binarying                             --- #
    # ------------------------------------------------- #
    _, img = cv2.threshold( img, threshold, maxColor, cv2.THRESH_BINARY )
    return( img )



# ========================================================= #
# === find edge by canny method                         === #
# ========================================================= #

def find__edgeByCannyMethod( img=None, jpgFile=None, threshold1=90, threshold2=110 ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice02.py] img / jpgFile == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] graying / gaussian bluring            --- #
    # ------------------------------------------------- #
    img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    img = cv2.GaussianBlur( img, (5,5), 0 )

    # ------------------------------------------------- #
    # --- [3] call canny method                     --- #
    # ------------------------------------------------- #
    img = cv2.Canny( img, threshold1=threshold1, threshold2=threshold2 )
    return( img )


# ========================================================= #
# ===  Hough Line detection                             === #
# ========================================================= #
def find__HoughLine( img    =None, jpgFile=None, threshold_pixel_on_line=70,\
                     threshold1=90, threshold2=110, \
                     outFile="out/with_HoughLine.jpg" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice02.py] img / jpgFile == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] find Hough Line                       --- #
    # ------------------------------------------------- #
    canny = find__edgeByCannyMethod( img, threshold1=threshold1, threshold2=threshold2 )
    lines = cv2.HoughLines( canny, 1, np.pi/180, threshold_pixel_on_line )

    # ------------------------------------------------- #
    # --- [3] convert line into start and end point --- #
    # ------------------------------------------------- #
    print( len(lines) )
    print( lines.shape )
    for line in lines:
        rho, theta = line[0,0], line[0,1]
        a   = np.cos( theta )
        b   = np.sin( theta )
        x0  = a * rho
        y0  = b * rho
        x1  = int( x0 + 1000*(-b) )
        y1  = int( y0 + 1000*( a) )
        x2  = int( x0 - 1000*(-b) )
        y2  = int( y0 - 1000*( a) )
        img = cv2.line( img, (x1,y1), (x2,y2), (0,0,255), 2 )
        print( x1, y1, x2, y2 )
    cv2.imwrite( outFile, img )
    print( "[practice01.py] save as {} ".format( outFile ) )
    return()


# ========================================================= #
# ===  Hough Circle detection                           === #
# ========================================================= #
def find__HoughCircle( img    =None, jpgFile=None, \
                       threshold1=90, threshold2=110, \
                       minDist=110, minRadius=20, maxRadius=120, dp=1.5, \
                       outFile="out/with_HoughCircle.jpg" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice02.py] img / jpgFile == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] find Hough Line                       --- #
    # ------------------------------------------------- #
    canny   = find__edgeByCannyMethod( img, threshold1=threshold1, threshold2=threshold2 )
    circles = cv2.HoughCircles( canny, cv2.HOUGH_GRADIENT, \
                                dp=dp, minDist=minDist, \
                                minRadius=minRadius, maxRadius=maxRadius )
    circles = circles[0]
    nCircles= circles.shape[0]

    # ------------------------------------------------- #
    # --- [3] draw circles                          --- #
    # ------------------------------------------------- #
    if ( circles is None ):
        return()
    if ( len(circles) > 0 ):
        for circle in circles:
            x, y, r = int( circle[0] ), int( circle[1] ), int( circle[2] )
            img     = cv2.circle( img, (x, y), r, (255, 255, 0), 4 )
        cv2.imwrite( outFile, img )
        print( "[practice02.py] outFile :: {} ".format( outFile ) )
        print('number of circles detected: {}'.format( nCircles ) )
    return( circles )

        
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):

    exeList = [ "ex4" ]
    
    if ( "ex1" in exeList ):
        jpgFile = "jpg/ontable.jpg"
        img     = find__contourByBinaryImage( jpgFile=jpgFile, threshold=160 )
        plt.imshow( img, cmap="gray" )
        plt.show()

    if ( "ex2" in exeList ):
        jpgFile = "jpg/ontable.jpg"
        img     = find__edgeByCannyMethod( jpgFile=jpgFile, threshold1=90, threshold2=110 )
        plt.imshow( img, cmap="gray" )
        plt.show()

    if ( "ex3" in exeList ):
        jpgFile = "jpg/ontable.jpg"
        img     = find__HoughLine( jpgFile=jpgFile, threshold_pixel_on_line=110 )

    if ( "ex4" in exeList ):
        jpgFile = "jpg/ontable.jpg"
        circles = find__HoughCircle( jpgFile=jpgFile, minDist=110, \
                                     minRadius=20, maxRadius=120, dp=1.5 )
        print( circles )
