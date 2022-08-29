import os, sys
import cv2
import numpy as np


# ========================================================= #
# ===  load__movieFrames.py                             === #
# ========================================================= #

def load__movieFrames( inpFile=None, resize=None, frame_to_use=None ):

    w_, h_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile  is None ): sys.exit( "[load__movieFrames.py] inpFile == ???" )
    baseName, input_ext = os.path.splitext( os.path.basename( inpFile ) )
    
    if ( not( input_ext.strip(".").lower() in [ "mov", "mp4" ] ) ):
        print( "[load__movieFrames.py] illegal file extention....  ( .mov or .mp4 )  [ERROR] " )
        print( "[load__movieFrames.py] inpFile = {} ".format( inpFile ) )
        print( "[load__movieFrames.py] extention  = {} ".format( input_ext  ) )
        sys.exit()
    print()
    
    # ------------------------------------------------- #
    # --- [2] load capture                          --- #
    # ------------------------------------------------- #
    cap = cv2.VideoCapture( inpFile )
    if ( cap.isOpened() is False ):
        print( "[load__movieFrames.py] cannot open file... [ERROR]  inpFile :: {} ".format( inpFile ) )
        return
    else:
        print( "[load__movieFrames.py] save frames in movie :: {} ".format( inpFile ) )

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

    if ( resize is not None ):
        print( "[load__movieFrames.py] resize image         :: ( w x h = {} x {} ) "\
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
    # --- [5] devide into images                    --- #
    # ------------------------------------------------- #

    images = []
    
    if   ( type(frame_to_use) is str  ):
        
        if ( frame_to_use.lower() == "all" ):
            while True:
                ret, frame = cap.read()
                if ( ret ):
                    if ( resize is not None ):
                        frame = cv2.resize( frame, dsize=resize_ )
                    images.append( frame )
                else:
                    break

    elif ( type(frame_to_use) is list ):
        
        for ik,frame_index in enumerate( frame_to_use ):
            cap.set( cv2.CAP_PROP_POS_FRAMES, frame_index )  # too slow...
            ret, frame = cap.read()
            if ( ret ):
                if ( resize is not None ):
                    frame = cv2.resize( frame, dsize=resize_ )
                images.append( frame )
            else:
                break
            
    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    cap.release()
    images = np.array( images )
    return( images )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile       = "mov/sample.MOV"
    # resize        = (320,640)
    # frame_to_use = 11
    resize        = None
    frame_to_use = None
    ret = load__movieFrames( inpFile=inpFile, resize=resize, frame_to_use=frame_to_use )
    print( ret.shape )
