import numpy as np
import cv2


# ========================================================= #
# ===  resample.py                                      === #
# ========================================================= #

def resample( inpFile = "mov/sample_original.mov", outFile = "mov/sample.mov", resize=None ):
    
    # ------------------------------------------------- #
    # --- [1] resample.py                           --- #
    # ------------------------------------------------- #
    import nkOpenCV.resample__movie as res
    resize        = None
    frames_to_use = 21
    ret           = res.resample__movie( inpFile=inpFile, outFile=outFile, \
                                         resize=resize, frame_to_use=frame_to_use )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    resample()
    
