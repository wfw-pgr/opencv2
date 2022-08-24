import cv2, os, sys
import numpy as np

# ========================================================= #
# ===  load figure                                      === #
# ========================================================= #

def load__figure( inpFile=None, returnType="bgr" ):

    # ------------------------------------------------- #
    # --- [0] argument check                        --- #
    # ------------------------------------------------- #    
    if ( inpFile is None ): sys.exit( "[load__figure.py] inpFile == ???" )
    
    # ------------------------------------------------- #
    # --- [1] load figure                           --- #
    # ------------------------------------------------- #
    img_bgr = cv2.imread( inpFile )
    
    # ------------------------------------------------- #
    # --- [2] pre-process for figure                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "bgr"  ):
        return( img_bgr )
    elif ( returnType.lower() == "rgb"  ):
        return( cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB  ) )
    elif ( returnType.lower() == "gray" ):
        return( cv2.cvtColor( img_bgr, cv2.COLOR_BGR2GRAY ) )
    else:
        print( "[load__figure.py] returnType == {}??".format( returnType ) )
        sys.exit()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    
    inpFile = "jpg/coin__onSheet.jpg"
    ret     = load__figure( inpFile=inpFile, returnType="bgr" )
    print( ret.shape )
