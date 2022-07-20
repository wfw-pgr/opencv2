import os, sys
import numpy   as np


# ========================================================= #
# ===  transcribe__holePosition.py                      === #
# ========================================================= #

def transcribe__holePosition( markers_ideal=None, markers_actual=None, detected_ids=None, \
                              xypos=None ):
    
    x_, y_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( markers_ideal  is None ): sys.exit("[transcribe__holePosition.py] markers_ideal  == ?")
    if ( markers_actual is None ): sys.exit("[transcribe__holePosition.py] markers_actual == ?")
    if ( detected_ids   is None ): sys.exit("[transcribe__holePosition.py] detected_ids   == ?")
    
    # ------------------------------------------------- #
    # --- [2] obtain c.o.g. of ids                  --- #
    # ------------------------------------------------- #
    nMarkers       = detected_ids.shape[0]
    markers_ideal_ = np.array( [ markers_ideal[ik][0,:] for ik in detected_ids ] )
    cog_ideal      = np.average( markers_ideal_, axis=0 )
    cog_actual     = np.average( markers_actual, axis=0 )

    # ------------------------------------------------- #
    # --- [3] each vector from c.o.g.               --- #
    # ------------------------------------------------- #
    vec_ideal  = markers_ideal_ - np.repeat( cog_ideal [None,:], nMarkers, axis=0 )
    vec_actual = markers_actual - np.repeat( cog_actual[None,:], nMarkers, axis=0 )
    
    # ------------------------------------------------- #
    # --- [4] find enclosing triangle               --- #
    # ------------------------------------------------- #
    #  -- need to add !!! boundary exception ( theta < -pi , theta > +pi )
    xypos_g = xypos[:,:] - np.repeat( cog_ideal[None,:], xypos.shape[0], axis=0 )
    theta_i = np.arctan2( vec_ideal[:,y_], vec_ideal[:,x_] )
    theta_p = np.arctan2( xypos_g[:,y_], xypos_g[:,x_] )
    thp,thi = np.meshgrid( theta_p, theta_i, indexing="ij" )
    index   = np.argmin( np.abs( thp-thi ), axis=1 )
    other   = np.where( theta_p - theta_i[index], +1, -1 )
    other   = index + other
    other[ np.where( other > nMarkers-1 ) ] = 0
    other[ np.where( other <          0 ) ] = nMarkers-1
    
    # ------------------------------------------------- #
    # --- [5] find (s,t) value for interpolation    --- #
    # ------------------------------------------------- #
    vec1_i  = vec_ideal[ index, : ]
    vec2_i  = vec_ideal[ other, : ]
    AreaInv = 1.0 / ( vec1_i[:,x_]*vec2_i[:,y_] - vec1_i[:,y_]*vec2_i[:,x_] )
    sval    = AreaInv * ( + vec2_i[:,y_]*xypos_g[:,x_] - vec2_i[:,x_]*xypos_g[:,y_] )
    tval    = AreaInv * ( - vec1_i[:,y_]*xypos_g[:,x_] + vec1_i[:,x_]*xypos_g[:,y_] )
    
    # ------------------------------------------------- #
    # --- [6] use (s,t)_ideal to interpolate        --- #
    # ------------------------------------------------- #
    vec1_a  = vec_actual[ index, : ]
    vec2_a  = vec_actual[ other, : ]
    sval_a  = np.repeat( sval[:,None], 2, axis=1 )
    tval_a  = np.repeat( tval[:,None], 2, axis=1 )
    diff_a  = sval_a*vec1_a + tval_a*vec2_a
    cog_a   = np.repeat( cog_actual[None,:], diff_a.shape[0], axis=0 )
    ret     = diff_a + cog_a
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    markers_ideal  = np.array( [ [0,0], \
                                 [1.2,0],
                                 [1.2,0.8],
                                 [0.0,0.8] ] )
    markers_actual = np.array( [ [0,0], \
                                 [1200,0],
                                 [1200,800],
                                 [0,800] ] )
    detected_ids   = np.array( [ [0],
                                 [1],
                                 [2],
                                 [3] ] )

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.2, 1.0, 11 ]
    x2MinMaxNum = [ 0.2, 0.6, 11 ]
    x3MinMaxNum = [ 0.0, 0.0,  1 ]
    xypos       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    xypos       = xypos[:,0:2]
    
    ret = transcribe__holePosition( markers_ideal=markers_ideal, markers_actual=markers_actual, \
                                    detected_ids =detected_ids , xypos=xypos )
    import nkUtilities.save__pointFile as spf
    outFile   = "out.dat"
    spf.save__pointFile( outFile=outFile, Data=ret )

    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "out.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ 0.0, 1200 ]
    config["plt_yRange"]     = [ 0.0,  800 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=ret[:,x_], yAxis=ret[:,y_], marker="o", linestyle="none" )
    fig.set__axis()
    fig.save__figure()



    
