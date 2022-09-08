import numpy as np
import cv2
import os, sys, time
import nkOpenCV.detect__holePosition as dhp
import nkUtilities.load__constants   as lcn
import nkUtilities.load__pointFile   as lpf
import nkOpenCV.load__movieFrames    as lmf
import nkOpenCV.put__rectangular     as rec
import nkOpenCV.save__imageAsMovie   as sim
import nkOpenCV.detect__circleCannyHough         as cch
import nkOpenCV.put__ellipses        as ell
import nkOpenCV.perspectiveTransform__byARmarker as per

# ========================================================= #
# ===  mark__ProjectCannyHough.py                       === #
# ========================================================= #

def mark__ProjectCannyHough():

    x_, y_, r_  = 0, 1, 2
    n_,i_       = 2, 3

    stock1, stock2, stock3 = 0.0, 0.0, 0.0

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
    ARm_designs  = lpf.load__pointFile( inpFile=ARmFile , dtype=np.float32 )
    const        = lcn.load__constants( inpFile=cnsFile )
    time1s       = time.time()
    if   ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".mov", ".mp4" ] ):
        images   = lmf.load__movieFrames( inpFile=inpFile, resize=resize, \
                                          frame_to_use=frame_to_use )
    elif ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".png", ".jpg" ] ):
        images   = [ cv2.imread( inpFile ) ]
    time1e       = time.time()
    stock1       = time1e - time1s
    
    print()
    print( "[mark__ProjectCannyHough.py] [load movie] " )
    print( "[mark__ProjectCannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[mark__ProjectCannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    
    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_    = []
    xMin, xMax =   0,  1920
    yMin, yMax = 100,  800
    for ik,img in enumerate( np.copy(images) ):

        
        img_   = np.copy( img )
        time2s = time.time()
        img_   = per.perspectiveTransform__byARmarker( image=img_, \
                                                       ARm_designs=ARm_designs, figSize=figSize )
        time2e = time.time()
        stock2 += float( time2e - time2s )
        if ( img_ is None ):
            print( "faield to detect ARmarker" )
            # return( np.array( [] ), None )
        time3s = time.time()
        xyr, img_canny = cch.detect__circleCannyHough( image=np.copy(img_), **const, \
                                                       returnType="xyr,image" )
        time3e = time.time()
        stock3 += float( time3e - time3s )
        # xyr = xyr[ np.where( ( xyr[:,x_] > xMin ) & ( xyr[:,x_] < xMax ) & \
        #                      ( xyr[:,y_] > yMin ) & ( xyr[:,y_] < yMax ) ) ]
        if ( xyr is None ):
            print( "[mark__ProjectCannyHough.py] no circles are detected.... " )
            image_  = np.copy( img_ )
        else:
            colors  = np.repeat( np.array([0,255,0])[None,:], xyr.shape[0], axis=0 )
            image_  = ell.put__ellipses( image=img_, xc=xyr[:,x_], yc=xyr[:,y_], rc=xyr[:,r_], \
                                         colors=colors, thickness=2 )
        
        images_.append( image_ )
        
    # ------------------------------------------------- #
    # --- [3] display image                         --- #
    # ------------------------------------------------- #
    images_ = np.array( images_ )
    print( images_.shape )
    cv2.imwrite( "jpg/out.jpg", images_[0,:,:,:] )
    print()
    print( "[mark__ProjectCannyHough.py] [save movie] " )
    print( "[mark__ProjectCannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[mark__ProjectCannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    time1s       = time.time()
    ret     = sim.save__imageAsMovie( images=images_, outFile=outFile )
    time1e       = time.time()
    stock1      += float( time1e - time1s )

    print( "time for I/O         :: {} (s)".format( stock1 / float( images.shape[0] ) ) )
    print( "time for projection  :: {} (s)".format( stock2 / float( images.shape[0] ) ) )
    print( "time for canny-Hough :: {} (s)".format( stock3 / float( images.shape[0] ) ) )

    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    mark__ProjectCannyHough()
    
