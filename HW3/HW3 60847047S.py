#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np
from random import uniform
from math import sin, cos, sqrt, log


gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1024x640')


def Input(): 
    global PILFile, p2
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP', 'bmp', 'png', 'ppm'}:
        PILFile = Image.open(filename).convert('F')
        width, height = PILFile.size
        lb.config(text = "讀入 "+ str(width) + "X" + str(height) + " " + t2 + " 檔")
        PILFile = PILFile.resize((390, 480), Image.ANTIALIAS)
        create_img(PILFile)
             
    else:
        lb.config(text = "不支援的檔案格式")
            
def create_img(PILFile):
    global pilfile, qq
    pilfile = ImageTk.PhotoImage(PILFile)
    qq.configure(image = pilfile)

def noise(sigma):
    gray = PILFile.copy()
    gary = gray.load()
    width, height = gray.size
    f = np.zeros(shape = (height, width))
    if (width % 2) == 0:
        for i in range(height):
            for j in range(0, width, 2):
                generate(sigma)
                f[i, j] = gary[j, i] + z1
                f[i, j+1] = gary[j+1, i] + z2
    else:
         for i in range(height - 1):
            for j in range(0, width - 1, 2):
                generate(sigma)
                f[i, j] = gary[j, i] + z1
                f[i, j+1] = gary[j+1, i] + z2
            generate(sigma)
            f[i, width -1] = gary[width -1, i] + z1
    for i in range(f.shape[0]):
        for j in range(f.shape[1]):
            gary[j, i] = branch(f[i, j])
    create_img(gray)
    hist(gray)
    
def branch(num):
    if num > 255:
        return 255
    elif num < 0:
        return 0
    else:
        return num
    
def generate(sigma):
    global z1, z2
    r = uniform(0, 1)
    phi = uniform(0, 1)
    z1 = sigma*cos(2*3.14*phi)*sqrt((-2)*log(r))
    z2 = sigma*sin(2*3.14*phi)*sqrt((-2)*log(r))    
    
def hist(PILFile):
    global _Image, qaq, avatar
    im_array = np.array(PILFile)
    m_array = np.ndarray.flatten(im_array)
    m_array = np.round(m_array)
    uniqueValues, occurCount = np.unique(m_array, return_counts=True)

    width = 400
    height = 400
    avatar = Image.new("RGB", (width, height), (255,255,255))
    drawAvatar = ImageDraw.Draw(avatar)

    for i, j in zip(uniqueValues, occurCount):
        j = round(j*400/max(occurCount))
        drawAvatar.rectangle([(0, i),(j, i)], fill = 'Blue')
    del drawAvatar
    avatar = avatar.rotate(90)
    _Image = ImageTk.PhotoImage(avatar)
    qaq.configure(image = _Image)

    
def save(img):
    filename = asksaveasfilename(title = "Select file",filetypes = ([("PNG", "*.png"),("JPEG", "*.jpg"),("BMP", "*.BMP"),("PPM", "*.ppm"),("All files", "*")]), defaultextension = "*.*")
    if filename:
        img.save(filename)
        
frame1 = tk.Frame(gui, width= 450, height= 580)
qq = tk.Label(frame1)
qq.pack()
frame2 = tk.Frame(gui, width= 400, height = 400)
qaq = tk.Label(frame2)
qaq.pack()
frame1.place(x = 0, y = 100)
frame2.place(x = 670, y = 180)


def print_selection(v):
    l.config(text='σ = ' + v)
    noise(s.get())

l = tk.Label(gui, bg='yellow', width=20, text='高斯雜訊')
l.place(x = 300, y = 0)
s = tk.Scale(gui, label='σ number', from_=0, to=50, orient=tk.HORIZONTAL,
showvalue=0, tickinterval=10, resolution=1, length=300, command=print_selection)
s.place(x = 300, y = 30)

lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 450, y = 600)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
btn2 = tk.Button(gui, text = "儲存直方圖", command = lambda : save(avatar), font = 80, height = 3, width = 10)
btn2.place(x = 82, y = 0) 
l1 = tk.Label(gui, text = '輸入影像', width = 10,height = 3, font = 30).place(x = 180, y = 600)
l2 = tk.Label(gui, text = '輸出影像', width = 10,height = 3, font = 30).place(x = 780, y = 600)
'''
btn3 = tk.Button(gui, text = "做直方圖", command = lambda : hist(PILFile), font = 80, height = 3, width = 8)
btn3.place(x = 82, y = 0)
'''

gui.mainloop()


# In[ ]:




