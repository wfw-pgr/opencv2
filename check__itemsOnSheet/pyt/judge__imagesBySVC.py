import os, sys, pickle
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.model_selection as skms
import sklearn.svm
import sklearn.metrics


# ========================================================= #
# === judge__imagesBySVC.py                             === #
# ========================================================= #

def judge__imagesBySVC( images=None, labels=None, trainMode=False, \
                        trainedModelFile=None, train_size=0.8, shuffle=True, random_state=10 ):

    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( images           is None ): sys.exit( "[judge__imagesBySVC.py] images == ???" )
    if ( trainedModelFile is None ): sys.exit( "[judge__imagesBySVC.py] trainedModelFile == ???" )

    nImages    = images.shape[0]
    images_svc = np.reshape( images, (nImages,-1) )
    
    # ------------------------------------------------- #
    # --- [2] train classifier / save classifier    --- #
    # ------------------------------------------------- #
    if ( trainMode ):
        print( "[judge__imagesBySVC.py] trainMode :: train and save model in file : {}"\
               .format( trainedModelFile ) )
        if ( labels is None ): sys.exit( "[judge__imagesBySVC.py] labels == ???" )
        img_train, img_test = skms.train_test_split( images_svc, train_size=train_size, \
                                                     shuffle=shuffle, random_state=random_state )
        ans_train, ans_test = skms.train_test_split( labels, train_size=train_size, \
                                                     shuffle=shuffle, random_state=random_state )
        classifier = sklearn.svm.SVC()
        print( img_train.shape, ans_train.shape )
        classifier.fit( img_train, ans_train )
        prd_test   = classifier.predict( img_test )
        accuracy   = sklearn.metrics.accuracy_score( prd_test, ans_test )
        with open( trainedModelFile, "wb" ) as f:
            pickle.dump( classifier, f )
        print( "\n[judge__imagesBySVC.py] trained model accuracy :: {} (%) \n".format(accuracy) )
        print( "[judge__imagesBySVC.py] trainMode :: train and save model in file : {}  [Done]"\
               .format( trainedModelFile ) )
        return()
        
    # ------------------------------------------------- #
    # --- [3] load classifier                       --- #
    # ------------------------------------------------- #
    with open( trainedModelFile, "rb" ) as f:
        classifier = pickle.load( f )
        
    # ------------------------------------------------- #
    # --- [4] predict using classifier and return   --- #
    # ------------------------------------------------- #
    prd_test   = classifier.predict( images_svc )
    return( prd_test )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    judge__imagesBySVC()
