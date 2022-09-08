import os, sys, pickle
import numpy                   as np
import sklearn
import sklearn.datasets
import sklearn.model_selection as skms
import sklearn.svm
import sklearn.metrics

# ========================================================= #
# === judge__imagesBySVC.py                             === #
# ========================================================= #

def judge__imagesBySVC( images=None, labels=None, mode=None, probability=False, \
                        returnType="result", \
                        trainedModelFile=None, train_size=0.8, shuffle=True, random_state=10 ):

    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( images           is None ): sys.exit( "[judge__imagesBySVC.py] images           == ???" )
    if ( trainedModelFile is None ): sys.exit( "[judge__imagesBySVC.py] trainedModelFile == ???" )
    if ( mode             is None ): sys.exit( "[judge__imagesBySVC.py] mode             == ???" )
    nImages    = len( images )
    images_svc = np.reshape( np.array( images ), (nImages,-1) )
    if ( not( mode.lower() in [ "train", "test" ] ) ):
        print( "[judge__imagesBySVC.py] mode is not [ train, test ]   [ERROR] " )
        sys.exit()
        
    # ------------------------------------------------- #
    # --- [2] train classifier / save classifier    --- #
    # ------------------------------------------------- #
    if ( mode.lower() == "train" ):
        if ( labels is None ):
            sys.exit( "[judge__imagesBySVC.py] [trainMode] labels == ???" )
        img_train, img_test = skms.train_test_split( images_svc, train_size=train_size, \
                                                     shuffle=shuffle, random_state=random_state )
        ans_train, ans_test = skms.train_test_split( labels    , train_size=train_size, \
                                                     shuffle=shuffle, random_state=random_state )
        print( "[judge__imagesBySVC.py] training is undergoing..... ", end="" )
        classifier = sklearn.svm.SVC()
        classifier.fit( img_train, ans_train )
        prd_test   = classifier.predict( img_test )
        accuracy   = sklearn.metrics.accuracy_score( prd_test, ans_test ) * 100.0
        print( "   [Done]" )
        print( "[judge__imagesBySVC.py] trained model accuracy :: {} (%) \n".format(accuracy) )
        print( "[judge__imagesBySVC.py] trainMode :: train and save model in file : {}"\
               .format( trainedModelFile ), end="" )
        with open( trainedModelFile, "wb" ) as f:
            pickle.dump( classifier, f )
        print( "   [Done]" )
        return( classifier )
        
    # ------------------------------------------------- #
    # --- [3] predict answer using classifier       --- #
    # ------------------------------------------------- #
    if ( mode.lower() == "test" ):
        with open( trainedModelFile, "rb" ) as f:
            classifier = pickle.load( f )
        if ( probability is True ):
            prd_test = classifier.predict_proba( images_svc )
        else:
            prd_test   = classifier.predict( images_svc )
        if ( returnType.lower() == "classifier" ):
            return( classifier )
        else:
            return( prd_test )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    judge__imagesBySVC()
