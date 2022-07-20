import numpy as np
import cv2

aruco  = cv2.aruco
p_dict = aruco.getPredefinedDictionary( aruco.DICT_4X4_50 )
    
img_bgr = cv2.imread("png/printed_ARmarker_with_coin3.jpg")
img_gry = cv2.cvtColor ( img_bgr, cv2.COLOR_BGR2GRAY )
# img_gry = cv2.threshold   ( img_gry, 90,255, cv2.THRESH_BINARY )[1]
# img_gry = cv2.medianBlur  ( img_gry, 3 )
# img_gry = cv2.GaussianBlur( img_gry, (3,3), 0 )

corners, ids, rejectedImgPoints = aruco.detectMarkers( img_gry, p_dict ) # 検出
img_marked = aruco.drawDetectedMarkers( img_bgr.copy(), corners, ids )   # 検出結果をオーバーレイ

print( ids )
print( corners[0] )
print( rejectedImgPoints[0] )

outFile = "png/out.png"
cv2.imwrite( outFile, img_marked ) # 表示
