import numpy as np

# ========================================================= #
# ===  generate__holeData.py                            === #
# ========================================================= #

def generate__holeData():

    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    delta   = 80
    radius  = 20
    Lx,Ly   = 1000, 700
    figsize = (1200,900)
    center  = np.array( [ figsize[0]//2, figsize[1]//2 ] )
    Nx,Ny   = Lx // delta + 1, Ly // delta + 1
    Mx,My   = delta*(Nx-1), delta*(Ny-1)
    hitrate = 0.1

    # ------------------------------------------------- #
    # --- [2] generate coordinate                   --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ (-0.5)*Mx, (+0.5)*Mx, Nx ]
    x2MinMaxNum = [ (-0.5)*My, (+0.5)*My, Ny ]
    x3MinMaxNum = [       0.0,       0.0,  1 ]
    coord1      = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    Nx,Ny       = Nx-1, Ny-1
    Mx,My       = Mx-delta, My-delta
    x1MinMaxNum = [ (-0.5)*Mx, (+0.5)*Mx, Nx ]
    x2MinMaxNum = [ (-0.5)*My, (+0.5)*My, Ny ]
    x3MinMaxNum = [       0.0,       0.0,  1 ]
    coord2      = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    coord       = ( np.concatenate( [coord1,coord2], axis=0 )[:,0:2] ).astype( np.int32 )
    coord       = coord + np.repeat( center[None,:], coord.shape[0], axis=0 )

    # ------------------------------------------------- #
    # --- [3] add radii                             --- #
    # ------------------------------------------------- #
    radii       = np.repeat( radius, coord.shape[0] )
    
    # ------------------------------------------------- #
    # --- [4] generate hit or miss                  --- #
    # ------------------------------------------------- #
    dice        = np.random.rand( coord.shape[0] )
    dice        = np.where( dice < hitrate, 1, 0 )

    # ------------------------------------------------- #
    # --- [5] concatenate array                     --- #
    # ------------------------------------------------- #
    coord       = np.concatenate( [coord,radii[:,None],dice[:,None]], axis=1 )
    
    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/holeData.dat"
    spf.save__pointFile( outFile=outFile, Data=coord )
    print( np.sum( coord[:,2] ) / coord.shape[0] )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__holeData()
