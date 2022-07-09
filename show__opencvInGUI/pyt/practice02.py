import tkinter
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
root = tkinter.Tk()
 
img_bgr = cv2.imread("jpg/lena.jpg")
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGRからRGBに変換
 
fig = plt.figure()
# ax = fig.add_subplot()
# ax = img_rgb
 
plt.imshow(img_rgb)
 
Canvas = FigureCanvasTkAgg( fig, master=root )
Canvas.get_tk_widget().grid( row=0, column=0 )
root.mainloop()
