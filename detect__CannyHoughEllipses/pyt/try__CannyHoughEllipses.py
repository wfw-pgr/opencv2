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

def detect__CannyHoughEllipses( image=None, sigma=1.0, exe=False, \
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
    if ( exe is True ):
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
    exe = False

    inpFile    = "jpg/match_45deg.jpg"
    image      = cv2.imread( inpFile )
    image_sk   = ( skimage.util.img_as_float( image ) )[:,:,::-1]  # -- BGR 2 RGB -- #
    image_sk   = image_sk[ 210:285, 360:520,:]
    # image_sk = cv2.resize( image_sk, dsize=(300,300) )
    const   = { "sigma"    :2.0, "low_threshold":0.20, "high_threshold":0.60, "accuracy":2, \
                "threshold": 50, "min_size"     :10  , "max_size"      :70 }
    print( "[begin detection]" )
    res,img = detect__CannyHoughEllipses( image=image_sk, **const, exe=exe )
    print( "[end detection]" )
    skimage.io.imshow( img )
    plt.show()
    image_cv = ( skimage.img_as_ubyte( img ) )[:,:]
    cv2.imwrite( "jpg/canny.jpg", image_cv )
    sys.exit()
    print( res )
    print( res.shape )
    pileup = []
    for tp in res:
        pileup.append( np.array( [ int(round(val)) for val in list(tp) ] ) )
    res = np.array( pileup )
    print( res.shape )
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/res.dat"
    spf.save__pointFile( outFile=outFile, Data=res )

    
    import nkOpenCV.put__ellipses as ell
    img     = ell.put__ellipses( img, xc=res[:,1], yc=res[:,2], \
                                 a1=res[:,3], a2=res[:,4], angle=res[:,5] )
    cv2.imwrite( "jpg/output.jpg", image )
