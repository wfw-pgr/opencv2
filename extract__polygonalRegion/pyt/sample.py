import sys
import cv2
import numpy as np

inpFile = "jpg/coin__onSheet.jpg"
src_img = cv2.imread(inpFile)

# parameter
poly = [ [0,0],
         [1500,200],
         [3024,100],
         [3024,3700],
         [100,3700],
]
bb   = [0,0,3024,4032]

# working file
mask = np.zeros_like(src_img) # (y, x, c)

# # segmentation data
# sg = np.asarray(sg)
# poly_number = int(len(sg)/2)
# poly = np.zeros( (poly_number, 2) )
# for i in range(poly_number):
#   poly[i][0] = sg[(i * 2) + 0] # x
#   poly[i][1] = sg[(i * 2) + 1] # y

# generate mask
mask = cv2.fillConvexPoly( mask, np.array(poly, 'int32'), color=(255, 255, 255))

# generate src_img and mask_image
cv2.imwrite("jpg/src_img.png", src_img)
cv2.imwrite("jpg/mask.png", mask)

# masked image
masked_src_img = np.where(mask==255, src_img, mask)
cv2.imwrite("jpg/masked.png", masked_src_img)

# cropping img
bb = np.asarray(bb, 'int32')
offset_x = bb[0]
offset_y = bb[1]
length_x = bb[2]
length_y = bb[3]
cv2.imwrite("jpg/masked_crop.png", masked_src_img[offset_y : (offset_y + length_y), offset_x : (offset_x + length_x)])
