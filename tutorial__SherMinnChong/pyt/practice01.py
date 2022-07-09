import os, sys
import numpy as np
import cv2


# ========================================================= #
# ===  display image with matplotlib                    === #
# ========================================================= #
def display__opencvImage( img=None, cmap=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        sys.exit( "[practice01.py] img == ???" )
    
    # ------------------------------------------------- #
    # --- [2] display an image                      --- #
    # ------------------------------------------------- #
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow( img, cmap=cmap )
    plt.show()
    return()
    

# ========================================================= #
# ===  preprocessing ( Gaussian Blur + Binary Imaging ) === #
# ========================================================= #
def get__binaryImageWithGaussianBlur( img=None, jpgFile=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice01.py] jpgFIle == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] load image and convert into grayed    --- #
    # ------------------------------------------------- #
    img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

    # ------------------------------------------------- #
    # --- [3] Gaussian Bluring                      --- #
    # ------------------------------------------------- #
    img = cv2.GaussianBlur( img, (5,5), 0 )

    # ------------------------------------------------- #
    # --- [4] get binary image                      --- #
    # ------------------------------------------------- #
    _, coins_binary = cv2.threshold( img, 130, 255, cv2.THRESH_BINARY )
    coins_binary = cv2.bitwise_not( coins_binary )
    return( coins_binary )


# ========================================================= #
# ===  find contour by color of an image                === #
# ========================================================= #
def find__contourByColor( img=None, jpgFile=None, min_area=60, \
                          outFile="out/with_contours.jpg" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice01.py] jpgFIle == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] call findContour                      --- #
    # ------------------------------------------------- #
    binary             = get__binaryImageWithGaussianBlur( img=img )
    contours, hierarcy = cv2.findContours( binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    large_contours     = [ cnt for cnt in contours if cv2.contourArea( cnt ) > min_area ]
    
    # ------------------------------------------------- #
    # --- [3] draw contour and image                --- #
    # ------------------------------------------------- #
    image_and_contours = np.copy( img )
    output             = cv2.drawContours( image_and_contours, large_contours, -1, (255,0,0) )
    cv2.imwrite( outFile, output )
    print( "[find__contourByColor] #. of large contours == {}".format( len( large_contours ) ) )
    return( large_contours )


# ========================================================= #
# ===  detect and notice with rectangular               === #
# ========================================================= #
def notice__withRectangular( img=None, jpgFile=None, min_area=60, \
                             outFile="out/with_rectangulars.jpg"  ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( img is None ):
        if ( jpgFile is None ):
            sys.exit( "[practice01.py] jpgFIle == ???" )
        else:
            img = cv2.imread( jpgFile )

    # ------------------------------------------------- #
    # --- [2] call findContour                      --- #
    # ------------------------------------------------- #
    binary             = get__binaryImageWithGaussianBlur( img=img )
    contours, hierarcy = cv2.findContours( binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    large_contours     = [ cnt for cnt in contours if cv2.contourArea( cnt ) > min_area ]

    # ------------------------------------------------- #
    # --- [3] draw rectangular                      --- #
    # ------------------------------------------------- #
    for cnt in large_contours:
        x, y, w, h = cv2.boundingRect( cnt )
        img        = cv2.rectangle( img, (x,y), (x+w,y+h), (0,255,0), 3 )
    cv2.imwrite( outFile, img )
    print( "[practice01.py] save as {} ".format( outFile ) )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    exeList = ["ex3"]
    
    # ------------------------------------------------- #
    # --- [1] ex1                                   --- #
    # ------------------------------------------------- #
    if ( "ex1" in exeList ):
        jpgFile = "jpg/coins.jpg"
        img     = get__binaryImageWithGaussianBlur( jpgFile=jpgFile )
        display__opencvImage( img=img, cmap="gray" )

    # ------------------------------------------------- #
    # --- [2] ex2                                   --- #
    # ------------------------------------------------- #
    if ( "ex2" in exeList ):
        jpgFile = "jpg/coins.jpg"
        img     = find__contourByColor( jpgFile=jpgFile )
    
    # ------------------------------------------------- #
    # --- [3] ex3                                   --- #
    # ------------------------------------------------- #
    if ( "ex3" in exeList ):
        jpgFile = "jpg/coins.jpg"
        img     = notice__withRectangular( jpgFile=jpgFile )

