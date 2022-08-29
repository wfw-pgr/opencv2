import os, sys
import cv2
import numpy as np

# ========================================================= #
# ===  resample__movie.py                               === #
# ========================================================= #

def resample__movie( inpFile=None, outFile=None, output_format=None, \
                     resize=None, frame_to_save=None, frame_rate=None ):

    w_, h_ = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ):
        sys.exit( "[resample__movie.py] inpFile == ???" )
    if ( outFile is None ):
        input_base, input_format = os.path.splitext( inpFile )
        if ( output_format is None ):
            output_format = input_format
        outFile = ".".join( [ input_base+"_resized", ( output_format.strip(".") ).lower() ] )

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
            resize_ = [ int( width/height*resize[h_]), int(resize[h_]) ]
        elif ( ( resize[w_] is not None ) and ( resize[h_] is     None ) ):
            resize_ = [ int(resize[w_]), int( height/width*resize[w_]) ]
        elif ( ( resize[w_] is not None ) and ( resize[h_] is not None ) ):
            resize_ = [ int(val) for val in resize ]
    else:
        resize_ = [ int(width), int(height) ]
    if ( resize is not None ):
        print( "[save__movieFrames.py] resize image         :: ( w x h = {} x {} ) "\
               .format( resize_[w_], resize_[h_] ) )

    # ------------------------------------------------- #
    # --- [4] choose frames                         --- #
    # ------------------------------------------------- #
    if ( frame_to_save is None ):
        frame_to_save = "all"
    if   ( type( frame_to_save ) is str   ):
        if ( frame_to_save.lower() == "all" ): # all 
            frame_to_save = "all"
    elif ( type( frame_to_save ) is int   ): # 11 = [ first, last ] => 11 division
        frame_to_save = np.linspace( 0, float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ), frame_to_save )
        frame_to_save = [ int(val) for val in frame_to_save ]
        
    elif ( type( frame_to_save ) is list  ): # [ 0.1, 0.9, 11 ] =   [0.1,0.9] => 11 division
        from_         = int( frame_to_save[0]*float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ) )
        to_           = int( frame_to_save[1]*float( cap.get( cv2.CAP_PROP_FRAME_COUNT )-1 ) )
        frame_to_save = np.linspace( from_, to_, frame_to_save[2] )
        frame_to_save = [ int(val) for val in frame_to_save ]


    # ------------------------------------------------- #
    # --- [5] prepare for saving                    --- #
    # ------------------------------------------------- #
    if ( frame_rate is None ):
        frame_rate = int( cap.get(cv2.CAP_PROP_FPS) )
    write_format = cv2.VideoWriter_fourcc( "m", "p", "4", "v" )
    print( resize_ )
    writer       = cv2.VideoWriter( outFile, write_format, frame_rate, tuple(resize_) )
    print( "[save__movieFrames.py] outFile          :: {} ".format( outFile  ) ) 
    print()


    # ------------------------------------------------- #
    # --- [6] devide into images                    --- #
    # ------------------------------------------------- #
    
    if   ( type(frame_to_save) is str  ):
        
        if ( frame_to_save.lower() == "all" ):
            ik = 0
            while True:
                ret, frame = cap.read()
                if ( ret ):
                    if ( resize is not None ):
                        frame = cv2.resize( frame, dsize=resize_ )
                    writer.write(frame)
                    ik += 1
                else:
                    break

    elif ( type(frame_to_save) is list ):
        
        for ik,frame_index in enumerate( frame_to_save ):
            cap.set( cv2.CAP_PROP_POS_FRAMES, frame_index )  # too slow...
            ret, frame = cap.read()
            if ( ret ):
                if ( resize is not None ):
                    frame = cv2.resize( frame, dsize=resize_ )
                writer.write(frame)
            else:
                break

    # ------------------------------------------------- #
    # --- [7] end                                   --- #
    # ------------------------------------------------- #
    writer.release()
    cap.release()
    return

    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile       = "mov/sample.MOV"
    resize        = (320,640)
    frame_rate    = 1
    frame_to_save = [ 0.2, 0.8, 11 ]
    resample__movie( inpFile=inpFile, resize=resize, frame_to_save=frame_to_save, \
                     frame_rate=frame_rate )
