import os, sys
import numpy   as np


# ========================================================= #
# ===  transcribe__holePosition.py                      === #
# ========================================================= #

def transcribe__holePosition( markers_id    =None, markers_ph=None, \
                              detected_ARids=None, cpos_id   =None ):
    
    x_, y_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( markers_id     is None ): sys.exit("[transcribe__holePosition.py] markers_id     == ??")
    if ( markers_ph     is None ): sys.exit("[transcribe__holePosition.py] markers_ph     == ??")
    if ( detected_ARids is None ): sys.exit("[transcribe__holePosition.py] detected_ARids == ??")
    
    # ------------------------------------------------- #
    # --- [2] obtain c.o.g. of ids                  --- #
    # ------------------------------------------------- #
    nMarkers    = detected_ARids.shape[0]
    markers_id_ = markers_id[ detected_ARids ]
    cog_iAR     = np.average( markers_id_, axis=0 )
    cog_pAR     = np.average( markers_ph , axis=0 )
    
    # ------------------------------------------------- #
    # --- [3] each vector from c.o.g.               --- #
    # ------------------------------------------------- #
    markers_id_ = markers_id_ - np.repeat( cog_iAR[None,:], nMarkers, axis=0 )
    markers_ph_ = markers_ph  - np.repeat( cog_pAR[None,:], nMarkers, axis=0 )
    
    # ------------------------------------------------- #
    # --- [4] find enclosing triangle               --- #
    # ------------------------------------------------- #
    #  -- need to add !!! boundary exception ( theta < -pi , theta > +pi )
    cpos_cg     = cpos_id[:,:] - np.repeat( cog_iAR[None,:], cpos_id.shape[0], axis=0 )
    theta_iAR   = np.arctan2( markers_id_[:,y_], markers_id_[:,x_] )
    theta_iCP   = np.arctan2( cpos_cg    [:,y_], cpos_cg    [:,x_] )
    thAR,thCP   = np.meshgrid( theta_iAR, theta_iCP, indexing="ij" )
    index       = np.argmin( np.abs( thAR-thCP ), axis=0 )
    other       = np.where( ( ( theta_iCP-theta_iAR[index] ) > 0 ), +1, -1 )
    other       = index + other
    other[ np.where( other > nMarkers-1 ) ] = 0
    other[ np.where( other <          0 ) ] = nMarkers-1
    
    # ------------------------------------------------- #
    # --- [5] find (s,t) value for interpolation    --- #
    # ------------------------------------------------- #
    vec1_id     = markers_id_[ index, : ]
    vec2_id     = markers_id_[ other, : ]
    AreaInv     = 1.0 / ( vec1_id[:,x_]*vec2_id[:,y_] - vec1_id[:,y_]*vec2_id[:,x_] )
    sval        = AreaInv * ( + vec2_id[:,y_]*cpos_cg[:,x_] - vec2_id[:,x_]*cpos_cg[:,y_] )
    tval        = AreaInv * ( - vec1_id[:,y_]*cpos_cg[:,x_] + vec1_id[:,x_]*cpos_cg[:,y_] )
    
    # ------------------------------------------------- #
    # --- [6] use (s,t)_ideal to interpolate        --- #
    # ------------------------------------------------- #
    vec1_ph  = markers_ph_[ index, : ]
    vec2_ph  = markers_ph_[ other, : ]
    sval_ph  = np.repeat( sval[:,None], 2, axis=1 )
    tval_ph  = np.repeat( tval[:,None], 2, axis=1 )
    diff_ph  = sval_ph*vec1_ph + tval_ph*vec2_ph
    cog_ph   = np.repeat( cog_pAR[None,:], diff_ph.shape[0], axis=0 )
    ret      = diff_ph + cog_ph
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    markers_id  = np.array( [ [0,0], \
                                 [1.2,0],
                                 [1.2,0.8],
                                 [0.0,0.8] ] )
    markers_ph = np.array( [ [0,0], \
                                 [1200,0],
                                 [1200,800],
                                 [0,800] ] )
    detected_ARids   = np.array( [ [0],
                                 [1],
                                 [2],
                                 [3] ] )

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.2, 1.0, 11 ]
    x2MinMaxNum = [ 0.2, 0.6, 11 ]
    x3MinMaxNum = [ 0.0, 0.0,  1 ]
    cpos_id       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    cpos_id       = cpos_id[:,0:2]
    
    ret = transcribe__holePosition( markers_id=markers_id, markers_ph=markers_ph, \
                                    detected_ARids =detected_ARids , cpos_id=cpos_id )
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



    
