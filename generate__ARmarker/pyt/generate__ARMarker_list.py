import numpy as np
import os, sys, cv2

# ========================================================= #
# ===  generate__ARMarker.py                            === #
# ========================================================= #

def generate__ARMarker():

    x_, y_, z_    = 0, 1, 2
    aruco         = cv2.aruco
    markerType    = cv2.aruco.DICT_4X4_50
    markerSize    = 100
    figSize       = (  400, 400 )
    paperSize     = ( 1600,1600 )
    ARids         = [ 0, 1, 3, 4 ]
    
    markers_dict  = aruco.getPredefinedDictionary( markerType )
    markers_imgs  = [ aruco.drawMarker( markers_dict, ARid, markerSize ) for ARid in ARids ]
    markers_imgs  = np.array( markers_imgs )

    print( markers_imgs.shape )

    figure        = np.ones( (figSize[y_],figSize[x_]) ) * 255.0
    bb            = np.array( [ [80,80,180,180],  [220,220,320,320],
                                [80,220,180,320], [220,80 ,320,180] ], dtype=np.int64 )
    for ik, marker in enumerate( markers_imgs ):
        figure[ bb[ik,0]:bb[ik,2], bb[ik,1]:bb[ik,3] ] = np.copy( marker )
    base_unit = np.copy( figure )

    paper         = np.ones( (paperSize[y_],paperSize[x_]) ) * 255.0
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, paperSize[0], 5 ]
    x2MinMaxNum = [ 0.0, paperSize[1], 5 ]
    x3MinMaxNum = [ 0.0,          0.0, 1 ]
    bb          = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    bb          = bb[ 0, :,:, 0:2 ]
    bb_top      = np.array( np.copy( bb ), dtype=np.int64 )
    bb_         = np.roll( bb, (-1,-1), axis=(0,1) )
    paper_bb    = np.concatenate( [ bb, bb_ ], axis=2 )
    paper_bb    = np.array( paper_bb[ 0:4, 0:4, : ], dtype=np.int64 )

    ic     = 0
    ratio  = np.linspace( 0.2, 1.0, 16 )
    images = []
    for i1 in range( 4 ):
        for i2 in range( 4 ):
            img     = np.copy( base_unit )
            dsize   = ( int( ratio[ic]*figSize[0] ), int( ratio[ic]*figSize[1] ) )
            print( dsize )
            bb_     = np.array( bb_top[i1,i2,0:2] + np.array( dsize ), dtype=np.int64 )
            
            print( bb_, bb_.shape )
            img     = cv2.resize( img, dsize=dsize )
            print( img.shape )
            ic     += 1
            images.append( img )
            paper[ bb_top[i1,i2,0]:bb_[0], bb_top[i1,i2,1]:bb_[1] ] = np.copy( img )
            # paper[ paper_bb[i1,i2,0]:paper_bb[i1,i2,2], paper_bb[i1,i2,1]:paper_bb[i1,i2,3] ] =\
            #     np.copy( img )
    # print( len( images ), type( images ) )
    # images = np.array( images )
    # print( images.shape )
    # cv2.imwrite( "out.jpg", figures )
    cv2.imwrite( "jpg/out.jpg", paper )
    print( paper )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__ARMarker()
    
