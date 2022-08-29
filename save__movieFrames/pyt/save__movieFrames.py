import os, sys
import cv2
import numpy as np


# ========================================================= #
# ===  save__movieFrames.py                             === #
# ========================================================= #

def save__movieFrames( inpFile=None, outFile=None, output_format="jpg", resize=None, \
                       frame_to_use=None, silent=False ):

    w_, h_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile  is None ): sys.exit( "[save__movieFrames.py] inpFile == ???" )
    baseName, input_ext = os.path.splitext( os.path.basename( inpFile ) )
    if ( outFile  is None ): outFile = baseName
    
    if ( not( input_ext.strip(".").lower() in [ "mov", "mp4" ] ) ):
        print( "[save__movieFrames.py] illegal file extention....  ( .mov or .mp4 )  [ERROR] " )
        print( "[save__movieFrames.py] inpFile = {} ".format( inpFile ) )
        print( "[save__movieFrames.py] extention  = {} ".format( input_ext  ) )
        sys.exit()
    if ( not( output_format.strip(".").lower() in [ "jpg", "png", "tiff" ] ) ):
        print( "[save__movieFrames.py] illegal file extention....  ( .mov or .mp4 )  [ERROR] " )
        print( "[save__movieFrames.py] extention  = {} ".format( output_format ) )
        sys.exit()
    print()
    
    # ------------------------------------------------- #
    # --- [2] load capture                          --- #
    # ------------------------------------------------- #
    cap = cv2.VideoCapture( inpFile )
    if ( cap.isOpened() is False ):
        print( "[save__movieFrames.py] cannot open file... [ERROR]  inpFile :: {} ".format( inpFile ) )
        return
    else:
        print( "[save__movieFrames.py] save frames in movie :: {} ".format( inpFile ) )

    # ------------------------------------------------- #
    # --- [3] resize images                         --- #
    # ------------------------------------------------- #
    width  = cap.get( cv2.CAP_PROP_FRAME_WIDTH  )
    height = cap.get( cv2.CAP_PROP_FRAME_HEIGHT )
    if ( resize is not None ):
        if   ( ( resize[w_] is     None ) and ( resize[h_] is not None ) ):
            resize_ = [ int( width/height*resize[h_]), int( resize[h_] ) ]
        elif ( ( resize[w_] is not None ) and ( resize[h_] is     None ) ):
            resize_ = [ int( resize[w_] ), int( height/width*resize[w_]) ]
        elif ( ( resize[w_] is not None ) and ( resize[h_] is not None ) ):
            resize_ = [ int(val) for val in resize ]
    else:
        resize_ = [ int(width), int(height) ]

    if ( not( silent ) and resize is not None ):
        print( "[save__movieFrames.py] resize image         :: ( w x h = {} x {} ) "\
               .format( resize_[w_], resize_[h_] ) )

    # ------------------------------------------------- #
    # --- [4] choose frames                         --- #
    # ------------------------------------------------- #
    if ( frame_to_use is None ):
        frame_to_use = "all"
    if   ( type( frame_to_use ) is str   ):
        if ( frame_to_use.lower() == "all" ): # all 
            frame_to_use = "all"
    elif ( type( frame_to_use ) is int   ): # 11 = [ first, last ] => 11 division
        frame_to_use = np.linspace( 0, float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ), frame_to_use )
        frame_to_use = [ int(val) for val in frame_to_use ]
        
    elif ( type( frame_to_use ) is list  ): # [ 0.1, 0.9, 11 ] =   [0.1,0.9] => 11 division
        from_         = int( frame_to_use[0]*float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ) )
        to_           = int( frame_to_use[1]*float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ) )
        frame_to_use = np.linspace( from_, to_, frame_to_use[2] )
        frame_to_use = [ int(val) for val in frame_to_use ]

    # ------------------------------------------------- #
    # --- [3] prepare for saving                    --- #
    # ------------------------------------------------- #
    os.makedirs( outFile, exist_ok=True )
    outFile_base = os.path.join( outFile, baseName )
    digit        = max( len( str( int( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ) ) ), 4 )
    print( "[save__movieFrames.py] output path          :: {} ".format( outFile ) ) 
    print()

    # ------------------------------------------------- #
    # --- [4] devide into images                    --- #
    # ------------------------------------------------- #

    if   ( type(frame_to_use) is str  ):
        
        if ( frame_to_use.lower() == "all" ):
            ik = 0
            while True:
                ret, frame = cap.read()
                if ( ret ):
                    num_     = "_{}.".format( str(ik).zfill(digit) )
                    outFile_ = outFile_base + num_ + output_format
                    if ( not( silent ) ):
                        print( "[save__movieFrames.py] output image file :: {} ".format( outFile_ ) )
                    if ( resize is not None ):
                        frame = cv2.resize( frame, dsize=resize_ )
                    cv2.imwrite( outFile_, frame )
                    ik += 1
                else:
                    break

    elif ( type(frame_to_use) is list ):
        
        for ik,frame_index in enumerate( frame_to_use ):
            cap.set( cv2.CAP_PROP_POS_FRAMES, frame_index )  # too slow...
            ret, frame = cap.read()
            if ( ret ):
                num_     = "_{}.".format( str(ik).zfill(digit) )
                outFile_ = outFile_base + num_ + output_format
                if ( not( silent ) ):
                    print( "[save__movieFrames.py] output image file :: {} ".format( outFile_ ) )
                if ( resize is not None ):
                    frame = cv2.resize( frame, dsize=resize_ )
                cv2.imwrite( outFile_, frame )
            else:
                break
    return


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile       = "mov/sample.MOV"
    outFile       = "jpg/sample"
    resize        = (320,640)
    frame_to_use = 11
    save__movieFrames( inpFile=inpFile, outFile=outFile, \
                       resize=resize, frame_to_use=frame_to_use )
