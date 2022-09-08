import os, sys, cv2
import sklearn, sklearn.svm
import numpy as np
import nkUtilities.load__pointFile as lpf
import nkUtilities.load__config    as lcf
import nkUtilities.configSettings  as cfs
import nkUtilities.plot1D          as pl1
import nkML.gridSearch__hyperParameter as hyp


# ========================================================= #
# ===  gridsearch__svm.py                               === #
# ========================================================= #

def gridsearch__svm():

    p1_, p2_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    nImages = 10
    nPieces = 370
    resize  = None
    imgFile = "../universal_board_images/image{0:04}/extract{1:04}.jpg"
    lblFile = "../universal_board_images/labels.dat"
    pngFile = "png/hyperParameter_search.png"
    datFile = "dat/hyperParams.dat"
    
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
    if ( resize is not None ):
        for ik,img in enumerate( images ):
            images[ik] = cv2.resize( img, dsize=resize )
    images    = np.array( images )
    labels    = np.array( labels )
    images    = np.reshape( images, (images.shape[0],-1) )
    print( images.shape, labels.shape )
    
    # ------------------------------------------------- #
    # --- [3] define trainer / evaluator            --- #
    # ------------------------------------------------- #
    def trainer_for_svm( Data=None, labels=None, C=None, gamma=None  ):
        classifier = sklearn.svm.SVC( C=C, gamma=gamma )
        classifier.fit( Data, labels )
        return( classifier )

    def accuracy_evaluator( pred, true ):
        return( sklearn.metrics.accuracy_score( pred, true ) )
    evaluator = accuracy_evaluator
    
    # ------------------------------------------------- #
    # --- [4] call evaluate__roc                    --- #
    # ------------------------------------------------- #
    params1_list = [ 2.0**(i) for i in list( range( -1, 5, 1 ) ) ]
    params2_list = [ 5.e-9, 1.e-8, 5.e-8, 1.e-7, 5.e-7, 1.e-6 ]
    params_name  = [ "C", "gamma" ]
    scores  = hyp.gridSearch__hyperParameter( trainer=trainer_for_svm, \
                                              evaluator=evaluator, Data=images, \
                                              labels=labels, returnType="scores", \
                                              params1_list=params1_list, \
                                              params2_list=params2_list, \
                                              params_name=params_name, pngFile=pngFile )
    if ( datFile is not None ):
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=datFile, Data=scores )

    # ------------------------------------------------- #
    # --- [5] display                               --- #
    # ------------------------------------------------- #
    display               = True
    display__gamma_sample = False
    if ( display ):
        print( scores )
    if ( display__gamma_sample ):
        gamma_sample = 1.0 / ( images.shape[1] * images.var() )
        print( gamma_sample )
        
    # ------------------------------------------------- #
    # --- [6] draw heatmap                          --- #
    # ------------------------------------------------- #
    if ( pngFile is not None ):
        import nkUtilities.draw__heatmap    as dhm
        xlabels = [ "{:.2e}".format( val ) for val in params1_list ]
        ylabels = [ "{:.2e}".format( val ) for val in params2_list ]
        dhm.draw__heatmap( Data=scores, pngFile=pngFile, \
                           xtitle=params_name[p1_], ytitle=params_name[p2_], \
                           xlabels=xlabels, ylabels=ylabels )


    # ------------------------------------------------- #
    # --- [7] return                                --- #
    # ------------------------------------------------- #
    return()




# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    gridsearch__svm()
    
