import numpy as np
import cv2
import os, sys
import nkOpenCV.detect__holePosition as dhp
import nkUtilities.load__constants   as lcn
import nkOpenCV.load__movieFrames    as lmf
import nkOpenCV.put__rectangular     as rec
import nkOpenCV.save__imageAsMovie   as sim

# ========================================================= #
# ===  evaluate__CannyHough.py                          === #
# ========================================================= #

def evaluate__CannyHough():

    x_, y_, rc_ = 0, 1, 2
    n_,i_       = 2, 3
    bgr_colors  = np.array( [ [255,0,0], [0,255,0], [0,0,255] ] )

    inpFile     = "mov/sample_original.mov"
    # inpFile     = "jpg/trapezoidal01.jpg"
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
    frame_to_use = 5
    const        = lcn.load__constants( inpFile=cnsFile )
    if   ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".mov", ".mp4" ] ):
        images   = lmf.load__movieFrames( inpFile=inpFile, resize=resize, \
                                          frame_to_use=frame_to_use )
    elif ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".png", ".jpg" ] ):
        images   = [ cv2.imread( inpFile ) ]

    print( "[evaluate__CannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[evaluate__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    
    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_ = []
    for ik,img in enumerate(images):
        holepos,image = dhp.detect__holePosition( image  =img, ARmFile=ARmFile, \
                                                  figSize=figSize, posFile=posFile, \
                                                  const=const, maxDist=maxDist )
        if ( image is not None ):
            centers     = np.array( holepos[:,0:2] )
            colorValues = np.array( holepos[:,2], dtype=np.int64 )
            image       = rec.put__rectangular( image=image, centers=centers, \
                                                colorValues=colorValues, \
                                                edge_length=edge_length )
            images_.append( image )
        
    # ------------------------------------------------- #
    # --- [3] display image                         --- #
    # ------------------------------------------------- #
    images_ = np.array( images_ )
    ret     = sim.save__imageAsMovie( images=images_, outFile=outFile )
    print( "\n[evaluate__CannyHough.py]    #. of images :: {}".format( images.shape[0] ) )
    print( "\n[evaluate__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    print( "outFile :: {}".format( outFile ) )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    evaluate__CannyHough()
    
