import cv2
import os, sys
import numpy   as np

# ========================================================= #
# ===  detect__circleCannyHough                         === #
# ========================================================= #

def detect__circleCannyHough( image =None, iGauss=None, threshold=None, param1=None, \
                              dp=1.2, param2=0.2, minDist=0.1, radiusRange=[0.05,0.1], \
                              normalized_parameter=True, returnType="list", message=False ):

    min_, max_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    #  -- [1-1] missing argument check              --  #
    if ( image  is     None ): sys.exit( "[detect__circleCannyHough.py] image == ???" )
    if ( iGauss is not None ):
        if ( not( type( iGauss ) in [ list, tuple, np.ndarray, int ] ) ):
            print( "[detect__circleCannyHough.py] type( iGauss ) == {} ??? "\
                   .format( type(iGauss) ) )
            sys.exit()
        if ( type( iGauss ) == int ):
            iGauss = ( iGauss, iGauss )
    img    = np.copy( image )

    #  -- [1-2] auto parameter determination        --  #
    if ( threshold is None ):
        sigma     = 0.33  # 0.33
        med_val   = np.median( img )
        min_val   = int( max(   0, (1.0 - sigma) * med_val) )
        max_val   = int( max( 255, (1.0 + sigma) * med_val) )
        threshold = np.array( [ min_val, max_val ] )
        if ( normalized_parameter ):
            threshold = threshold / 255.0
   
    if ( param1    is None ):
        param1 = max( threshold[min_], threshold[max_] )

    #  -- [1-3] normalized parameter =>             --  #
    if ( normalized_parameter ):
        threshold   = np.array( 255 * np.array( threshold ), dtype=np.int32 )
        param1      = 255 * param1
        param2      = 255 * param2
        Lx, Ly      = img.shape[1], img.shape[0]
        imgLength   = max( Lx, Ly )
        minDist     =           imgLength * minDist
        radiusRange = np.array( imgLength * np.array( radiusRange ), dtype=np.int32 )

    
    # ------------------------------------------------- #
    # --- [2] pre-processing                        --- #
    # ------------------------------------------------- #
    if   ( img.ndim == 3 ):
        img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    if   ( iGauss is not None ):
        img = cv2.GaussianBlur( img, iGauss, 0 )

    # ------------------------------------------------- #
    # --- [3] Canny-Method & Hough conversion       --- #
    # ------------------------------------------------- #
    #  -- [3-1] Canny-Method                        --  #
    img      = cv2.Canny       ( img, threshold1=threshold[min_], threshold2=threshold[max_] )
    if ( returnType.lower() == "canny" ): return( img )
    
    #  -- [3-2] Hough conversion                    --  #
    circles  = cv2.HoughCircles( img, cv2.HOUGH_GRADIENT, minDist=minDist,
                                 param1=param1, param2=param2, dp=dp, \
                                 minRadius=radiusRange[min_], maxRadius=radiusRange[max_] )

    if ( circles is not None ):
        circles  = circles[0]
    else:
        circles  = None
        if ( message ):
            print( "[detect__circleCannyHough.py] no circles is detected..." )

    if ( message ):
        print( "[detect__circleCannyHough.py] detected circles :: {}".format( circles.shape[0] ) )
 
        
    # ------------------------------------------------- #
    # --- [4] return value                          --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "list"    ):
        ret = [ circles, img ]
        return( ret )
    
    elif ( returnType.lower() == "circles" ):
        return( circles )
    
    elif ( returnType.lower() == "dict"    ):
        ret = { "img_canny":img, "circles":circles }
        return( ret )
    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile            = "jpg/coin__onSheet.jpg"
    image              = cv2.imread( inpFile )
    circles, img_canny = detect__circleCannyHough( image=image, returnType="list" )
    print( circles )
    print( img_canny.shape )

    if ( circles is not None ):
        for circle in circles:
            color      = (255, 255, 0)
            x0, y0, rc = int( circle[0] ), int( circle[1] ), int( circle[2] )
            img_show   = cv2.circle( image, (x0, y0), rc, color, 4 )
    else:
        img_show = np.copy( image )
    cv2.imshow( "circles", img_show )
    cv2.waitKey( int(1e5) )
