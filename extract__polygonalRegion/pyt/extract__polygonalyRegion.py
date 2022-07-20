import sys
import cv2
import numpy as np

# ========================================================= #
# ===  extract__polygonalRegion.py                      === #
# ========================================================= #

def extract__polygonalRegion( image=None, polygon=None, returnType="masked" ):

    black_rgb = ( 255,255,255 )
    black_val = 255

    # ------------------------------------------------- #
    # --- [1] argument  check                       --- #
    # ------------------------------------------------- #
    if ( image   is None ): sys.exit( "[extract__polygonalyRegion.py] image   == ???" )
    if ( polygon is None ): sys.exit( "[extract__polygonalyRegion.py] polygon == ???" )

    mask    = np.zeros_like( image )
    if   ( type( polygon ) == list ):
        polygon = np.array( polygon )
    elif ( type( polygon ) == np.ndarray ):
        pass
    else:
        print( "[extract__polygonalyRegion.py] polygon is not list or numpy.ndarray " )
        sys.exit()
    if ( polygon.ndim != 2 ):
        print( "[extract__polygonalyRegion.py] polygon's shape is not [nPolygon,2] " )
        sys.exit()
    else:
        if ( polygon.shape[1] != 2 ):
            print( "[extract__polygonalyRegion.py] polygon's shape is not [nPolygon,2] " )
            sys.exit()
        else:
            nPolygon = polygon.shape[0]
    
    # ------------------------------------------------- #
    # --- [2] generate mask                         --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() in [ "mask"   ] ):
        mask      = cv2.fillConvexPoly( mask, polygon, color=black_rgb )
        return( mask )

    elif ( returnType.lower() in [ "masked" ] ):
        mask      = cv2.fillConvexPoly( mask, polygon, color=black_rgb )
        masked    = np.where( mask==black_val, image, mask )
        return( masked )

    else:
        print( "[extract__polygonalyRegion.py] unknown returnType :: {} ".format( returnType ) )
        sys.exit()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile = "jpg/coin__onSheet.jpg"
    polygon = np.array( [ [0,0],
                          [1500,200],
                          [3024,100],
                          [3024,3700],
                          [100,3700],
    ] )

    image   = cv2.imread( inpFile )
    ret     = extract__polygonalRegion( image=image, polygon=polygon )

    cv2.imshow( "masked", ret )
    cv2.waitKey( int(1e6) )
