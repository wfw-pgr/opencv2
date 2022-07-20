import os, sys
import cv2
import numpy as np

import load__figure                  as lfg
import detect__ARmarker              as dar
import extract__polygonalRegion      as epr
import extract__rectangularRegion    as err
import detect__circleCannyHough      as cch
import draw__circlesOnImage          as dci


# ========================================================= #
# ===  check__itemsOnSheet.py                           === #
# ========================================================= #

def check__itemsOnSheet():

    x0_,y0_,rc_           = 0, 1, 2
    
    inpFile               = "jpg/testSheet.jpg"
    # inpFile               = "jpg/coin__onSheet.jpg"
    markerType            = "aruco.DICT_4X4_50"
    circleDetector        = "Canny-Hough"
    show__CannyHoughImage = True
    display_mode          = "all"
    reordered             = None
    # reordered             = ( 1, 0, 2, 3 )
    margin                = 0.1
    rescale               = (32,32)

    classifierType        = "SVC"
    trainMode             = False
    trainedModelFile      = "dat/trained_model.pickle_bin"

    
    # ------------------------------------------------- #
    # --- [1] load figure                           --- #
    # ------------------------------------------------- #
    img_bgr    = lfg.load__figure    ( inpFile =inpFile, returnType="bgr"   )
    img_gray   = lfg.load__figure    ( inpFile =inpFile, returnType="gray"  )
    
    # ------------------------------------------------- #
    # --- [2] detect marker and crip around it      --- #
    # ------------------------------------------------- #
    markers,ids  = dar.detect__ARmarker( img_gray=img_gray, markerType=markerType )
    if ( reordered is not None ):
        markers  = np.array( [ markers[ik] for ik in reordered ] )
    polygon    = np.average( markers, axis=1 ).astype( np.int32 )
    img_masked, poly_ = epr.extract__polygonalRegion( image=img_gray, polygon=polygon, \
                                                      bb="auto"  )
    markers_actual = np.concatenate( [poly_,] )
    
    # ------------------------------------------------- #
    # --- [3] detect circles                        --- #
    # ------------------------------------------------- #
    if ( circleDetector.lower() == "canny-hough" ):
        params = { "dp":1.1, "param2":0.20, "minDist":0.01, \
                   "iGauss":(3,3), "radiusRange":[0.01,0.07] }
        circles, img_canny = cch.detect__circleCannyHough( image=img_masked, \
                                                           returnType="list" , **params )
    if ( show__CannyHoughImage ):
        outFile  = "jpg/img_canny.jpg"
        img_show = cv2.cvtColor( np.copy( img_canny ), cv2.COLOR_GRAY2RGB )
        img_show = dci.draw__circlesOnImage( image=img_show, circles=circles )
        cv2.imwrite( outFile, img_show )

    # ------------------------------------------------- #
    # --- [4] match hole position                   --- #
    # ------------------------------------------------- #
    markers_ideal = np.copy( markers_actual )
    xypos_i       = np.copy( circles[:,0:2] ) # ideal circles is needed. [UNDER DEVELOPMENT]
    xypos_a       = np.copy( circles[:,0:2] ) 
    import transcribe__holePosition as thp
    xypos_t = thp.transcribe__holePosition( markers_ideal =markers_ideal , detected_ids=ids,
                                            markers_actual=markers_actual, xypos=xypos_i )
    import match__holePosition as mhp
    labels  = np.zeros( (xypos_a.shape[0],) )
    print( labels.shape )
    print( xypos_t.shape )
    ans     = mhp.match__holePosition( xypos_t=xypos_t, xypos_a=xypos_a, values=labels )

    # ------------------------------------------------- #
    # --- [5] extract detected circles              --- #
    # ------------------------------------------------- #
    center_pos = np.copy( circles[:,x0_:y0_+1] )
    length     = np.copy( circles[:,rc_] * 2.0 )
    img_pieces = err.extract__rectangularRegion( image=img_masked, center_pos=center_pos, \
                                                 length=length, margin=margin, rescale=rescale )

    # ------------------------------------------------- #
    # --- [6] judge images by CNN / SVC             --- #
    # ------------------------------------------------- #
    if   ( classifierType.lower() == "svc" ):
        import judge__imagesBySVC as svc
        labels = np.where( np.random.rand( img_pieces.shape[0] ) > 0.7, 1, 0 )
        if ( trainMode ):
            svc.judge__imagesBySVC( images=img_pieces, labels=labels, \
                                    trainedModelFile=trainedModelFile, trainMode=True )
            print( "[check__itemsOnSheet.py] training completed... [END] " )
            sys.exit()
        else:
            ret = svc.judge__imagesBySVC( images=img_pieces, trainedModelFile=trainedModelFile )
            
    elif ( classifierType.lower() == "cnn" ):
        import judge__imagesByCNN as cnn
        labels = np.where( np.random.rand( img_pieces.shape[0] ) > 0.7, 1, 0 )
        if ( trainMode ):
            labels_cnn = None
            judge__imagesByCNN( images=img_pieces, labels=labels, \
                                trainedModelFile=trainedModelFile, trainMode=True )
            print( "[check__itemsOnSheet.py] training completed... [END] " )
            sys.exit()
        else:
            ret = judge__imagesByCNN( images=img_pieces, trainedModelFile=trainedModelFile )
    
    # ------------------------------------------------- #
    # --- [7] make action array                     --- #
    # ------------------------------------------------- #
    # index1 = np.where(   ret == ans                  ) #  0
    # index2 = np.where( ( ret == 1 ) and ( ans == 0 ) ) # -1
    # index3 = np.where( ( ret == 0 ) and ( ans == 1 ) ) # +1
    ans        = np.copy( ret )
    action_arr = np.array( ans - ret )
            
    # ------------------------------------------------- #
    # --- [8] display circles                       --- #
    # ------------------------------------------------- #
    bgr             = np.array( [ [255,0,0], [0,255,0], [0,0,255] ] )
    colors          = np.array( bgr[ np.array( action_arr+1, dtype=np.int32 ) ] )
    if    ( display_mode.lower() == "all" ):
        circles_    = np.copy( circles )
        colors_     = np.copy( colors  )
    elif  ( display_mode.lower() == "diff"):
        index       = np.where( np.abs(action_arr)==1 ) 
        circles_    = circles[ index ]
        colors_     = colors [ index ]

    img_show, poly_ = epr.extract__polygonalRegion( image=img_bgr, polygon=polygon, bb="auto"  )
    img_show = dci.draw__circlesOnImage( image=img_show, circles=circles_, colors=colors_ )
    outFile  = "jpg/img_display.jpg"
    cv2.imwrite( outFile, img_show )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    check__itemsOnSheet()
