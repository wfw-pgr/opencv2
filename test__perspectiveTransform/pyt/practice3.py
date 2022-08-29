import numpy as np
import cv2
import os, sys


# ========================================================= #
# ===  practice3.py                                     === #
# ========================================================= #

def practice3( inpFile=None, figSize=(1200,900) ):

    # ------------------------------------------------- #
    # --- [1] load image                            --- #
    # ------------------------------------------------- #
    image        = cv2.imread( inpFile )

    # ------------------------------------------------- #
    # --- [2] detect ar marker                      --- #
    # ------------------------------------------------- #
    import nkOpenCV.detect__ARmarker as arm
    markers, ids = arm.detect__ARmarker( image=image )
    ARm_detects  = np.array( ( np.average( markers[:,:,:], axis=1 ) )[ list(ids) ], \
                             dtype=np.float32 )

    # ------------------------------------------------- #
    # --- [3] load settings for armarker            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile     = "dat/ARmarker_pos.dat"
    ARm_designs = np.array( lpf.load__pointFile( inpFile=inpFile, returnType="point" ), \
                            dtype=np.float32 )
    
    # ------------------------------------------------- #
    # --- [4] get Matrix / conversion               --- #
    # ------------------------------------------------- #
    matrix = cv2.getPerspectiveTransform( ARm_detects, ARm_designs )
    image_ = cv2.warpPerspective( image, matrix, figSize )
    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    cv2.imwrite( "jpg/out.jpg", image_ )
    print( "[practice3.py] outFile = jpg/out.jpg " )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile = "jpg/trapezoidal01.jpg"
    practice3( inpFile=inpFile )
    
