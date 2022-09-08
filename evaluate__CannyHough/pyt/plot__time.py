import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs

# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():

    x_,y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    inpFile = "dat/time_for_calc.dat"
    pngFile = "png/time_for_calc.png"
    
    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data  = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    Data  = Data * 1000.0
    # Data  = Data
    Data1 = Data[:,1]
    Data2 = Data[:,2]
    Data3 = Data[:,3]
    bot1  = np.zeros_like( Data1 )
    bot2  = bot1 + Data1
    bot3  = bot2 + Data2
    print( Data1.shape, Data2.shape, Data3.shape )
    print(  bot1.shape,  bot2.shape,  bot3.shape )

    h_index = np.arange( 2 ) + 0.5
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = ""
    config["yTitle"]         = "Time (ms)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ 0.0,+2.0]
    config["plt_yRange"]     = [ 0.0,+300.0]
    config["plt_linewidth"]  = 1.0
    config["xMajor_Nticks"]  = 5
    config["yMajor_Nticks"]  = 4

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__bar( xAxis=h_index, yAxis=Data1, bottom=bot1 )
    fig.add__bar( xAxis=h_index, yAxis=Data2, bottom=bot2 )
    fig.add__bar( xAxis=h_index, yAxis=Data3, bottom=bot3 )
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

