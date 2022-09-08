import numpy as np


# ========================================================= #
# ===  set__holeFile.py                                 === #
# ========================================================= #

def set__holeFile():


    outFile = "hole_univ.dat"

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 2.54, 2.54*15, 15 ]
    x2MinMaxNum = [ 2.54, 2.54*25, 25 ]
    x3MinMaxNum = [  0.0,     0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    zeros       = np.zeros( (coord.shape[0],) )
    Data = np.concatenate( [coord,zeros[:,None]], axis=1 )
    
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=Data )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    set__holeFile()
    
