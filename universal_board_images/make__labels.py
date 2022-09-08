import numpy as np

# ========================================================= #
# ===  make__labels.py                                  === #
# ========================================================= #

def make__labels():
    
    
    inpFile     = "labels_one.dat"
    with open( inpFile, "r" ) as f:
        one_index = np.loadtxt( f, dtype=np.int64 )
    plus_index  = one_index[ np.where( one_index > 0 ) ]
    minus_index = one_index[ np.where( one_index < 0 ) ]
    plus_index  = plus_index - 1
    minus_index = np.abs( minus_index ) - 1

    nPieces = 375
    nImages = 320
    locs    = []
    for ii in range( nImages ):
        labels               = np.zeros( (nPieces,) )
        labels[plus_index]   = + 1.0
        labels[minus_index]  = - 1.0
        index                = np.zeros( (nPieces) )
        image_num            = np.ones ( (nPieces) ) * ( ii+1 )
        piece_num            = np.arange( nPieces ) + 1
        nn                   = np.zeros( (nPieces) )
        loc                  = np.concatenate( [ index[:,None], image_num[:,None], \
                                                 piece_num[:,None], nn[:,None], \
                                                 labels[:,None] ], axis=1 )
        locs.append( loc )
    labels = np.array( locs )
    labels[:,:,0] = np.reshape( np.arange( labels.shape[0]*labels.shape[1] ) + 1, \
                                ( labels.shape[0], labels.shape[1] ) )
    # print( labels.shape )
    # sys.exit()
    
    #     index                = np.array( np.arange( 375 ), dtype=np.int64 )
    # labels[:,0]          = index + 1
    # labels[:,1]          = index // 15 + 1
    # labels[:,2]          = index - ( index // 15 ) * 15 + 1
    # labels[:,4]          = np.copy( labels_ )
    # labels               = np.reshape( labels, (1,labels.shape[0],5) )

    import nkUtilities.save__pointFile as spf
    outFile     = "labels.dat"
    names       = [ "index", "row", "col", "nn", "label" ]
    spf.save__pointFile( outFile=outFile, Data=labels )
    return()



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__labels()
    
