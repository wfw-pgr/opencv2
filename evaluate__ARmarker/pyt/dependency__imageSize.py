import numpy as np
import os, sys
import resample as res
import evaluate__ARmarker as eva


inpFile  = "mov/sample.mov"
orgFile  = "mov/sample_original.mov"
resizes  = np.linspace( 0.10, 0.95, 18 )
org_size = np.array( [ 1080, 1920 ] )

ans = []

for ik,resize in enumerate( resizes ):
    
    import nkOpenCV.resample__movie as res
    ret     = res.resample__movie( inpFile=orgFile, outFile=inpFile, resize=resize )
    ret     = eva.evaluate__ARmarker( inpFile=inpFile )
    ret     = np.array( ret )
    size    = np.array( org_size * resize )
    ans_    = np.concatenate( [ size, ret ] )
    ans.append( ans_ )

ans = np.array( ans )
print( ans )
    
with open( "dat/result.dat", "w" ) as f:
    np.savetxt( f, ans, fmt="%15.8e" )
