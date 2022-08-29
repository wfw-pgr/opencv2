import cv2, os, sys
import numpy as np

# return :: 

# ========================================================= #
# ===  detect__ARmarker.py                              === #
# ========================================================= #

def detect__ARmarker( image=None, markerType="aruco.DICT_4X4_50", reorder=None ):

    # ------------------------------------------------- #
    # --- [1] argument image check                  --- #
    # ------------------------------------------------- #
    if ( image is None ): sys.exit( "[detect__ARmarker.py] image == ??? " )
    image_ = np.copy( image )
    if ( image_.ndim == 3 ): image_ = cv2.cvtColor( image_, cv2.COLOR_BGR2GRAY )

    # ------------------------------------------------- #
    # --- [2] call aruco ARmaker dictionary         --- #
    # ------------------------------------------------- #
    aruco    = cv2.aruco
    if   ( markerType == "aruco.DICT_4X4_50"  ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_4X4_50  )
    elif ( markerType == "aruco.DICT_5X5_100" ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_5X5_100 )
    else:
        print( "[detect__ARmarker.py] unknown markerType == {}".format( markerType ) )
        print( "[detect__ARmarker.py] markerType :: [ aruco.DICT_4X4_50, aruco.DICT_5X5_100 ]" )
        sys.exit()

    # ------------------------------------------------- #
    # --- [3] detect AR marker                      --- #
    # ------------------------------------------------- #
    corners, ids, rejectedImgPoints = aruco.detectMarkers( image_, markers_dict )
    index    = np.argsort( np.reshape( ids, (-1) ) )
    markers  = np.array( [ corners[iid][0,...] for iid in index ] )
    ids      = np.array( [     ids[iid][0,...] for iid in index ] )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( reorder is not None ):
        markers = markers[ reorder ]
        ids     = ids    [ reorder ]
    return( markers, ids )


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
