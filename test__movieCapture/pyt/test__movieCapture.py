import os, sys
import cv2
import numpy as np


# ========================================================= #
# ===  test__movieCapture.py                            === #
# ========================================================= #

def test__movieCapture( video_path=None, output_path=None, output_ext="jpg" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( video_path  is None ): sys.exit( "[test__movieCapture.py] video_path == ???" )
    if ( output_path is None ): output_path = "./"
    baseName, input_ext = os.path.splitext( os.path.basename( video_path ) )
    if ( input_ext.strip(".").lower() in [ "mov", "mp4" ] ):
        print( "[test__movieCapture.py] illegal file extention....  ( .mov or .mp4 )  [ERROR] " )
        sys.exit()
    if ( output_ext.strip(".").lower() in [ "jpg", "png", "tiff" ] ):
        print( "[test__movieCapture.py] illegal file extention....  ( .mov or .mp4 )  [ERROR] " )
        sys.exit()
    
    # ------------------------------------------------- #
    # --- [2] load capture                          --- #
    # ------------------------------------------------- #
    cap = cv2.VideoCapture( video_path )
    if ( cap.isOpened() is False ):
        return

    # ------------------------------------------------- #
    # --- [3] prepare for saving                    --- #
    # ------------------------------------------------- #
    base_path  = os.path.join( output_path + baseName )
    os.makedirs( baseName, exist_ok=True )
    base_path_ = os.path.join( base_path, baseName )
    digit      = len( str( int( cap.get( cv2.CAP_PROP_FRAME_COUNT ) ) ) )

    # ------------------------------------------------- #
    # --- [4] devide into images                    --- #
    # ------------------------------------------------- #    
    n = 0
    while True:
        ret, frame = cap.read()
        if ( ret ):
            outFile = base_path_ + "_{}.".format( str(n).zfill(digit) ) + output_ext.strip(".")
            cv2.imwrite( outFile, frame )
            print( outFile, frame.shape )
            n += 1
        else:
            break
    return


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    video_path  = "mov/sample.MOV"
    output_path = "jpg/"
    test__movieCapture( video_path=video_path, output_path=output_path )
