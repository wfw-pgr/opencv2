import os, sys
import numpy as np


# ========================================================= #
# ===  remove__points.py                                === #
# ========================================================= #

def remove__points():

    x_, y_ = 0, 1
    
    import nkUtilities.load__pointFile as lpf
    inpFile   = "dat/hole_original.dat"
    Data      = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )
    
    pt1, pt2  = const["outline.01"], const["outline.02"]
    pt3, pt4  = const["outline.03"], const["outline.04"]

    def straightLine( x, p1, p2 ):
        a = ( p2[y_] - p1[y_] ) / ( p2[x_] - p1[x_] )
        y = a * ( x - p1[x_] ) + p1[y_]
        return( y )

    y_line1 = straightLine( Data[:,x_], pt1, pt2 )
    y_line2 = straightLine( Data[:,x_], pt3, pt4 )
    judge   = np.where( ( Data[:,y_] < y_line1 ) & ( Data[:,y_] < y_line2 ) )
    Data_   = Data[judge]
    print( Data.shape, Data_.shape )

    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "png/out.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data_[:,x_], yAxis=Data_[:,y_], marker="o", linestyle="none" )
    fig.add__plot( xAxis=Data [:,x_], yAxis=y_line1, label="line1"  )
    fig.add__plot( xAxis=Data [:,x_], yAxis=y_line2, label="line2"  )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()
    
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/hole.dat"
    names     = [ "xp", "yp", "rc", "flag" ]
    spf.save__pointFile( outFile=outFile, Data=Data_, names=names )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    remove__points()

    
