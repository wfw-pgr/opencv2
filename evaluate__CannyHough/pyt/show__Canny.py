import numpy as np
import cv2
import os, sys
import nkOpenCV.detect__holePosition as dhp
import nkUtilities.load__constants   as lcn
import nkOpenCV.load__movieFrames    as lmf
import nkOpenCV.put__rectangular     as rec
import nkOpenCV.save__imageAsMovie   as sim
import nkOpenCV.detect__circleCannyHough         as cch
import nkOpenCV.put__ellipses        as ell

# ========================================================= #
# ===  show__Canny.py                              === #
# ========================================================= #

def show__Canny():

    x_, y_, r_  = 0, 1, 2
    n_,i_       = 2, 3

    inpFile     = "mov/match_90deg.mov"
    cnsFile     = "dat/parameter.conf"
    ARmFile     = "dat/ARmarker_pos.dat"
    posFile     = "dat/hole.dat"
    outFile     = "mov/out.mov"
    figSize     = (1200,900)
    maxDist     = 20
    edge_length = (50,50)
    
    # ------------------------------------------------- #
    # --- [1] load parameterFile & image            --- #
    # ------------------------------------------------- #
    resize       = None
    frame_to_use = "first"
    const        = lcn.load__constants( inpFile=cnsFile )
    if   ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".mov", ".mp4" ] ):
        images   = lmf.load__movieFrames( inpFile=inpFile, resize=resize, \
                                          frame_to_use=frame_to_use )
    elif ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".png", ".jpg" ] ):
        images   = [ cv2.imread( inpFile ) ]

    print()
    print( "[show__Canny.py] [load movie] " )
    print( "[show__Canny.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[show__Canny.py] shape of images :: {}\n".format( images.shape    ) )
    
    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_    = []
    for ik,img in enumerate( np.copy(images) ):
        xyr, img_canny = cch.detect__circleCannyHough( image=img, **const, \
                                                       returnType="xyr,image" )
        img_canny      = cv2.cvtColor( img_canny, cv2.COLOR_GRAY2BGR )
        image_  = np.copy( img_canny )
        images_.append( image_ )
        
    # ------------------------------------------------- #
    # --- [3] display image                         --- #
    # ------------------------------------------------- #
    images_ = np.array( images_ )
    cv2.imwrite( "jpg/canny.jpg", images_[0,:,:,:] )
    print()
    print( "[show__Canny.py] [save movie] " )
    print( "[show__Canny.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[show__Canny.py] shape of images :: {}\n".format( images.shape    ) )
    ret     = sim.save__imageAsMovie( images=images_, outFile=outFile )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    show__Canny()
    
