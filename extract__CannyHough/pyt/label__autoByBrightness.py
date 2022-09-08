import numpy as np
import cv2
import os, sys

# ========================================================= #
# ===  label__autoByBrightness.py                       === #
# ========================================================= #

def label__autoByBrightness():

    x_, y_, z_ = 0, 1, 2
    nImage     = 321
    nPiece     = 149
    
    # ------------------------------------------------- #
    # --- [1] labelling                             --- #
    # ------------------------------------------------- #
    totals = []
    fnames = []
    ikips  = []
    for ik in range( nImage ):
        for ip in range( nPiece ):
            imgFile = "jpg/image{0:04}/extract{1:04}.jpg".format( ik+1, ip+1 )
            if ( os.path.exists( imgFile ) is False ):
                sys.exit( "cannot find file :: {}".format( imgFile ) )
            image   = cv2.cvtColor( cv2.imread( imgFile ), cv2.COLOR_BGR2GRAY )
            total   = np.sum( image )
            ikips .append( [ ik+1, ip+1 ] )
            totals.append( total )
            fnames.append( imgFile )
    ikips  = np.array( ikips  )
    totals = np.array( totals )
    fnames = np.array( fnames )
    
    totals = totals / np.max( totals )
    tindex = np.arange( totals.shape[0] ) + 1

    # ------------------------------------------------- #
    # --- [2] labeling of the Data                  --- #
    # ------------------------------------------------- #

    threshold = 0.75
    labels    = np.where( totals <= threshold, 1, 0 )     # large value == white == 0,   small value == black == 1
    trues     = np.where( totals <= threshold, True, False )
    falses    = np.logical_not( trues )

    Data      = np.concatenate( [tindex[:,None],ikips,totals[:,None],labels[:,None]], axis=1 )
    Data      = np.reshape( Data, (nImage,nPiece,5) )
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/labels.dat"
    names     = [ "index", "image_num", "piece_num", "totals", "labels" ]
    spf.save__pointFile( outFile=outFile, Data=Data, names=names )

    
    # ------------------------------------------------- #
    # --- [3] plot values                           --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    pngFile                  = "png/toDetermin__threshold.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=tindex[trues] , yAxis=totals[trues] , linestyle="none", marker=".", color="red"  )
    fig.add__plot( xAxis=tindex[falses], yAxis=totals[falses], linestyle="none", marker=".", color="blue" )
    fig.set__axis()
    fig.save__figure()

    
    
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    label__autoByBrightness()
    
