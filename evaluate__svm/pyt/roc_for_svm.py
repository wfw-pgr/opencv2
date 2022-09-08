import os, sys, cv2
import sklearn, sklearn.svm
import numpy as np
import nkML.evaluate__ROC          as roc
import nkUtilities.load__pointFile as lpf
import nkUtilities.load__config    as lcf
import nkUtilities.configSettings  as cfs
import nkUtilities.plot1D          as pl1


# ========================================================= #
# ===  roc_for_svm.py                                   === #
# ========================================================= #

def roc_for_svm():

    
    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    nImages = 100
    nPieces = 370
    figsize = (55,55,3)
    imgFile = "../universal_board_images/image{0:04}/extract{1:04}.jpg"
    lblFile = "../universal_board_images/labels.dat"
    modFile = "dat/model.pickle"
    
    # ------------------------------------------------- #
    # --- [2] load images / labels                  --- #
    # ------------------------------------------------- #
    labels_ = lpf.load__pointFile( inpFile=lblFile, returnType="structured" )
    labels_ = np.reshape( np.copy( ( labels_[0:nImages,0:nPieces,4] ) ), (nImages,nPieces) )
    images, labels = [], []
    for ii in range( nImages ):
        for ip in range( nPieces ):
            if ( labels_[ii,ip] >= 0 ):
                imgFile_h = ( imgFile.format( ii+1, ip+1 ) )
                if ( os.path.exists( imgFile_h ) ):
                    images.append( cv2.imread( imgFile_h ) )
                    labels.append( labels_[ii,ip] )
                else:
                    print( "path does not exists :: {}".format( imgFile_h ) )
    images    = np.array( images )
    labels    = np.array( labels )
    

    # ------------------------------------------------- #
    # --- [3] define trainer                        --- #
    # ------------------------------------------------- #
    def trainer_for_svm( Data=None, labels=None ):
        classifier = sklearn.svm.SVC()
        classifier.fit( Data, labels )
        return( classifier )

    # ------------------------------------------------- #
    # --- [4] call evaluate__roc                    --- #
    # ------------------------------------------------- #
    ROCs, AUC = roc.evaluate__ROC( trainer=trainer_for_svm, Data=images, labels=labels, \
                                   returnType="ROCs-AUC", pngFile="png/inRoutine_roc_curve.png" )

    # ------------------------------------------------- #
    # --- [5] draw roc curve                        --- #
    # ------------------------------------------------- #
    # -- config settings -- #
    fpr_, tpr_ = 0, 1
    pngFile = "png/ROC_for_SVM.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["xTitle"]         = "False Positive Rate"
    config["yTitle"]         = "True Positive Rate"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ -0.1, +1.1 ]
    config["plt_yRange"]     = [ -0.1, +1.1 ]
    config["xMajor_auto"]    = False
    config["yMajor_auto"]    = False
    config["xMajor_ticks"]   = np.linspace( 0.0, 1.0, 6 )
    config["yMajor_ticks"]   = np.linspace( 0.0, 1.0, 6 )
    # --  plot  -- #
    label   = "SVM's ROC ( AUC = {:.3f} )".format( AUC )
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=ROCs[:,fpr_], yAxis=ROCs[:,tpr_], label=label, \
                   linestyle="-", linewidth=2.0, \
                   marker="o", markersize=4.0, color="Orange" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()
    print( "[evaluate__ROC.py] pngFile :: {}".format( pngFile ) )
    
    return()




# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    roc_for_svm()
    
