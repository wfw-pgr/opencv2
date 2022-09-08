import numpy as np
import cv2
import sys, os
import nkOpenCV.load__movieFrames as lmf


# ========================================================= #
# ===  extract__first.py                                === #
# ========================================================= #

def extract__first():

    inpFile = "mov/match_45deg.mov"
    outFile = "jpg/match_45deg.jpg"
    resize  = None
    frame_to_use = "first"
    images  = lmf.load__movieFrames( inpFile=inpFile, resize=resize, \
                                     frame_to_use=frame_to_use )
    cv2.imwrite( outFile, images[0] )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    extract__first()
    
