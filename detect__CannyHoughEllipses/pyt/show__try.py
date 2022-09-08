import os, sys
import numpy as np
import cv2

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/res.dat"
    Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    print( Data.shape )
    Data[  ]

    inpFile    = "jpg/match_45deg.jpg"
    image      = cv2.imread( inpFile )
    image      = image[ 210:285, 360:520,:]
    
    import nkOpenCV.put__ellipses as ell
    image     = ell.put__ellipses( image, xc=Data[:,1], yc=Data[:,2], \
                                 a1=Data[:,3], a2=Data[:,4], angle=Data[:,5] )
    cv2.imwrite( "jpg/output.jpg", image )
