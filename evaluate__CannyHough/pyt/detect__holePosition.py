import cv2, os, sys
import numpy as np
import nkOpenCV.detect__circleCannyHough         as cch
import nkOpenCV.perspectiveTransform__byARmarker as per
import nkUtilities.load__pointFile               as lpf
import nkBasicAlgs.search__nearestPoint          as snp


# ========================================================= #
# ===  detect__holePosition.py                          === #
# ========================================================= #

def detect__holePosition( image=None, imgFile=None, figSize=None, const=None, maxDist=None, \
                          ARm_designs=None, ARmFile=None, posFile=None ):

    x_, y_, z_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( image is None ):
        if ( imgFile is None ):
            sys.exit( "[detect__holePosition.py] image == ???" )
        else:
            image = cv2.imread( imgFile )
    if ( ARm_designs is None ):
        if ( ARmFile is None ):
            sys.exit( "[detect__holePosition.py] ARm_desings == ???" )
        else:
            ARm_designs = lpf.load__pointFile( inpFile=ARmFile , dtype=np.float32 )
    if ( figSize is None ):
        sys.exit( "[detect__holePosition.py] figSize == ???" )
    if ( posFile is None ):
        sys.exit( "[detect__holePosition.py] posFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] perspectiveTransform                  --- #
    # ------------------------------------------------- #
    image_ = per.perspectiveTransform__byARmarker( image=image, ARm_designs=ARm_designs, \
                                                   figSize=figSize )
    if (  )
    
    # ------------------------------------------------- #
    # --- [3] Canny-Hough Conversion                --- #
    # ------------------------------------------------- #
    circles, img_canny = cch.detect__circleCannyHough( image=image_, **const )

    # ------------------------------------------------- #
    # --- [4] search nearest point                  --- #
    # ------------------------------------------------- #
    holes          = lpf.load__pointFile( inpFile=posFile, returnType="point" )
    designed_pos   = holes  [ :, x_:y_+1 ]
    detected_pos   = circles[ :, x_:y_+1 ]
    index,distance = snp.search__nearestPoint( vec1=designed_pos, vec2=detected_pos,  \
                                               returnType="index-distance", foreach=1 )

    # ------------------------------------------------- #
    # --- [5] replace by detected position          --- #
    # ------------------------------------------------- #
    nearby                 = np.where( distance <= maxDist, True, False )
    designed_pos[ nearby ] = detected_pos[ index[ nearby ] ]

    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    holepos = np.concatenate( [ designed_pos, nearby[:,None], index[:,None] ], axis=1 )
    return( holepos, image )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    maxDist = 20
    const   = { "iGauss"     : (5,5),        \
                "threshold"  : [0.3,0.7],    \
                "param2"     : 0.2,          \
                "dp"         : 1.2,          \
                "minDist"    : 0.04,         \
                "radiusRange": [0.02,0.07],  \
                "normalized_parameter": True }
    imgFile = "jpg/trapezoidal01.jpg"
    ARmFile = "dat/ARmarker_pos.dat"
    posFile = "dat/hole.dat"
    figSize        = (1200,900)
    image          = cv2.imread( imgFile )
    holepos,image  = detect__holePosition( image  =image  , ARmFile=ARmFile, \
                                           figSize=figSize, posFile=posFile, \
                                           const=const, maxDist=maxDist )
    
    # ------------------------------------------------- #
    # --- [2] display image                         --- #
    # ------------------------------------------------- #
    x_,y_,n_,i_ = 0, 1, 2, 3
    Leng_Sq     = 50
    colorTypes  = np.array( [ [255,0,0], [0,255,0] ], dtype=np.uint8 )
    lineColor   = colorTypes[ np.array( holepos[:,n_], dtype=np.int32 ) ]
    for ik,sq in enumerate( holepos ):
        pt1     = ( int(sq[x_]-0.5*Leng_Sq), int(sq[y_]-0.5*Leng_Sq) )
        pt2     = ( int(sq[x_]+0.5*Leng_Sq), int(sq[y_]+0.5*Leng_Sq) )
        color   = tuple( [ int(val) for val in lineColor[ik] ] )
        image   = cv2.rectangle( image, pt1, pt2, color=color, thickness=2 )
    cv2.imwrite( "jpg/out.jpg", image )
