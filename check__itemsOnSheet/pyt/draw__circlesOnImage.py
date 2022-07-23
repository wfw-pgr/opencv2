import os, sys
import cv2
import numpy as np

# ========================================================= #
# ===  draw__circlesOnImage.py                          === #
# ========================================================= #

def draw__circlesOnImage( image=None, circles=None, colors=None, \
                          posit=None, radii  =None, linewidth=4 ):

    x0_,y0_,rc_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] check argument                        --- #
    # ------------------------------------------------- #
    if ( image   is None ): sys.exit( "[draw__circlesOnImage.py] image   == ???" )
    if ( circles is None ):
        if ( ( posit is not None ) and ( radii is not None ) ):
            circles = np.concatenate( [posit,radii[:,None]], axis=1 )
        else:
            sys.exit( "[draw__circlesOnImage.py] circles == ???" )
    if ( colors  is None ):
        if   ( image.ndim == 3 ):
            colors = np.repeat( np.array( [0,0,255], dtype=np.uint8 )[None,:], \
                                circles.shape[0], axis=0 )
        elif ( image.ndim == 2 ):
            colors = np.repeat( np.array( [255], dtype=np.uint8 )[None,:], \
                                circles.shape[0], axis=0 )
        

    # ------------------------------------------------- #
    # --- [2] draw circles                          --- #
    # ------------------------------------------------- #
    img_show = np.copy( image )
    circles_ = np.array( circles, dtype=np.int32 )
    
    for ik,circ in enumerate(circles_):
        hcolor   = [ int(val) for val in colors[ik] ]
        img_show = cv2.circle( img_show, ( circ[x0_],circ[y0_]), circ[rc_], \
                               color=hcolor, thickness=linewidth )
    return( img_show )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile = "jpg/coin__onSheet.jpg"
    image   = cv2.imread( inpFile )
    circles = np.array( [ [ 726.6, 1314.6, 227.5 ] ], dtype=np.int32 )
    colors  = [ [255,0,0] ]
    colors  = None
    
    img_reg = draw__circlesOnImage( image=image, circles=circles, colors=colors )
    print( img_reg.shape )

    cv2.imshow( "figure", img_reg )
    cv2.waitKey( 1000000 )
