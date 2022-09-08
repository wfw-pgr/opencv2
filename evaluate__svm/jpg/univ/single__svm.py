import numpy as np
import cv2
import os, sys
import judge__imagesBySVC      as svc
import sklearn.model_selection as skms


# ========================================================= #
# ===  evaluate__svm.py                                 === #
# ========================================================= #

def evaluate__svm():

    nImages = 1
    nPieces = 375
    imgDir  = "jpg/univ/image/"
    imgFile = os.path.join( imgDir, "univ_{0:04}.jpg" )
    modFile = "dat/model.pickle"
    lblFile = "jpg/univ/labels.dat"
    
    # ------------------------------------------------- #
    # --- [1] load images / labels                  --- #
    # ------------------------------------------------- #
    images  = []
    ii_ip   = []
    for ii in range( nPieces ):
        images += [ cv2.imread( imgFile.format( ii+1 ) ) ]
    images  = np.array( images )

    import nkUtilities.load__pointFile as lpf
    labels_ = lpf.load__pointFile( inpFile=lblFile, returnType="structured" )
    labels  = np.copy( ( labels_[:,4] ) )

    # ------------------------------------------------- #
    # --- [2] train / test split                    --- #
    # ------------------------------------------------- #
    train_size   = 0.5
    shuffle      = True
    random_state = 314
    img_train, img_test = skms.train_test_split( images, train_size=train_size, \
                                                 shuffle=shuffle, random_state=random_state )
    ans_train, ans_test = skms.train_test_split( labels, train_size=train_size, \
                                                 shuffle=shuffle, random_state=random_state )
    
    # ------------------------------------------------- #
    # --- [2] train svc                             --- #
    # ------------------------------------------------- #
    train = svc.judge__imagesBySVC( images=img_train, labels=ans_train, mode="train", \
                                    trainedModelFile=modFile, random_state=7 )
    # ------------------------------------------------- #
    # --- [3] test svc                              --- #
    # ------------------------------------------------- #
    prd_test   = svc.judge__imagesBySVC( images=img_test , mode="test", \
                                         trainedModelFile=modFile, returnType="result" )
    classifier = svc.judge__imagesBySVC( images=img_test , mode="test", \
                                         trainedModelFile=modFile, returnType="classifier" )
    img_test_  = np.reshape( img_test, ( img_test.shape[0],-1) )
    
    compares  = np.concatenate( [ ans_test[:,None], prd_test[:,None] ], axis=1 )
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/compares.dat"
    spf.save__pointFile( outFile=outFile, Data=compares )
    accuracy  = ( 1.0 - np.sum( np.abs( prd_test - ans_test ) ) / prd_test.shape[0] ) * 100.0
    print( " accuracy :: {}".format( accuracy ) )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    evaluate__svm()
    
