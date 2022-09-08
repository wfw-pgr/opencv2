import os, sys
import cv2
import numpy   as np
import skimage
import skimage.util, skimage.color, skimage.io
import skimage.feature, skimage.transform
import matplotlib.pyplot as plt

# ========================================================= #
# ===  detect__CannyHoughEllipses.py                    === #
# ========================================================= #

def detect__CannyHoughEllipses( image=None, sigma=1.0, \
                                low_threshold=0.55, high_threshold=0.80, accuracy=3, \
                                threshold=5, min_size=10, max_size=50 ):
    
    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    #  -- [1-1] missing argument check              --  #
    if ( image  is     None ): sys.exit( "[detect__circleCannyHough.py] image == ???" )
    image_   = np.copy( image )
    
    # ------------------------------------------------- #
    # --- [2] openCV image -> skimage               --- #
    # ------------------------------------------------- #
    image_sk = ( skimage.util.img_as_float( image_ ) )[:,:,::-1] # -- BGR 2 RGB -- #

    # ------------------------------------------------- #
    # --- [3] Canny-Method & Hough conversion       --- #
    # ------------------------------------------------- #
    image_gray = skimage.color.rgb2gray( image_sk )
    image_edge = skimage.feature.canny ( image_gray, sigma=sigma, \
                                         low_threshold =low_threshold, \
                                         high_threshold=high_threshold )
    result     = None
    result     = skimage.transform.hough_ellipse( np.copy(image_edge), accuracy=accuracy, \
                                                  threshold=threshold,
                                                  min_size=min_size, max_size=max_size )
    print( result )
    # ------------------------------------------------- #
    # --- [4] return value                          --- #
    # ------------------------------------------------- #
    return( result, image_edge )
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    
    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] preparation                           --- #
    # ------------------------------------------------- #
    figSize     = (1000,1000)
    image       = np.ones( (figSize[y_],figSize[x_],3), dtype=np.uint8 ) * 255

    # ------------------------------------------------- #
    # --- [2] grid-like point to put rectangle      --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 200.0, 800.0, 2 ]
    x2MinMaxNum = [ 200.0, 800.0, 2 ]
    x3MinMaxNum = [   0.0,   0.0, 1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    centers     = coord[:,0:2]

    # ------------------------------------------------- #
    # --- [3] edge-length & colors                  --- #
    # ------------------------------------------------- #
    xc          = np.copy( centers[:,x_] )
    yc          = np.copy( centers[:,y_] )
    rc          = np.random.randint( 100,200, (xc.shape[0],) )
    a1          = np.random.randint( 100,200, (xc.shape[0],) )
    a2          = np.random.randint( 100,200, (xc.shape[0],) )
    angle       = np.random.randint( 0,360, (xc.shape[0],) )
    colors      = np.repeat( np.array( [255,0,0] )[None,:], xc.shape[0], axis=0 )

    # ------------------------------------------------- #
    # --- [4] put rectangululars                    --- #
    # ------------------------------------------------- #
    import nkOpenCV.put__ellipses as ell
    image_      = ell.put__ellipses( image=image, xc=xc, yc=yc, a1=a1, a2=a2, angle=angle, \
                                     colors=colors )

    # ------------------------------------------------- #
    # --- [5] output                                --- #
    # ------------------------------------------------- #
    outFile     = "jpg/ellipses.jpg"
    cv2.imwrite( outFile, image_ )
    print( " outFile :: {}".format( outFile ) )
    print()

    image   = cv2.imread( outFile )
    image   = cv2.resize( image, dsize=(300,300) )
    const   = { "sigma"    :1.0, "low_threshold":0.20, "high_threshold":0.60, "accuracy":1, \
                "threshold": 20, "min_size"     :20  , "max_size"      :30 }
    res,img = detect__CannyHoughEllipses( image=image, **const )
    res     = np.array( res )
    print( res.shape )
    import nkOpenCV.put__ellipses as ell
    img     = ell.put__ellipses( img, xc=res[:,1], yc=res[:,2], \
                                 a1=res[:,3], a2=res[:,4], angle=res[:,5] )
    cv2.imwrite( "output.jpg", image )
