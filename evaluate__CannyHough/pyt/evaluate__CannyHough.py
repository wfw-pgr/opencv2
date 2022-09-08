import cv2
import os, sys
import numpy as np
import nkOpenCV.detect__holePosition as dhp
import nkUtilities.load__constants   as lcn
import nkOpenCV.load__movieFrames    as lmf
import nkOpenCV.put__rectangular     as rec
import nkOpenCV.put__ellipses        as ell
import nkOpenCV.save__imageAsMovie   as sim


# ========================================================= #
# ===  evaluate__CannyHough.py                          === #
# ========================================================= #

def evaluate__CannyHough():

    x_, y_, rc_ = 0, 1, 2
    n_,i_       = 2, 3
    bgr_colors  = np.array( [ [255,0,0], [0,255,0], [0,0,255] ] )

    inpFile     = "mov/match_75deg.mov"
    cnsFile     = "dat/parameter.conf"
    ARmFile     = "dat/ARmarker_pos.dat"
    posFile     = "dat/hole.dat"
    outFile     = "mov/out.mov"
    figSize     = (1200,900)
    maxDist     = 25
    edge_length = (50,50)
    
    # ------------------------------------------------- #
    # --- [1] load parameterFile & image            --- #
    # ------------------------------------------------- #
    resize       = None
    frame_to_use = "all"
    const        = lcn.load__constants( inpFile=cnsFile )
    if   ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".mov", ".mp4" ] ):
        images   = lmf.load__movieFrames( inpFile=inpFile, resize=resize, \
                                          frame_to_use=frame_to_use )
    elif ( ( os.path.splitext( inpFile )[1] ).lower() in [ ".png", ".jpg" ] ):
        images   = [ cv2.imread( inpFile ) ]

    print( "[evaluate__CannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[evaluate__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    nImages = images.shape[0]
    
    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_         = []
    success_counter = 0
    for ik,img in enumerate(images):
        holepos,circles,image = dhp.detect__holePosition( image  =img, ARmFile=ARmFile, \
                                                          figSize=figSize, posFile=posFile, \
                                                          const=const, maxDist=maxDist, \
                                                          returnType="hole-circle-image" )
        if ( image is not None ):
            centers     = np.array( holepos[:,0:2] )
            colorValues = np.array( holepos[:,2], dtype=np.int64 )
            image       = rec.put__rectangular( image=image, centers=centers, \
                                                colorValues=colorValues, edge_length=edge_length )
            xc          = np.copy( circles[:,x_]  )
            yc          = np.copy( circles[:,y_]  )
            rc          = np.copy( circles[:,rc_] )
            image       = ell.put__ellipses( image=image, xc=xc, yc=yc, rc=rc )
            images_.append( image )

        if ( ( image is not None ) and ( len(holepos) > 0 ) ):
            sumTrue = np.sum( np.array( holepos[:,2], dtype=np.int64 ) )
            arrSize = holepos.shape[0]
            if ( sumTrue == arrSize ):
                success_counter +=1

            
    # ------------------------------------------------- #
    # --- [3] display image                         --- #
    # ------------------------------------------------- #
    images_  = np.array( images_ )
    ret      = sim.save__imageAsMovie( images=images_, outFile=outFile )
    accuracy = success_counter / float( nImages ) * 100
    print( "\n[evaluate__CannyHough.py]    #. of images :: {}".format( images.shape[0] ) )
    print( "\n[evaluate__CannyHough.py] shape of images :: {}".format( images.shape    ) )
    print( "\n[evaluate__CannyHough.py] success counter :: {}".format( success_counter ) )
    print( "\n[evaluate__CannyHough.py] accuracy        :: {}".format( accuracy        ) )
    
    print( "outFile :: {}".format( outFile ) )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    evaluate__CannyHough()
    
