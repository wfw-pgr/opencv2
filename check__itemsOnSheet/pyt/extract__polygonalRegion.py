import os, sys
import cv2
import numpy as np

# return :: ( mask, polygon, bb )
#           mask :: [  ]

# ========================================================= #
# ===  extract__polygonalRegion.py                      === #
# ========================================================= #

def extract__polygonalRegion( image=None, polygon=None, bb=None, returnType="masked" ):

    x_, y_    = 0, 1
    black_rgb = ( 255,255,255 )
    black_val = 255

    # ------------------------------------------------- #
    # --- [1] argument  check                       --- #
    # ------------------------------------------------- #
    if ( image   is None ): sys.exit( "[extract__polygonalyRegion.py] image   == ???" )
    if ( polygon is None ): sys.exit( "[extract__polygonalyRegion.py] polygon == ???" )
    image_ = np.copy( image )
    if   ( image_.ndim == 3 ):
        image_ = cv2.cvtColor( image_, cv2.COLOR_BGR2GRAY )


    # ------------------------------------------------- #
    # --- [2] polygon type check                    --- #
    # ------------------------------------------------- #
    mask    = np.zeros_like( image_ )
    if   ( type( polygon ) == list ):
        polygon = np.array( polygon )
    elif ( type( polygon ) == np.ndarray ):
        pass
    else:
        print( "[extract__polygonalyRegion.py] polygon is not list or numpy.ndarray " )
        sys.exit()
        
    # ------------------------------------------------- #
    # --- [3] polygon shape / bb type check         --- #
    # ------------------------------------------------- #
    nPolygon = polygon.shape[0]
    if ( not( polygon.shape == (nPolygon,2) ) ):
        print( "[extract__polygonalyRegion.py] polygon's shape is not [nPolygon,2] " )
        sys.exit()
    if ( type(bb) == str ):
        if ( bb.lower() == "auto" ):
            bb = [ np.min( polygon[:,x_] ), np.min( polygon[:,y_] ), \
                   np.max( polygon[:,x_] ), np.max( polygon[:,y_] )  ]
        
    # ------------------------------------------------- #
    # --- [4] generate mask                         --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() in [ "mask"   ] ):
        mask      = cv2.fillConvexPoly( mask, polygon, color=black_rgb )
        if ( bb is not None ):
            mask           = mask[ bb[1]:bb[3], bb[0]:bb[2], ... ]
            polygon_       = np.copy( polygon )
            polygon_[:,x_] = polygon[:,x_] - bb[0]
            polygon_[:,y_] = polygon[:,y_] - bb[1]
        return( mask, polygon_, bb )

    elif ( returnType.lower() in [ "masked" ] ):
        mask      = cv2.fillConvexPoly( mask, polygon, color=black_rgb )
        masked    = np.where( mask==black_val, image_, mask )
        if ( bb is not None ):
            masked         = masked[ bb[1]:bb[3], bb[0]:bb[2], ... ]
            polygon_       = np.copy( polygon )
            polygon_[:,x_] = polygon[:,x_] - bb[0]
            polygon_[:,y_] = polygon[:,y_] - bb[1]
        return( masked, polygon_, bb )

    else:
        print( "[extract__polygonalyRegion.py] unknown returnType :: {} ".format( returnType ) )
        sys.exit()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile = "jpg/coin__onSheet.jpg"
    polygon = np.array( [ [300,0],
                          [1500,200],
                          [3024,100],
                          [3024,3700],
                          [100,3700],
    ] )

    image    = cv2.imread( inpFile )
    ret,poly = extract__polygonalRegion( image=image, polygon=polygon, bb="auto" )
    print( polygon )
    print( poly )
    cv2.imshow( "masked", ret )
    cv2.waitKey( int(1e6) )
