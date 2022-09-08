import numpy as np

# ========================================================= #
# ===  make__labels.py                                  === #
# ========================================================= #

def make__labels():

    inpFile     = "labels_one2.dat"
    with open( inpFile, "r" ) as f:
        one_index = np.loadtxt( f, dtype=np.int64 )
    one_index   = one_index - 1
    
    nPhoto      = 375
    labels_     = np.zeros( (nPhoto,) )
    labels_[one_index] = 1.0
    labels      = np.zeros( (nPhoto,5) )
    labels[:,4] = np.copy( labels_ )

    import nkUtilities.save__pointFile as spf
    outFile     = "labels.dat"
    spf.save__pointFile( outFile=outFile, Data=labels )
    return()



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__labels()
    
