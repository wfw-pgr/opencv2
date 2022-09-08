import cv2
import os, sys
import numpy as np
import nkOpenCV.detect__holePosition as dhp
import nkUtilities.load__constants   as lcn
import nkUtilities.load__pointFile   as lpf
import nkUtilities.save__pointFile   as spf
import nkOpenCV.load__movieFrames    as lmf
import nkOpenCV.put__rectangular     as rec
import nkOpenCV.put__ellipses        as ell
import nkOpenCV.save__imageAsMovie   as sim
import nkOpenCV.extract__rectangularRegion as ext


# ========================================================= #
# ===  extract__CannyHough.py                           === #
# ========================================================= #

def extract__CannyHough():

    x_, y_, rc_ = 0, 1, 2
    n_,i_       = 2, 3
    bgr_colors  = np.array( [ [255,0,0], [0,255,0], [0,0,255] ] )

    inpFile     = "mov/univ_input.mov"
    cnsFile     = "dat/parameter_univ.conf"
    ARmFile     = "dat/ARmarker_univ.dat"
    posFile     = "dat/hole_univ.dat"
    outFile     = "mov/out_univ.mov"
    figSize     = (40.64,66.04)
    scale       = 20.0
    maxDist     = 40
    margin      = np.array([2,2])
    edge_length = (30,30)
    if ( margin is not None ):
        figSize = tuple( list( np.array(figSize) + margin*2 ) )

    if ( scale is not None ):
        figSize = tuple( [ int(val*scale) for val in figSize ] )
        pos     = lpf.load__pointFile( inpFile=posFile, returnType="point" )
        ARm     = lpf.load__pointFile( inpFile=ARmFile, returnType="point" )
        if ( margin is not None ):
            pos[:,0] = pos[:,0] + margin[0]
            pos[:,1] = pos[:,1] + margin[1]
        pos,ARm = pos*scale, (ARm+margin)*scale
        posFile_= posFile.replace( ".", "_." )
        ARmFile_= ARmFile.replace( ".", "_." )
        spf.save__pointFile( outFile=posFile_, Data=pos )
        spf.save__pointFile( outFile=ARmFile_, Data=ARm )
    else:
        posFile_= posFile.replace( ".", "_." )
        ARmFile_= ARmFile.replace( ".", "_." )
    
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

    print( "[extract__CannyHough.py]    #. of images :: {}"  .format( images.shape[0] ) )
    print( "[extract__CannyHough.py] shape of images :: {}\n".format( images.shape    ) )
    nImages = images.shape[0]
    
    # ------------------------------------------------- #
    # --- [2] detect hole position                  --- #
    # ------------------------------------------------- #
    images_         = []
    for ik,img in enumerate(images):
        holepos,circles,image = dhp.detect__holePosition( image  =img, ARmFile=ARmFile_, \
                                                          figSize=figSize, posFile=posFile_, \
                                                          const=const, maxDist=maxDist, \
                                                          returnType="hole-circle-image" )
        image_org = np.copy( image )
        if ( image is not None ):
            centers     = np.array( holepos[:,0:2] )
            colorValues = np.array( holepos[:,2], dtype=np.int64 )
            image       = rec.put__rectangular( image=image, centers=centers, \
                                                colorValues=colorValues, edge_length=edge_length)
            xc          = np.copy( circles[:,x_]  )
            yc          = np.copy( circles[:,y_]  )
            rc          = np.copy( circles[:,rc_] )
            image       = ell.put__ellipses( image=image, xc=xc, yc=yc, rc=rc )
            images_.append( image )

        pieces = []
        if ( image is not None ):
            center_pos  = holepos[:,x_:y_+1]
            length      = 50
            pieces      = ext.extract__rectangularRegion( image=image_org, \
                                                          center_pos=center_pos, \
                                                          length=length )
        for ip,piece in enumerate(pieces):
            if ( not( os.path.exists( "jpg/image{0:04}/".format( ik+1 ) ) ) ):
                os.makedirs( "jpg/image{0:04}/".format( ik+1 ), exist_ok=True )
            ret = cv2.imwrite( "jpg/image{0:04}/extract{1:04}.jpg".format( ik+1, ip+1 ), piece )

    # ------------------------------------------------- #
    # --- [3] extract image                         --- #
    # ------------------------------------------------- #
    if ( len(images_) > 0 ):
        images_  = np.array( images_ )
        ret      = sim.save__imageAsMovie( images=images_, outFile=outFile )
        print( "\n[extract__CannyHough.py]    #. of images :: {}".format( images.shape[0] ) )
        print( "\n[extract__CannyHough.py] shape of images :: {}".format( images.shape    ) )
        print( "outFile :: {}".format( outFile ) )
    else:
        print( "[extract__CannyHough_univ.py] no circles on images is found...." )
    
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    extract__CannyHough()
    
