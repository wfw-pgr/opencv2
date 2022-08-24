import cv2
import os, sys, subprocess, re
import numpy                         as np
import nkUtilities.load__pointFile   as lpf
import nkUtilities.save__pointFile   as spf
import extract__rectangularRegion    as err
import draw__circlesOnImage          as dci


# ========================================================= #
# ===  check__itemsOnSheet.py                           === #
# ========================================================= #

def check__itemsOnSheet():

    x_, y_, rc_ = 0, 1, 2
    bgr_colors  = np.array( [ [255,0,0], [0,255,0], [0,0,255] ] )

    # ------------------------------------------------- #
    # --- [1] load parameterFile  &  image          --- #
    # ------------------------------------------------- #
    #  -- [1-1] load parameter File                 --  #
    import nkUtilities.load__constants as lcn
    cnsFile    = "dat/parameter.conf"
    const      = lcn.load__constants( inpFile=cnsFile )

    #  -- [1-2] chc parameter packing               --  #
    import nkBasicAlgs.pack__groupedParameters as pgp
    chc_params = pgp.pack__groupedParameters( const=const, group="chc", strip_groupName=True )
    
    #  -- [1-3] load images                         --  #
    import load__figure as lfg
    image      = lfg.load__figure( inpFile =const["main.inputFile"], returnType="bgr" )

    #  -- [1-4] load ARmarker/hole Position (ideal) --  #
    markers_id = ( lpf.load__pointFile( inpFile=const["ARmarker.ideal.file"]     ) )[:,1:]
    circles_id =   lpf.load__pointFile( inpFile=const["detectCircle.ideal.file"] )

    #  -- [1-5] load hole position      ( ideal )   --  #
    cpos_id    = np.copy( np.array( circles_id[:,0:2], dtype=np.int32 ) )
    labels     = np.copy( np.array( circles_id[:,  3], dtype=np.int32 ) )

    
    # ------------------------------------------------- #
    # --- [2] detect marker and crip around it      --- #
    # ------------------------------------------------- #
    import detect__ARmarker          as dar
    import extract__polygonalRegion  as epr
    markers,ARids   = dar.detect__ARmarker( image=image, \
                                            markerType=const["ARmarker.markerType"], \
                                            reorder   =const["ARmarker.reorder"] )
    markers_ph      = np.average( markers, axis=1 ).astype( np.int32 )
    img_, poly_, bb = epr.extract__polygonalRegion( image=image, polygon=markers_ph, bb="auto" )
    
    if ( const["ARmarker.checkImage.sw"] ):
        cv2.imwrite( const["ARmarker.checkImage.file"], img_ )

        
    # ------------------------------------------------- #
    # --- [3] detect circles in Image               --- #
    # ------------------------------------------------- #
    if ( const["detectCircle.method"].lower() == "canny-hough" ):
        import detect__circleCannyHough as cch
        circles, img_ = cch.detect__circleCannyHough( image=img_, **chc_params )
        if ( circles is None ):
            print( "[check__itemsOnSheet.py] None circles was detected. " )
            sys.exit()
        else:
            offsets = np.repeat( np.array( bb[x_:y_+1] )[None,:], circles.shape[0], axis=0 )
            cpos_ph = np.copy( circles[:,0:2] ) + offsets
            length  = np.copy( circles[:,rc_] * 2.0 )
    
    if ( const["detectCircle.checkImage.sw"] ):
        img_ = dci.draw__circlesOnImage( image=image, posit=cpos_ph, radii=circles[:,rc_] )
        cv2.imwrite( const["detectCircle.checkImage.file"], img_ )

        
    # ------------------------------------------------- #
    # --- [4] match circles position                --- #
    # ------------------------------------------------- #
    import transcribe__holePosition as thp
    import match__holePosition      as mhp
    cpos_id_ = thp.transcribe__holePosition( markers_id=markers_id, detected_ARids=ARids,
                                             markers_ph=markers_ph, cpos_id       =cpos_id )
    index    = mhp.match__holePosition( pos1=cpos_id_, pos2=cpos_ph, indexType="2->1", \
                                        max_distance=const["matchCircle.max_distance"] )
    labels_  = labels[index]

    if ( const["matchCircle.checkImage.sw"] ):
        colors = bgr_colors[ np.array( labels_, dtype=np.int32 ) ]
        img_   = dci.draw__circlesOnImage( image=image, posit=cpos_ph, colors=colors, \
                                           radii=np.repeat( 20.0, cpos_ph.shape[0] ) )
        cv2.imwrite( const["matchCircle.checkImage.file"], img_ )

        
    # ------------------------------------------------- #
    # --- [5] extract detected circles              --- #
    # ------------------------------------------------- #
    img_       = cv2.cvtColor( np.copy( image ), cv2.COLOR_BGR2GRAY )
    img_pieces = err.extract__rectangularRegion( image=img_, center_pos=cpos_ph, length=length,\
                                                 margin =const["crip.margin" ], \
                                                 rescale=const["crip.rescale"] )
    if ( const["crip.checkImage.sw"] ):
        import glob
        if ( len( glob.glob( "jpg/crip/*.jpg" ) ) > 0 ):
            subprocess.call( "rm -r jpg/crip/*.jpg", shell=True )
        for ik,img in enumerate( img_pieces ):
            cv2.imwrite( const["crip.checkImage.file"].format( ik+1, labels_[ik] ), img )

    # ------------------------------------------------- #
    # --- [6] judge images by CNN / SVC             --- #
    # ------------------------------------------------- #
    if   ( const["ml.classifierType"].lower() == "svc" ):
        import judge__imagesBySVC as svc
        if ( const["ml.trainMode"] ):
            print( "hi" )
            svc.judge__imagesBySVC( images=img_pieces, labels=labels_, trainMode=True, \
                                    trainedModelFile=const["ml.trainedModelFile"] )
            print( "[check__itemsOnSheet.py] training completed... [END] " )
            sys.exit()
        else:
            pred = svc.judge__imagesBySVC( images=img_pieces, \
                                           trainedModelFile=const["ml.trainedModelFile"] )
            
    elif ( const["ml.classifierType"].lower() == "cnn" ):
        import judge__imagesByCNN as cnn
        if ( const["ml.trainMode"] ):
            cnn.judge__imagesByCNN( images=img_pieces, labels=labels_, trainMode=True, \
                                    trainedModelFile=const["ml.trainedModelFile"] )
            print( "[check__itemsOnSheet.py] training completed... [END] " )
            sys.exit()
        else:
            pred = cnn.judge__imagesByCNN( images=img_pieces, \
                                           trainedModelFile=const["ml.trainedModelFile"] )
    
    # ------------------------------------------------- #
    # --- [7] save / evaluate result                --- #
    # ------------------------------------------------- #
    diff     = pred - labels_
    check    = np.concatenate( [pred[:,None],labels_[:,None],diff[:,None],], axis=1 )
    accuracy = ( 1.0 - ( np.sum( np.abs(diff) ) / diff.shape[0] ) ) * 100.0
    spf.save__pointFile( outFile=const["main.outputFile"], Data=check, \
                         names=[ "prediction", "label", "diff" ] )
    print( "\n[check__itemsOnSheet.py]  Accuracy  :: {} (%) \n".format( accuracy ) )

    # ------------------------------------------------- #
    # --- [8] display circles                       --- #
    # ------------------------------------------------- #
    colors       = bgr_colors[ diff+1 ]
    circles      = np.insert( cpos_ph, 2, 20.0, axis=1 )
    if    ( const["main.displayMode"].lower() == "all"  ):
        pass
    elif  ( const["main.displayMode"].lower() == "diff" ):
        index    = np.where( np.abs(diff) > 0 )
        circles  = circles[ index ]
        colors   = colors [ index ]
    img_ = dci.draw__circlesOnImage( image=image, circles=circles, colors=colors )
    cv2.imwrite( const["main.result.file"], img_ )
    print( "\n[check__itemsOnSheet.py] result image :: {}\n".format(const["main.result.file"]) )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    check__itemsOnSheet()
