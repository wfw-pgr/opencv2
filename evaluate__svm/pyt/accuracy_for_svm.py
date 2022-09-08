import os, sys, cv2
import sklearn, sklearn.svm
import numpy as np
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
    train_size = 0.5
    
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
    def trainer_for_svm( Data=None, labels=None, C=None, gamma=None ):
        classifier = sklearn.svm.SVC( C=C, gamma=gamma )
        classifier.fit( Data, labels )
        return( classifier )

    # ------------------------------------------------- #
    # --- [4] call evaluate__accuracy               --- #
    # ------------------------------------------------- #
    import nkML.evaluate__accuracy as acc
    trainer_params = { "C":8.0, "gamma":1.e-7 }
    ret = acc.evaluate__accuracy( trainer=trainer_for_svm, Data=images, labels=labels, \
                                  trainer_params=trainer_params, train_size=train_size )
    print( ret )
    return()




# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    roc_for_svm()
    
