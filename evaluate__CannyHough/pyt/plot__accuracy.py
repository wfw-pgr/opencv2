import sys
import numpy                       as np
import nkUtilities.load__pointFile as lpf
import nkUtilities.load__config    as lcf
import nkUtilities.plot1D          as pl1
import nkUtilities.configSettings  as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():

    angle_, accu_, intr_ = 0, 3, 4
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/accuracy.dat"
    pngFile = "png/accuracy.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    Data    = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    Data[:,accu_] = Data[:,accu_]
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Angle (deg.)"
    config["yTitle"]         = "Accuracy of Detection (%)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ +0.0,+100]
    config["plt_yRange"]     = [+90.0,+110]
    config["plt_linestyle"]  = "-"
    config["plt_linewidth"]  = 2.0
    config["plt_marker"]     = "o"
    config["plt_markerSize"] = 2.0
    config["xMajor_Nticks"]  = 11
    config["yMajor_Nticks"]  = 11

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data[:,angle_], yAxis=Data[:,accu_], label="w/o" )
    fig.add__plot( xAxis=Data[:,angle_], yAxis=Data[:,intr_], label="w/"  )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

