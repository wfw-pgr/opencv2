import numpy as np
import os, sys

# ========================================================= #
# ===  heatmap.py                                       === #
# ========================================================= #

def heatmap():

    p1_, p2_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1]  load data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile      = "dat/hyperParams.dat"
    pngFile      = "png/hyperParameter_search.png"
    scores       = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    params_name  = [ "C", r"$\gamma$" ]
    params1_list = [ 2.0**(i) for i in list( range( -1, 5, 1 ) ) ]
    params2_list = [ 5.e-9, 1.e-8, 5.e-8, 1.e-7, 5.e-7, 1.e-6 ]

    # ------------------------------------------------- #
    # --- [2] draw heat map                         --- #
    # ------------------------------------------------- #
    import nkUtilities.draw__heatmap    as dhm
    xlabels = [ "{:.2f}".format( val ) for val in params1_list ]
    ylabels = [ "{:.2e}".format( val ) for val in params2_list ]
    dhm.draw__heatmap( Data=scores, vmin=0.93, vmax=1.00, pngFile=pngFile, fontsize=10, \
                       xtitle=params_name[p1_], ytitle=params_name[p2_], \
                       xlabels=xlabels, ylabels=ylabels, position=[0.24,0.20,0.86,0.86]  )

    return()

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    heatmap()
