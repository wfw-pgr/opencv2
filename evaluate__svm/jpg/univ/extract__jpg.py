import os, sys, cv2
import numpy as np
import matplotlib.pyplot as plt
import nkOpenCV.put__rectangular as rec
import nkOpenCV.extract__rectangularRegion as ext

# ========================================================= #
# ===  extract__jpg.py                                  === #
# ========================================================= #

def extract__jpg():

    x_, y_, z_ = 0, 1, 2
    
    inpFile = "universal_board2.jpg"
    image   = cv2.imread( inpFile )
    # image   = cv2.cvtColor( cv2.imread( inpFile ), cv2.COLOR_BGR2RGB )
    w,h     = image.shape[1], image.shape[0]
    nHole_w = 15
    nHole_h = 25
    Nx, Ny  = 101, 101
    # rescale = (50,50)
    rescale = (100,100)

    xLine_v = [ (w/nHole_w)*ik for ik in range( nHole_w+1 ) ]
    yLine_v = [ (h/nHole_h)*ik for ik in range( nHole_h+1 ) ]
    xLine   = np.linspace( 0.0, w, Nx )
    yLine   = np.linspace( 0.0, h, Ny )

    coord1  = np.zeros( (Ny,2,nHole_w+1) )
    coord2  = np.zeros( (Nx,2,nHole_h+1) )
    for ik, xval in enumerate( xLine_v ):
        coord1[:,x_,ik] = np.repeat( xval, Ny )
        coord1[:,y_,ik] = np.copy( yLine )
    for ik, yval in enumerate( yLine_v ):
        coord2[:,x_,ik] = np.copy( xLine )
        coord2[:,y_,ik] = np.repeat( yval, Nx )

    # -- positions -- #
    Lx = w / nHole_w
    Ly = h / nHole_h
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0, w, nHole_w+1 ]
    x2MinMaxNum = [ 0, h, nHole_h+1 ]
    x3MinMaxNum = [ 0, 0,         1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    # x1MinMaxNum = [ 0.5*Lx, w-0.5*Lx, nHole_w ]
    # x2MinMaxNum = [ 0.5*Ly, h-0.5*Ly, nHole_h ]
    # x3MinMaxNum = [    0.0,      0.0,       1 ]
    # coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    #                                  x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    coord       = np.resize( coord[0,:,:,0:2], (nHole_h+1,nHole_w+1,2) )
    bb          = np.concatenate( [ coord[:-1,:-1,:], coord[1:,1:,:] ], axis=2 )
    print( bb.shape )
    bb     = np.reshape( bb, (-1,4) )
    image  = rec.put__rectangular( image=image, bb=bb )
    images = ext.extract__rectangularRegion( image=image, bb=bb, rescale=rescale )
    outFile = "image/univ_{0:04}.jpg"
    for ik,img in enumerate(images):
        cv2.imwrite( outFile.format( ik+1 ), img )
    
    # for ik in range( nHole_w ):
    #     plt.plot( coord1[:,x_,ik], coord1[:,y_,ik], color="blue" )
    # for ik in range( nHole_h ):
    #     plt.plot( coord2[:,x_,ik], coord2[:,y_,ik], color="red"  )
    plt.imshow( image )
    plt.show()
    
    return()



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    extract__jpg()
    
