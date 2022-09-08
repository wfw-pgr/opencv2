import sys
import cv2
import numpy as np

#  --  center_pos = [ [ x0, y0], [ x1, y1], ..... ]
#  --  length     = [ [lx0,lyl], [lxl,ly1], ..... ]
#  --  bb         = [ [x11,y11,x22,y22]_0, [x11,y11,x22,y22]_1, ..... ] # default

# ========================================================= #
# ===  extract__rectangularRegion.py                    === #
# ========================================================= #

def extract__rectangularRegion( image =None, bb=None   , center_pos=None, \
                                length=None, margin=0.1, rescale   =None, returnType="" ):

    xfrom_, yfrom_, xtill_, ytill_ = 0, 1, 2, 3
    
    # ------------------------------------------------- #
    # --- [1] argument  check                       --- #
    # ------------------------------------------------- #
    if ( image   is None ): sys.exit( "[extract__rectangularyRegion.py] image   == ???" )
    if ( bb      is None ):
        if ( ( center_pos is not None ) and ( length is not None ) ):
            if ( type(length) in [ int, float]  ):
                leng = np.repeat( np.array( [length,length] )[None,:], \
                                  center_pos.shape[0],axis=0 )
            elif ( type(length) in [np.ndarray] ):
                if ( length.ndim == 1 ):
                    if   ( length.shape[0] == 2 ):
                        leng = np.repeat( length[None,:], center_pos.shape[0], axis=0 )
                    elif ( length.shape[0] == center_pos.shape[0] ):
                        leng = np.repeat( length[:,None], 2, axis=1 )
            bb_11 = center_pos - ( 1.0 + margin ) * ( leng * 0.5 )
            bb_22 = center_pos + ( 1.0 + margin ) * ( leng * 0.5 )
            bb    = np.array ( np.concatenate( [bb_11,bb_22], axis=1 ), dtype=np.int32 )
        else:
            sys.exit( "[extract__rectangularyRegion.py] bb , or center_pos and length ???" )
    if ( rescale is not None ):
        if ( type( rescale ) == [ tuple, list, np.ndarray ] ):
            print( "[extract__rectangularRegion.py] rescale should be tuple, list or numpy array")
            sys.exit()
    Lx, Ly = image.shape[1], image.shape[0]
    dim    = image.ndim
    
    # ------------------------------------------------- #
    # --- [2] extract images                        --- #
    # ------------------------------------------------- #
    extractedImages = []
    for ik,hbb in enumerate( bb ):
        xfrom, xtill = int( hbb[xfrom_] ), int( hbb[xtill_] )
        yfrom, ytill = int( hbb[yfrom_] ), int( hbb[ytill_] )
        img          = image[ yfrom:ytill, xfrom:xtill, ... ]
        extractedImages.append( img )
        
    if ( rescale is None ):
        return( extractedImages )

    # ------------------------------------------------- #
    # --- [3] rescale image                         --- #
    # ------------------------------------------------- #
    rescaledImages = []
    for ik, img in enumerate( extractedImages ):
        rimg = cv2.resize( img, dsize=rescale )
        rescaledImages.append( rimg )
        
    return( np.array( rescaledImages ) )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile    = "jpg/coin__onSheet.jpg"
    circles    = np.array( [ [ 1229.4, 1842.6, 211.1 ] ] )
    center_pos = circles[:,0:2]
    length     = np.copy( circles[:,2] * 2.0 )
    margin     = 0.1
    rescale    = (64,64)

    image      = cv2.imread( inpFile )
    ret        = extract__rectangularRegion( image=image, center_pos=center_pos, \
                                             length=length, margin=margin, rescale=rescale )

    outFile    = "jpg/ext_test_{0:04}.jpg"
    for ik,img in enumerate( ret ):
        cv2.imwrite( outFile.format( ik+1 ), img )
