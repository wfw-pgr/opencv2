import os, sys, cv2
import numpy                      as np
import nkOpenCV.load__movieFrames as lmf
import nkOpenCV.detect__ARmarker  as arm


# ========================================================= #
# ===  show__detectedARmarker.py                        === #
# ========================================================= #

def show__detectedARmarker( inpFile=None, nARmarker=4, frame_to_use=None, outFile="out.jpg" ):

    markerType   = "aruco.DICT_4X4_50"
    sq_color     = (0,255,0)
    sq_thickness = 4
    fontScale    = 1.0
    black        = (255,0,0)
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[show__detectedARmarker.py] inpFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] load image / video                    --- #
    # ------------------------------------------------- #
    resize       = None
    images       = lmf.load__movieFrames( inpFile=inpFile, \
                                          resize=resize, frame_to_use=frame_to_use)
    image        = images[0]
    # image        = cv2.rotate( image, cv2.ROTATE_90_CLOCKWISE )
    markers, ids = arm.detect__ARmarker( image=image, markerType=markerType )
    for ik,marker in enumerate(markers):
        marker_  = np.concatenate( [ marker[:,:], marker[0,:][None,:] ], axis=0 )
        for ic in range(4):
            pt1      = tuple( [ int(val) for val in marker_[ic  ,:] ] )
            pt2      = tuple( [ int(val) for val in marker_[ic+1,:] ] )
            cv2.line( image, pt1, pt2, color=sq_color, thickness=sq_thickness )

    # ------------------------------------------------- #
    # --- [3] put text on ARmarker                  --- #
    # ------------------------------------------------- #
    x_, y_, z_ = 0, 1, 2
    for ik,marker in enumerate( markers ):
        margin = np.array( [-30,-30] )
        center = np.average( marker, axis=0 )
        org    = tuple( [ int(val) for val in center+margin ] )
        if ( int(ids[ik]) in [ 2 ] ):
            org = org + np.array( [-200,0] )
        if ( int(ids[ik]) in [ 1 ] ):
            org = org + np.array( [-200,+100] )
        text   = "ID={}, ({},{})".format( ids[ik], int(center[x_]), int(center[y_]) )
        cv2.putText( image, text=text, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, \
                     color=black, fontScale=fontScale, thickness=2 )
    print( "[show__detecteARmarker.py] outFile :: {} ".format( outFile ) )

    # ------------------------------------------------- #
    # --- [3] answer output                         --- #
    # ------------------------------------------------- #
    cv2.imwrite( outFile, image )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    nARmarker = 4
    inpFile   = "mov/match_90deg.mov"
    outFile   = "jpg/out.jpg"
    frame_to_use = "first"
    show__detectedARmarker( inpFile=inpFile, nARmarker=nARmarker, frame_to_use=frame_to_use, outFile=outFile )
