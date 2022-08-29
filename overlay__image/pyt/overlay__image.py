import os, cv2, sys
import numpy as np
import PIL.Image


# ========================================================= #
# ===  overlay__image.py                                === #
# ========================================================= #

def overlay__image( base=None, overlay=None, location=None, centering=True ):

    
    x_, y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( base     is None ): sys.exit( "[overlay__image.py] base     == ???" )
    if ( overlay  is None ): sys.exit( "[overlay__image.py] overlay  == ???" )
    if ( location is None ): sys.exit( "[overlay__image.py] location == ???" )

    overlay_h, overlay_w = overlay.shape[:2]
    if ( centering ):
        location[x_] = int( location[x_] - overlay_w * 0.5 )
        location[y_] = int( location[y_] - overlay_h * 0.5 )
    else:
        location[x_] = int( location[x_] )
        location[y_] = int( location[y_] )

    base         = cv2.cvtColor( base   , cv2.COLOR_BGR2RGB   )
    overlay      = cv2.cvtColor( overlay, cv2.COLOR_BGRA2RGBA )
    pil_base     = PIL.Image.fromarray( base    )
    pil_overlay  = PIL.Image.fromarray( overlay )
    pil_base     = pil_base   .convert( "RGBA" )
    pil_overlay  = pil_overlay.convert( "RGBA" )

    pil_tmp      = PIL.Image.new( "RGBA", pil_base.size, (255, 255, 255, 0) )
    pil_tmp.paste( pil_overlay, location, pil_overlay )
    result_image = PIL.Image.alpha_composite( pil_base, pil_tmp )

    ret          = cv2.cvtColor( np.asarray( result_image ), cv2.COLOR_RGBA2BGRA )
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_,y_,z_   = 0, 1, 2
    figsize1   = (640,320)
    figsize2   = (320,160)
    location   = [ 320,160 ]
    base = np.ones( ( figsize1[y_], figsize1[x_] ), dtype=np.uint8 ) * 255
    overlay  = cv2.imread( "jpg/todai.jpg" )

    overlayed  = overlay__image( base=base, overlay=overlay, location=location, \
                                 centering=True )

    outFile = "jpg/out.jpg"
    cv2.imwrite( outFile, overlayed )
    print( "[overlay__image.py] outFile :: {} ".format( outFile ) )
