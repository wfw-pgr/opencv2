import numpy as np
import cv2
import os, sys


# ========================================================= #
# ===  put__rectangular.py                         === #
# ========================================================= #

def put__rectangular( image=None, bb=None, centers=None, edge_length =50, \
                           colors=None, colorList=[ [255,0,0], [0,255,0] ], colorValues=None, \
                           thickness=2 ):

    # ------------------------------------------------- #
    # --- [1]  arguments                            --- #
    # ------------------------------------------------- #
    if ( image   is None ): sys.exit( "[put__rectangular.py] image   == ???" )
    if ( bb      is None ):
        if ( centers is not None ):
            if ( type( edge_length ) in [ int, float ] ):
                edge_length = [ int( edge_length ) ] * 2
            if ( type( edge_length ) in [ list, tuple, np.array ] ):
                edge_length = np.array( edge_length )
            if ( edge_length.ndim == 1 ):
                edge_length = np.repeat( np.reshape( edge_length, (1,2) ), \
                                         centers.shape[0], axis=0 )
                bb1         = centers - edge_length * 0.5
                bb2         = centers + edge_length * 0.5
                bb          = np.concatenate( [bb1,bb2], axis=1 )
        else:
            sys.exit( "[put__rectangular.py] bb   == ???" )
    if ( colors is None ):
        if ( colorValues is not None ):
            colorList = np.array( colorList, dtype=np.uint8 )
            colors    = colorList[ np.array( colorValues, dtype=np.int64 ) ]
        else:
            colors  = np.repeat( np.array( [ [255,0,0] ], dtype=np.uint8 ), \
                                 bb.shape[0], axis=0 )
    # ------------------------------------------------- #
    # --- [2] put rectangle on image                --- #
    # ------------------------------------------------- #
    for ik,hbb in enumerate( bb ):
        pt1     = tuple( [ int(val) for val in hbb[0:2] ] )
        pt2     = tuple( [ int(val) for val in hbb[2:4] ] )
        hcolor  = tuple( [ int(val) for val in colors[ik] ] )
        image   = cv2.rectangle( image, pt1, pt2, color=hcolor, thickness=thickness )
    
    # ------------------------------------------------- #
    # --- [3] return                                --- #
    # ------------------------------------------------- #
    return( image )



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
    x1MinMaxNum = [ 200.0, 800.0, 7 ]
    x2MinMaxNum = [ 200.0, 800.0, 7 ]
    x3MinMaxNum = [   0.0,   0.0, 1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    centers     = coord[:,0:2]

    # ------------------------------------------------- #
    # --- [3] edge-length & colors                  --- #
    # ------------------------------------------------- #
    edge_length = 50
    colorList   = np.array( [ [255,0,0], [0,255,0] ] )
    colorValues = np.array( np.where( np.random.random( centers.shape[0] ) > 0.5, 1, 0 ), \
                            dtype=np.int64 )

    # ------------------------------------------------- #
    # --- [4] put rectangululars                    --- #
    # ------------------------------------------------- #
    ret         = put__rectangular( image=image, centers=centers, edge_length=edge_length,\
                                    colorList=colorList, colorValues=colorValues )

    # ------------------------------------------------- #
    # --- [5] output                                --- #
    # ------------------------------------------------- #
    outFile     = "jpg/out.jpg"
    cv2.imwrite( outFile, image )
    print( " outFile :: {}".format( outFile ) )
    print()
