import os, sys, cv2
import numpy                      as np
import nkOpenCV.load__movieFrames as lmf
import nkOpenCV.detect__ARmarker  as arm


# ========================================================= #
# ===  evaluate__ARmarker.py                            === #
# ========================================================= #

def evaluate__ARmarker( inpFile=None, nARmarker=4, frame_to_use=None ):

    markerType = "aruco.DICT_4X4_50"
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[evaluate__ARmarker.py] inpFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] load image / video                    --- #
    # ------------------------------------------------- #
    resize       = None
    images       = lmf.load__movieFrames( inpFile=inpFile, \
                                          resize=resize, frame_to_use=frame_to_use)
    detected     = [ arm.detect__ARmarker( image=image, markerType=markerType ) \
                     for image in images ]
    nMarkers     = np.array( [ ( dtc[1] ).shape[0] for dtc in detected ] )
    correct      = np.where( nMarkers == nARmarker, 1, 0 )
    rate         = np.sum( correct ) / correct.shape[0]

    # ------------------------------------------------- #
    # --- [3] answer output                         --- #
    # ------------------------------------------------- #
    ret = [ np.sum( correct ), correct.shape[0], rate ]
    print( "correct :: {} / {} = {}".format( *ret ) )
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    nARmarker = 4
    inpFile   = "mov/match_belowdesk.mov"
    frame_to_use = 300
    evaluate__ARmarker( inpFile=inpFile, nARmarker=nARmarker, frame_to_use=frame_to_use )
