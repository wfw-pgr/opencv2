import numpy as np

# ========================================================= #
# ===  match__holePosition.py                           === #
# ========================================================= #

def match__holePosition( xypos_t=None, xypos_a=None, values=None ):

    x_, y_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    if ( xypos_t is None ): sys.exit( "[match__holePosition.py] xypos_t == ???" )
    if ( xypos_a is None ): sys.exit( "[match__holePosition.py] xypos_a == ???" )
    if ( values  is None ): sys.exit( "[match__holePosition.py] values  == ???" )

    # ------------------------------------------------- #
    # --- [2]  calculate distance                   --- #
    # ------------------------------------------------- #
    xt, xa = np.meshgrid( xypos_t[:,x_], xypos_a[:,x_], indexing="ij" )
    yt, ya = np.meshgrid( xypos_t[:,y_], xypos_a[:,y_], indexing="ij" )
    index  = np.argmin( ( xt-xa )**2 + ( yt-ya )**2, axis=0 )
    print( index.shape )

    # ------------------------------------------------- #
    # --- [3] return values                         --- #
    # ------------------------------------------------- #
    ret    = values[index]
    return( ret )


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
    ret         = match__holePosition( xypos_t=coord_t, xypos_a=coord_a, values=values )
    print( ret.shape )
    print( ret )
