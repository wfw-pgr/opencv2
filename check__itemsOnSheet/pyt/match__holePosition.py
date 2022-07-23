import os, sys
import numpy as np


# ========================================================= #
# ===  match__holePosition.py                           === #
# ========================================================= #

def match__holePosition( pos1=None, pos2=None, max_distance=None, indexType="1->2" ):

    x_, y_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    if ( pos1      is None ): sys.exit( "[match__holePosition.py] pos1 == ???" )
    if ( pos2      is None ): sys.exit( "[match__holePosition.py] pos2 == ???" )
    if   ( indexType.lower() == "2->1" ):
        axis = 0   # compress Row ( = pos1 ) :: closest pos1 for each pos2  ( ret. len(pos2) )
    elif ( indexType.lower() == "1->2" ):
        axis = 1   # compress Col ( = pos2 ) :: closest pos2 for each pos1  ( ret. len(pos1) )

    # ------------------------------------------------- #
    # --- [2]  calculate distance                   --- #
    # ------------------------------------------------- #
    xRow, xCol = np.meshgrid( pos1[:,x_], pos2[:,x_], indexing="ij" )
    yRow, yCol = np.meshgrid( pos1[:,y_], pos2[:,y_], indexing="ij" )
    radiiMat   = np.sqrt  ( ( xRow-xCol )**2 + ( yRow-yCol )**2 )
    index      = np.argmin( radiiMat, axis=axis )

    # ------------------------------------------------- #
    # --- [3] return values                         --- #
    # ------------------------------------------------- #
    return( index )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 0.0,  1 ]
    coord_t     = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    coord_a     = coord_t + np.random.normal( coord_t.shape[0], 2 ) * 0.05
    values      = np.where( np.random.rand( coord_t.shape[0] ) > 0.7, 1, 0 )
    ret         = match__holePosition( pos1=coord_t, pos2=coord_a )
    print( ret.shape )
    print( ret )
