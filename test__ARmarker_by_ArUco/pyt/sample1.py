import cv2
import numpy as np

# ------------------------------------------------- #
# --- [1] generate ARmarker                     --- #
# ------------------------------------------------- #

aruco  = cv2.aruco
p_dict = aruco.getPredefinedDictionary( aruco.DICT_4X4_50 )
marker =  [0] * 4 # 初期化
for i in range(len(marker)):
    marker[i] = aruco.drawMarker(p_dict, i, 75) # 75x75 px
    cv2.imwrite(f'png/marker{i}.png', marker[i])

    
