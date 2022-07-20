import numpy as np
import cv2

aruco = cv2.aruco
p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

img_bgr = cv2.imread("png/printed_ARmarker_with_coin3.jpg")
pShape  = tuple( img_bgr.shape[0:2] )
print( pShape )
img_gry = cv2.cvtColor ( img_bgr, cv2.COLOR_BGR2GRAY )
corners, ids, rejectedImgPoints = aruco.detectMarkers(img_bgr, p_dict) # 検出

# 時計回りで左上から順にマーカーの「中心座標」を m に格納
m = np.empty((4,2))
for i,c in zip( ids.ravel(), corners ):
  m[i] = c[0].mean(axis=0)

pRatio = float(pShape[1]) / float(pShape[0])
width, height = ( 500, int(500*pRatio), ) # 変形後画像サイズ

marker_coordinates = np.float32( m )
print( marker_coordinates.shape )
print( marker_coordinates )

trans = False
if ( trans ):
    true_coordinates   = np.float32([[0,0],[width,0],[0,height],[width,height],] )
    trans_mat = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates )
    img_out   = cv2.warpPerspective( img_bgr, trans_mat, (width, height) )
else:
    img_out   = img_bgr
    
cv2.imwrite( "png/out3.png", img_out )




