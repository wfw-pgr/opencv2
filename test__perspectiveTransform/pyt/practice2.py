import os, sys
import numpy as np
import cv2


# ========================================================= #
# ===  practice2                                        === #
# ========================================================= #

def practice2():

    x_,y_,t_ = 0, 1, 2
    src_pts  = np.array( [ [ 0, 0 ],
                           [ 1, 0 ],
                           [ 1, 1.2 ],
                           [ 0, 1 ] ], dtype=np.float32 )
    dst_pts  = np.array( [ [ 0, 0 ],
                           [ 1, 0 ],
                           [ 1, 1 ],
                           [ 0, 1 ] ], dtype=np.float32 )
    cvt_pts  = np.array( [ [ 0.0,   0 ],
                           [ 0.97,  0 ],
                           [ 1.0, 2.0 ],
                           [ 0.0,   1 ] ], dtype=np.float32 )
    
    cvt_pts  = np.concatenate( [cvt_pts,np.ones( (cvt_pts.shape[0],1))], axis=1 )
    Matrix   = cv2.getPerspectiveTransform( src_pts, dst_pts )
    print( cvt_pts.shape )
    print( Matrix.shape )
    print( cvt_pts )

    ret = np.transpose( np.matmul( Matrix, np.transpose( cvt_pts ) ) )
    ret = ret / np.repeat( ( ret[:,t_] )[:,None], 3, axis=1 )
    print( ret.shape )
    print( ret )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    practice2()
    
