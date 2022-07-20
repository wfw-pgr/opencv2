import cv2, os, sys
import numpy as np


# ========================================================= #
# ===  detect__ARmarker.py                              === #
# ========================================================= #

def detect__ARmarker( img_gray=None, markerType="aruco.DICT_4X4_50" ):

    # ------------------------------------------------- #
    # --- [0] argument check                        --- #
    # ------------------------------------------------- #
    if ( img_gray is None ): sys.exit( "[detect__ARmarker.py] img_gray == ??? " )

    # ------------------------------------------------- #
    # --- [1] call aruco ARmaker dictionary         --- #
    # ------------------------------------------------- #
    aruco    = cv2.aruco
    if   ( markerType == "aruco.DICT_4X4_50"  ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_4X4_50  )
    elif ( markerType == "aruco.DICT_5X5_100" ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_5X5_100 )
    else:
        print( "[detect__ARmarker.py] unknown markerType == {}".format( markerType ) )

    # ------------------------------------------------- #
    # --- [2] detect AR marker                      --- #
    # ------------------------------------------------- #
    corners, ids, rejectedImgPoints = aruco.detectMarkers( img_gray, markers_dict )
    nMarker    = ids.shape[0]
    marker_cnt = np.array( [ np.reshape( corners[iid], (4,2) ) for ik,iid in enumerate( ids.ravel() ) ] )
    ids_cnt    = np.array( [ np.reshape( ids[iid]    , (1, ) ) for ik,iid in enumerate( ids.ravel() ) ] )
    return( marker_cnt, ids_cnt )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile    = "jpg/coin__onSheet.jpg"
    img_gray   = cv2.cvtColor( cv2.imread( inpFile ), cv2.COLOR_BGR2GRAY )
    marker,ids = detect__ARmarker( img_gray=img_gray )
    print( marker )
    print( marker.shape )
    print( ids )
    print( ids.shape )
