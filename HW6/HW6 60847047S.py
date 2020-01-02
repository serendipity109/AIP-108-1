#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np 
from math import pi


gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1070x640')

def Input(): 
    global PILFile
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP','ppm'}:
        PILFile = Image.open(filename).convert('F')
        width, height = PILFile.size
        lb.config(text = "讀入 "+ str(width) + "X" + str(height) + " " + t2 + " 檔")
        PILFile= PILFile.resize((500, 500), Image.ANTIALIAS)       
        p1(PILFile)             
    else:
        lb.config(text = "不支援的檔案格式")
            

def p1(PILFile):
    global pilfile, qq
    pilfile = ImageTk.PhotoImage(PILFile)
    qq.configure(image = pilfile)
    
        
def p2(avatar):
    global _Image, qaq
    _Image = ImageTk.PhotoImage(avatar)
    qaq.configure(image = _Image)
    
def convolve(img, kernel):
    """Performs a naive convolution."""
    if kernel.shape[0] % 2 != 1 or kernel.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")

    img_height = img.shape[0]
    img_width = img.shape[1]
    pad_height = kernel.shape[0] // 2
    pad_width = kernel.shape[1] // 2
    # Allocate result image.
    pad = ((pad_height, pad_height), (pad_height, pad_width))
    g = np.empty(img.shape, dtype=np.float64)
    img = np.pad(img, pad, mode='constant', constant_values=0)
    # Do convolution
    for i in np.arange(pad_height, img_height+pad_height):
        for j in np.arange(pad_width, img_width+pad_width):
            roi = img[i - pad_height:i + pad_height +
                      1, j - pad_width:j + pad_width + 1]
            g[i - pad_height, j - pad_width] = (roi*kernel).sum()

    if (g.dtype == np.float64):
        kernel = kernel / 255.0
        kernel = (kernel*255).astype(np.uint8)
    else:
        g = g + abs(np.amin(g))
        g = g / np.amax(g)
        g = (g*255.0)

    return g

def xyfilter(size):
    x , y = np.mgrid[-(size-2):(size-1), -(size-2):(size-1)]
    return x, y
def gaussian_smooth(size):
    x, y = np.mgrid[-(size-2):(size-1), -(size-2):(size-1)]
    gaussian_kernel = np.multiply(1/(2*pi*(9**2)), np.exp(-(x**2+y**2)/(2*(9**2))))
    gaussian_kernel = gaussian_kernel / gaussian_kernel.sum()
    return gaussian_kernel
def edge_detection(img, size):
    img = np.array(img)
    blur = convolve(img, gaussian_smooth(size))
    x, y = xyfilter(size)
    a = convolve(blur, x)
    b = convolve(blur, y)
    c = np.sqrt(np.add(np.square(a), np.square(b)))
    c = c / c.max() * 255
    p2(Image.fromarray(c))
def smoothing(img, size):
    img = np.array(img)
    a = gaussian_smooth(size)
    b = convolve(img, a)
    p2(Image.fromarray(b))
'''     
def p3(avatar):
    global _Image1, qqq
    _Image1 = ImageTk.PhotoImage(avatar)
    qqq.configure(image = _Image1)

def p4(avatar):
    global _Image2, qqqq
    _Image2 = ImageTk.PhotoImage(avatar)
    qqqq.configure(image = _Image2)
   
def save(img):
    filename = asksaveasfilename(title = "Select file",filetypes = ([("PNG", "*.png"),("JPEG", "*.jpg"),("BMP", "*.BMP"),("PPM", "*.ppm"),("All files", "*")]), defaultextension = "*.*")
    print(filename)
    if filename:
        img.save(filename)
'''        
       
frame1 = tk.Frame(gui, width = 500, height = 500)
qq = tk.Label(frame1)
qq.pack()
frame2 = tk.Frame(gui, width = 500, height = 500)
qaq = tk.Label(frame2)
qaq.pack()
frame1.place(x = 0, y = 90)
frame2.place(x = 550, y = 90)
'''
frame3 = tk.Frame(gui, width = 300, height = 300)
qqq = tk.Label(frame3)
qqq.pack()
frame4 = tk.Frame(gui, width = 300, height = 300)
qqqq = tk.Label(frame4)
qqqq.pack()
frame3.place(x = 0, y = 350)
frame4.place(x = 670, y = 350)
'''

e = tk.Entry(gui)
e.place(x = 80, y = 40) 
eb = tk.Label(gui, text = 'Conv Size', font = 20).place(x = 140, y = 68)
def insert_point(instruction):
    global num
    num = 0
    if e.get():
        g = int(e.get())
        if (g - 1)%2 == 1:
            qaq.configure(image = pilfile)
        elif instruction == 1:
            num = g
            smoothing(PILFile, num)
        elif instruction == 0:
            num = g
            edge_detection(PILFile, num)


lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 470, y = 50)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
l1 = tk.Label(gui, text = '輸入影像', width = 8,height = 2, font = 10).place(x = 170, y = 600)
l2 = tk.Label(gui, text = '輸出影像', width = 8,height = 2, font = 10).place(x = 790, y = 600)
    
b1 = tk.Button(gui,text="邊緣偵測",width=20,height=1,command=lambda:insert_point(0))
b1.place(x = 80, y = 0) 
b2 = tk.Button(gui,text="影像平滑化",width=20,height=1,command=lambda:insert_point(1))
b2.place(x = 80, y = 20) 

gui.mainloop()

