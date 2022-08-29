import cv2
import os, sys
import numpy             as np
import matplotlib.pyplot as plt

img          = cv2.imread("jpg/sample_original_0000.jpg")
rows,cols,ch = img.shape

w, h         = int(1080*0.5), int(1920*0.5)

src_pts      = [ [71,429],
                 [971,429],
                 [971,1661],
                 [0,1920 ] ]
dst_pts      = [ [0,0], 
                 [w,0], 
                 [w,h], 
                 [0,h] ]
src_pts      = np.array( src_pts, dtype=np.float32 )
dst_pts      = np.array( dst_pts, dtype=np.float32 )
print( src_pts )
print( dst_pts )

Matrix  = cv2.getPerspectiveTransform( src_pts, dst_pts )
dst     = cv2.warpPerspective( img, Matrix, (w,h) )
print( dst.shape )

cv2.imwrite( "jpg/out.jpg", dst )

