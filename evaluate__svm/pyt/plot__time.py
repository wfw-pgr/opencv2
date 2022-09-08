import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs
import nkInterpolator.interpolate__polynomial as pol

# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():

    x_,y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/compute_time_svm.dat"
    pngFile = "png/compute_time_svm.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data   = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    xAxis1 = Data[:,1]
    yAxis1 = Data[:,4] / Data[:,1] * 1000.0
    xAxis2 = Data[:,1] # training data number is related to the complexity of network.
    yAxis2 = Data[:,5] / Data[:,2] * 1000.0

    # ------------------------------------------------- #
    # --- [3] fitting                               --- #
    # ------------------------------------------------- #
    xFit1  = np.linspace( 0.0, 40000, 201 )
    xFit2  = np.linspace( 0.0, 40000, 201 )
    xd1    = np.insert( xAxis1, 0, 0.0 )
    xd2    = np.insert( xAxis2, 0, 0.0 )
    fx1    = np.insert( yAxis1, 0, 0.0 )
    fx2    = np.insert( yAxis2, 0, 0.0 )

    # -- x^n -- #
    def xn_func( x, c0, c1 ):
        return( c0*x**c1 )
    import scipy.optimize as opt
    coefs1, cov1 = opt.curve_fit( xn_func, xd1, fx1 )
    coefs2, cov2 = opt.curve_fit( xn_func, xd2, fx2 )
    yFit1  = xn_func( xFit1, coefs1[0], coefs1[1] )
    yFit2  = xn_func( xFit2, coefs2[0], coefs2[1] )
    eq1    = "y={:.4f}x^{:.4f}".format( coefs1[0], coefs1[1] )
    eq2    = "y={:.4f}x^{:.4f}".format( coefs2[0], coefs2[1] )
    print( "[plot__time.py] (train) :: {}".format( eq1 ) )
    print( "[plot__time.py] (test)  :: {}".format( eq2 ) )
    
    # -- polynomial -- #
    # deg    = 2
    # func1  = np.poly1d( np.polyfit( xd1, fx1, deg ) )
    # func2  = np.poly1d( np.polyfit( xd2, fx2, deg ) )
    # yFit1  = func1( xFit1 )
    # yFit2  = func2( xFit2 )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Number of Training Data"
    config["yTitle"]         = "Computational Time / Number of Data (ms)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [0,+40000]
    config["plt_yRange"]     = [0,6.0]
    config["plt_linewidth"]  = 1.0
    config["xMajor_Nticks"]  = 5
    config["yMajor_Nticks"]  = 7
    config["plt_linestyle"]  = "none"
    config["leg_nColumn"]    = 2

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    
    label = { "train":"Training", "pred":"prediction", "fit1":eq1, "fit2":eq2 }
    fig   = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis1, yAxis=yAxis1, linestyle="none", label=label["train"], \
                   marker="o", markersize=4.0, color="royalblue" )
    fig.add__plot( xAxis=xAxis2, yAxis=yAxis2, linestyle="none", label=label["pred"] , \
                   marker="o", markersize=4.0, color="orange"    )
    fig.add__plot( xAxis=xFit1, yAxis=yFit1, linestyle="--", \
                   color="royalblue", label=label["fit1"] )
    fig.add__plot( xAxis=xFit2, yAxis=yFit2, linestyle="--", \
                   color="orange"   , label=label["fit2"] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

