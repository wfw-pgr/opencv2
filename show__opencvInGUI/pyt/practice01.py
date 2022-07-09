import cv2
import tkinter as tk
from PIL import ImageTk, Image
 
img = cv2.imread('jpg/lena.jpg')
 
root = tk.Tk()
 
canvas    = tk.Canvas()
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
image_pil = Image.fromarray(image_rgb)
image_Tk  = ImageTk.PhotoImage( image_pil, master=canvas)
canvas.create_image(0,0,image=image_Tk,anchor='center')
canvas.grid()
 
root.mainloop()
