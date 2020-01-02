#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np 

gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1024x840')


def Input(): 
    global PILFile
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP','ppm'}:
        PILFile = Image.open(filename).convert('F')
        width, height = PILFile.size
        lb.config(text = "讀入 "+ str(width) + "X" + str(height) + " " + t2 + " 檔")
        PILFile= PILFile.resize((300, 300), Image.ANTIALIAS)       
        p1(PILFile)             
    else:
        lb.config(text = "不支援的檔案格式")
            

def p1(PILFile):
    global pilfile, qq
    pilfile = ImageTk.PhotoImage(PILFile)
    qq.configure(image = pilfile)
    
        
def hist(PILFile, hint):
    global im_array, uniqueValues, occurCount
    im_array = np.array(PILFile)
    m_array = np.ndarray.flatten(im_array)
    m_array = np.round(m_array)
    uniqueValues, occurCount = np.unique(m_array, return_counts=True)
    width = 300
    height = 300
    avatar = Image.new("RGB", (width, height), (255,255,255))
    drawAvatar = ImageDraw.Draw(avatar)
    for i, j in zip(uniqueValues, occurCount):
        j = round(j*400/max(occurCount))
        drawAvatar.rectangle([(0, i),(j, i)], fill = 'Blue')
    del drawAvatar
    avatar = avatar.rotate(90)
    if hint == 2:
        p2(avatar)
    elif hint == 3:
        p3(avatar)
    elif hint == 4:
        p4(avatar)
    
def p2(avatar):
    global _Image, qaq
    _Image = ImageTk.PhotoImage(avatar)
    qaq.configure(image = _Image)
    
def p3(avatar):
    global _Image1, qqq
    _Image1 = ImageTk.PhotoImage(avatar)
    qqq.configure(image = _Image1)

def p4(avatar):
    global _Image2, qqqq
    _Image2 = ImageTk.PhotoImage(avatar)
    qqqq.configure(image = _Image2)
'''    
def save(img):
    filename = asksaveasfilename(title = "Select file",filetypes = ([("PNG", "*.png"),("JPEG", "*.jpg"),("BMP", "*.BMP"),("PPM", "*.ppm"),("All files", "*")]), defaultextension = "*.*")
    print(filename)
    if filename:
        img.save(filename)
'''        
def T(intensity, Hc, uniqueValues):
    g = intensity
    t1 = Hc[np.where(uniqueValues == round(g))[0][0]] 
    t2 = Hc[0]
    t3 = Hc[-1]
    return round((t1-t2)/(t3-t2)*255)

def equal(im_array, occurCount, uniqueValues):
    global Hc
    Hc = [None] * len(occurCount)
    Hc[0] = occurCount[0]
    for i in range(1, len(occurCount), 1):
        Hc[i] = Hc[i-1] + occurCount[i]
    output = np.zeros(shape = im_array.shape)
    for i in range(im_array.shape[0]):
        for j in range(im_array.shape[1]):
            output[i, j] = T(im_array[i, j], Hc, uniqueValues)
    output1 = Image.fromarray(output)
    p2(output1)
    hist(output, 4)
        
frame1 = tk.Frame(gui, width = 300, height = 300)
qq = tk.Label(frame1)
qq.pack()
frame2 = tk.Frame(gui, width = 300, height = 300)
qaq = tk.Label(frame2)
qaq.pack()
frame1.place(x = 0, y = 50)
frame2.place(x = 670, y = 50)
frame3 = tk.Frame(gui, width = 300, height = 300)
qqq = tk.Label(frame3)
qqq.pack()
frame4 = tk.Frame(gui, width = 300, height = 300)
qqqq = tk.Label(frame4)
qqqq.pack()
frame3.place(x = 0, y = 350)
frame4.place(x = 670, y = 350)

lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 470, y = 50)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
btn2 = tk.Button(gui, text = "直方圖均化", command = lambda : equal(im_array, occurCount, uniqueValues), font = 80, height = 3, width = 10)
btn2.place(x = 140, y = 0) 
l1 = tk.Label(gui, text = '輸入影像', width = 8,height = 2, font = 10).place(x = 170, y = 660)
l2 = tk.Label(gui, text = '輸出影像', width = 8,height = 2, font = 10).place(x = 790, y = 660)
btn3 = tk.Button(gui, text = "做直方圖", command = lambda : hist(PILFile, 3), font = 80, height = 3, width = 8)
btn3.place(x = 70, y = 0)

gui.mainloop()


# In[ ]:




