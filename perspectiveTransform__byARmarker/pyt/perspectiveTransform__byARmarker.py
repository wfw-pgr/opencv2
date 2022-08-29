import numpy as np
import cv2
import os, sys


# ========================================================= #
# ===  perspectiveTransform__byARmarker.py              === #
# ========================================================= #

def perspectiveTransform__byARmarker( image=None, imgFile=None, \
                                      ARm_designs=None, ARmFile=None, figSize=None, \
                                      outFile=None ):

    # ------------------------------------------------- #
    # --- [1] load image                            --- #
    # ------------------------------------------------- #
    if ( image is None ):
        if ( imgFile is None ):
            sys.exit( "[perspectiveTransform__byARmarker.py] image == ???" )
        else:
            image = cv2.imread( imgFile )
    if ( figSize is None ):
        print( "[perspectiveTransform__byARmarker.py] figSize = ??? " )
        print( "[perspectiveTransform__byARmarker.py] figSize = (1200,900) is used here." )
        figSize = (600,600)

    # ------------------------------------------------- #
    # --- [2] detect AR marker                      --- #
    # ------------------------------------------------- #
    import nkOpenCV.detect__ARmarker as arm
    markers, ids = arm.detect__ARmarker( image=image )
    if ( len( ids ) == 0 ):
        print( "[perspectiveTransform__byARmarker.py] ARm_detects is size 0... " )
        print( "[perspectiveTransform__byARmarker.py] failed to detect AR marker correctly." )
        return( image )
    else:
        ARm_detects  = np.array( ( np.average( markers, axis=1 ) )[ list(ids) ], \
                                 dtype=np.float32 )

    # ------------------------------------------------- #
    # --- [3] load settings for armarker            --- #
    # ------------------------------------------------- #
    if ( ARm_designs is None ):
        if ( ARmFile is None ):
            print( "[perspectiveTransform__byARmarker.py] ARm_designs and ARmFile is None. [ERROR]" )
            sys.exit()
        else:
            import nkUtilities.load__pointFile as lpf
            ARm_designs = np.array( lpf.load__pointFile( inpFile=ARmFile, returnType="point" ), \
                                    dtype=np.float32 )
    else:
        if ( ARm_detects.shape == ARm_designs.shape ):
            print( "[perspectiveTransform__byARmarker.py] different size of ARm_detects / ARm_designs... " )
            print( "[perspectiveTransform__byARmarker.py] failed to detect AR marker correctly.... [CAUTION] " )
            return( image )
            
    # ------------------------------------------------- #
    # --- [4] get Matrix / conversion               --- #
    # ------------------------------------------------- #
    matrix = cv2.getPerspectiveTransform( ARm_detects, ARm_designs )
    image_ = cv2.warpPerspective( image, matrix, figSize )
    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        cv2.imwrite( outFile, image_ )
        print( "[perspectiveTransform__byARmarker.py] outFile = {}".format( outFile ) )
    return( image_ )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    imgFile  = "jpg/trapezoidal01.jpg"
    ARmFile  = "dat/ARmarker_pos.dat"
    outFile  = "jpg/out.jpg"
    figSize  = (1200,900)
    ret      = perspectiveTransform__byARmarker( imgFile=imgFile, ARmFile=ARmFile, \
                                                figSize=figSize )
    # -- write image -- # 
    original = cv2.imread( imgFile )
    original = cv2.resize( original, dsize=figSize )
    image    = cv2.hconcat( [original,ret] )
    cv2.imwrite( outFile, image )

    
