import numpy as np
import cv2

# ========================================================= #
# ===  track__ARmarker.py                               === #
# ========================================================= #

def track__ARmarker():

    th1, th2             = 0.30, 0.40
    param1, param2       = max( th1,th2 ), 0.15
    minDist, dp          = 0.10, 1.0
    minRadius, maxRadius = 0.04, 0.12
    GaussSize            = 7
    extractMargin        = 1.2

    # ------------------------------------------------- #
    # --- [1] prepare image                         --- #
    # ------------------------------------------------- #
    aruco         = cv2.aruco
    markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_4X4_50 )

    jpgFile       = "jpg/printed_ARmarker_with_coin3.jpg"
    img_bgr       = cv2.imread  ( jpgFile )
    img_rgb       = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB  )
    img_gray      = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2GRAY )

    Lx, Ly        = img_bgr.shape[1], img_bgr.shape[0]
    refLength     = np.min( [Lx,Ly] )
    th1, th2      =    th1*255.0,    th2*255.0
    param1,param2 = param1*255.0, param2*255.0
    minDist       = refLength * minDist
    minRadius     = int( refLength * minRadius )
    maxRadius     = int( refLength * maxRadius )

    img_gauss  = cv2.GaussianBlur( img_gray, (GaussSize,GaussSize), 0 )
    med_val = np.median(img_gauss)
    sigma   = 0.33  # 0.33
    min_val = int(max(0, (1.0 - sigma) * med_val))
    max_val = int(max(255, (1.0 + sigma) * med_val))
    th1,th2 = min_val, max_val
    param1  = max( th1,th2 )
    
    # ------------------------------------------------- #
    # --- [2] detect AR marker                      --- #
    # ------------------------------------------------- #
    corners, ids, rejectedImgPoints = aruco.detectMarkers( img_gray, markers_dict )
    nMarker    = ids.shape[0]
    marker_cnt = [ np.mean( corners[iid], axis=1 ) for ik,iid in enumerate( ids.ravel() ) ]
    marker_cnt = np.reshape( np.array( marker_cnt ), (nMarker,2) )
    img_ext    = img_gray
    print( marker_cnt )
    
    # ------------------------------------------------- #
    # --- [3] detect coins                          --- #
    # ------------------------------------------------- #
    img_gauss  = cv2.GaussianBlur( img_gray, (GaussSize,GaussSize), 0 )
    img_canny  = cv2.Canny( img_gauss, threshold1=th1, threshold2=th2 )
    circles    = cv2.HoughCircles( img_canny, cv2.HOUGH_GRADIENT, minDist=minDist, \
                                   param1=param1, param2=param2, \
                                   dp=dp, minRadius=minRadius, maxRadius=maxRadius )
    if ( circles is not None ):
        circles        = circles[0]
        nCircles       = circles.shape[0]
        for circle in circles:
            x, y, r    = int( circle[0] ), int( circle[1] ), int( circle[2] )
            img_show   = cv2.circle( img_rgb, (x, y), r, (255, 255, 0), 4 )
    else:
        img_show = img_rgb
    print( circles )

    outFile = "jpg/out.jpg"
    cv2.imwrite( outFile, img_show )


    # ------------------------------------------------- #
    # --- [4] calculate position                    --- #
    # ------------------------------------------------- #


    return()

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    track__ARmarker()
