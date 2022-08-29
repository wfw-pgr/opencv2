import os, sys, cv2
import numpy as np


# ========================================================= #
# ===  mark__tobeDetected.py                            === #
# ========================================================= #

def mark__tobeDetected( imgFile=None, ARmFile=None, posFile=None, \
                        outFile=None, figSize=None ):
    
    x_, y_, z_ = 0, 1, 2
    thickness  = 3
    rectSize   = 50
    rectColor  = (255,0,0)

    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( imgFile is None ): sys.exit( "[mark__tobeDetected.py] imgFile == ???" )
    if ( ARmFile is None ): sys.exit( "[mark__tobeDetected.py] ARmFile == ???" )
    if ( posFile is None ): sys.exit( "[mark__tobeDetected.py] posFile == ???" )
    if ( figSize is None ): figSize = (600,600)
    
    # ------------------------------------------------- #
    # --- [1] load image                            --- #
    # ------------------------------------------------- #
    image  = cv2.imread( imgFile )
    
    # ------------------------------------------------- #
    # --- [2] perspectiveTransform by AR-marker     --- #
    # ------------------------------------------------- #
    import nkOpenCV.perspectiveTransform__byARmarker as per
    image  = per.perspectiveTransform__byARmarker( image=image, ARmFile=ARmFile, \
                                                   figSize=figSize )
    
    # ------------------------------------------------- #
    # --- [3] mark position to be detected          --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    holePos = lpf.load__pointFile( inpFile=posFile, returnType="point" )
    rect_lu = np.array( holePos[:,x_:y_+1]-rectSize*0.5, dtype=np.int64 )
    rect_rb = np.array( holePos[:,x_:y_+1]+rectSize*0.5, dtype=np.int64 )
    for pt1,pt2 in zip( rect_lu, rect_rb ):
        image  = cv2.rectangle( image, pt1, pt2, rectColor, thickness=3 )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        cv2.imwrite( outFile, image )
        print( "[mark__tobeDetected.py] outFile :: {} ".format( outFile ) )
    return( image )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    imgFile   = "jpg/trapezoidal01.jpg"
    ARmFile   = "dat/ARmarker_pos.dat"
    posFile   = "dat/hole.dat"
    outFile   = "jpg/out.jpg"
    figSize   = (1200,900)
    image     = mark__tobeDetected( imgFile=imgFile, ARmFile=ARmFile, posFile=posFile, \
                                    outFile=outFile, figSize=figSize  )
    
