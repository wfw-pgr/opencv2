import numpy as np
import cv2
import os, sys, time
import judge__imagesBySVC      as svc
import sklearn.model_selection as skms
import nkUtilities.load__pointFile as lpf
import sklearn
import sklearn.metrics
import nkOpenCV.put__rectangular as rec


# ========================================================= #
# ===  evaluate__svm.py                                 === #
# ========================================================= #

def evaluate__svm():

    nImages = 100
    nPieces = 370
    figsize = (55,55,3)
    imgDir  = "../universal_board_images/image{0:04}"
    imgFile = os.path.join( imgDir, "extract{1:04}.jpg" )
    modFile = "dat/model.pickle"
    lblFile = "../universal_board_images/labels.dat"
    
    # ------------------------------------------------- #
    # --- [1] load images / labels                  --- #
    # ------------------------------------------------- #
    labels_ = lpf.load__pointFile( inpFile=lblFile, returnType="structured" )
    labels_ = np.reshape( np.copy( ( labels_[0:nImages,0:nPieces,4] ) ), (nImages,nPieces) )
    images  = []
    labels  = []
    exists  = []
    for ii in range( nImages ):
        for ip in range( nPieces ):
            if ( labels_[ii,ip] >= -1.e-3 ):
                imgFile_h = ( imgFile.format( ii+1, ip+1 ) )
                if ( os.path.exists( imgFile_h ) ):
                    images.append( cv2.imread( imgFile_h ) )
                    labels.append( labels_[ii,ip] )
                else:
                    print( "path does not exists :: {}".format( imgFile_h ) )
    images    = np.array( images )
    labels    = np.array( labels )

    # outFile = "jpg/true/true_{0:04}.jpg"
    # bb1 = np.array( [ [ 0,0,figsize[0]-1  ,figsize[1]-1   ] ] )
    # for ik,img in enumerate(images):
    #     img_ = np.reshape( img, figsize )
    #     img_ = rec.put__rectangular( image=img_, bb=bb1, colorList=[ [0,255,0], [0,0,255] ], \
    #                                  colorValues=np.copy(labels[ik]) )
    #     cv2.imwrite( outFile.format( ik+1 ), img_ )
    # sys.exit()
    
    # ------------------------------------------------- #
    # --- [2] train / test split                    --- #
    # ------------------------------------------------- #
    train_size   = 0.5
    shuffle      = True
    random_state = 300
    img_train, img_test = skms.train_test_split( images, train_size=train_size, \
                                                 shuffle=shuffle, random_state=random_state )
    ans_train, ans_test = skms.train_test_split( labels, train_size=train_size, \
                                                 shuffle=shuffle, random_state=random_state )
    # outFile = "jpg/split/split_{0:04}.jpg"
    # bb1 = np.array( [ [ 0,0,figsize[0]-1  ,figsize[1]-1   ] ] )
    # for ik,img in enumerate(img_test):
    #     img_ = np.reshape( img, figsize )
    #     img_ = rec.put__rectangular( image=img_, bb=bb1, colorList=[ [0,255,0], [0,0,255] ], \
    #                                  colorValues=np.copy(ans_test[ik]) )
    #     cv2.imwrite( outFile.format( ik+1 ), img_ )
    # sys.exit()
    
    # ------------------------------------------------- #
    # --- [2] train svc                             --- #
    # ------------------------------------------------- #
    train = svc.judge__imagesBySVC( images=img_train, labels=ans_train, mode="train", \
                                    trainedModelFile=modFile )
    
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

    confMatrix = sklearn.metrics.confusion_matrix( np.copy(ans_test), np.copy(prd_test) )
    print( confMatrix )

    thickness = 2
    w         = 2*thickness
    bb1 = np.array( [ [ 0,0,figsize[0]-1  ,figsize[1]-1   ] ] )
    bb2 = np.array( [ [ w,w,figsize[0]-1-w,figsize[1]-1-w ] ] )
    outFile = "jpg/out/pred_{0:04}.jpg"
    for ik,img in enumerate(img_test):
        img_ = np.reshape( img, figsize )
        img_ = rec.put__rectangular( image=img_, bb=bb1, colorList=[ [0,255,0], [0,0,255] ], \
                                     colorValues=np.copy(prd_test[ik]) )
        img_ = rec.put__rectangular( image=img_, bb=bb2, colorList=[ [0,255,0], [0,0,255] ], \
                                     colorValues=np.copy(ans_test[ik]) )
        cv2.imwrite( outFile.format( ik+1 ), img_ )

        

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    evaluate__svm()
    
