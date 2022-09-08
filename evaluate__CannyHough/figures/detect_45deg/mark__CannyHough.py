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
# ===  mark__CannyHough.py                              === #
# ========================================================= #

def mark__CannyHough():

    x_, y_, r_  = 0, 1, 2
    n_,i_       = 2, 3

    inpFile     = "mov/match_45deg.mov"
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
    print( "[mark__CannyHough.py] [load movie] " )
    print( "[mark__CannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[mark__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )


    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_    = []
    # 90deg
    # xMin, xMax = 200,  880
    # yMin, yMax =   0, 1920
    # 45deg
    xMin, xMax = 0, 1920
    yMin, yMax = 0, 780
    for ik,img in enumerate( np.copy(images) ):
        xyr, img_canny = cch.detect__circleCannyHough( image=img, **const, \
                                                       returnType="xyr,image" )
        xyr = xyr[ np.where( ( xyr[:,x_] > xMin ) & ( xyr[:,x_] < xMax ) & \
                             ( xyr[:,y_] > yMin ) & ( xyr[:,y_] < yMax ) ) ]
        if ( xyr is None ):
            print( "[mark__CannyHough.py] no circles are detected.... " )
            image_  = np.copy( img )
        else:
            colors  = np.repeat( np.array([0,255,0])[None,:], xyr.shape[0], axis=0 )
            image_  = ell.put__ellipses( image=img, xc=xyr[:,x_], yc=xyr[:,y_], rc=xyr[:,r_], \
                                         colors=colors, thickness=2 )
        
        images_.append( image_ )
        
    # ------------------------------------------------- #
    # --- [3] display image                         --- #
    # ------------------------------------------------- #
    images_ = np.array( images_ )
    print( images_.shape )
    cv2.imwrite( "jpg/out.jpg", images_[0,:,:,:] )
    print()
    print( "[mark__CannyHough.py] [save movie] " )
    print( "[mark__CannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[mark__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    ret     = sim.save__imageAsMovie( images=images_, outFile=outFile )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    mark__CannyHough()
    
