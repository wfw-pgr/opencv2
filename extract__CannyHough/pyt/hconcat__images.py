import os, sys
import numpy as np
import cv2
import nkOpenCV.put__rectangular as rct
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  hconcat__images.py                               === #
# ========================================================= #

def hconcat__images():

    x_, y_, z_      = 0, 1, 2
    x1_,y1_,x2_,y2_ = 0, 1, 2, 3
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    nImage_max   = 300
    nPiece_max   = 120
    nImage_verti = 30
    nImage_horiz = 60
    image_size   = ( 2400, 1200 )
    frame_width  = 5
    lblFile      = "dat/labels.dat"
    outFile      = "jpg/stacked.jpg"
    
    # ------------------------------------------------- #
    # --- [2] random pick 2 integers                --- #
    # ------------------------------------------------- #
    iarr1 = np.random.randint( 1, nImage_max, ( nImage_verti, nImage_horiz ) )
    iarr2 = np.random.randint( 1, nPiece_max, ( nImage_verti, nImage_horiz ) )
    dsize = ( int( image_size[x_] / nImage_horiz ), int( image_size[y_] / nImage_verti ) )

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, image_size[0], nImage_horiz+1 ]
    x2MinMaxNum = [ 0.0, image_size[1], nImage_verti+1 ]
    x3MinMaxNum = [ 0.0,           0.0,              1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    bb1         = np.array( coord[ 0, :-1, :-1, 0:2 ], dtype=np.int64 )
    bb2         = np.array( coord[ 0, 1: , 1: , 0:2 ], dtype=np.int64 )
    bb          = np.concatenate( [bb1,bb2], axis=2 )

    labelData   = lpf.load__pointFile( inpFile=lblFile, returnType="structured" )
    labels      = np.reshape( labelData[ iarr1[:,:]-1, iarr2[:,:]-1, 4 ], (-1,) )
    
    # ------------------------------------------------- #
    # --- [3] pack images                           --- #
    # ------------------------------------------------- #
    image_stack = np.ones( (image_size[y_],image_size[x_],3), dtype=np.uint8 ) * 0
    for iv in range( nImage_verti ):
        for ih in range( nImage_horiz ):
            imgFile  = "jpg/image{0:04}/extract{1:04}.jpg".format( iarr1[iv,ih], iarr2[iv,ih] )
            img      = cv2.imread( imgFile )
            image_stack[ bb[iv,ih,y1_]:bb[iv,ih,y2_], \
                         bb[iv,ih,x1_]:bb[iv,ih,x2_], : ] = cv2.resize( img, dsize=dsize )

    wdt         = 1
    bb_         = np.reshape( bb, ( -1, 4 ) )
    dbb         = np.repeat( np.array( [+wdt,+wdt,-wdt,-wdt] )[None,:], bb_.shape[0], axis=0 )
    bb_         = bb_ + dbb
        
    colorList   = np.array( [ [255,0,0], [0,0,255] ] )
    image_stack = rct.put__rectangular( image=image_stack, bb=bb_, colorList=colorList, \
                                        colorValues=labels )
    cv2.imwrite( outFile, image_stack )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    hconcat__images()
    
