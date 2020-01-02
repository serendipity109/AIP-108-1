#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np 

gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1024x640')


def Input(): 
    global PILFile, ggg
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP','ppm'}:
        PILFile = Image.open(filename).convert('F')
        width, height = PILFile.size
        lb.config(text = "讀入 "+ str(width) + "X" + str(height) + " " + t2 + " 檔")
        PILFile = PILFile.resize((512, 512), Image.ANTIALIAS)       
        create_img(PILFile)
        ggg = np.asarray(PILFile).astype('int64')
    else:
        lb.config(text = "不支援的檔案格式")
            

def create_img(PILFile):
    global pilfile, qq
    pilfile = ImageTk.PhotoImage(PILFile)
    qq.configure(image = pilfile)    
    
###wavelet transform
def wavelet(ggg, iteration):
    global temp, tat, TAT 
    temp = []
    a = conv(ggg, iteration)
    a.reverse()
    for i in range(iteration):
        tt = np.concatenate((a.pop(0), a.pop(0)),axis=1)
        tat = np.concatenate((a.pop(0), a.pop(0)),axis=1)
        t = np.concatenate((tt, tat),axis=0)
        a.insert(0, t)
    WT = a[0]
    tat = Image.fromarray(WT)
    TAT = ImageTk.PhotoImage(tat)
    qaq.configure(image = TAT)

def conv(image, iteration):
    global temp, pop
    filters = ([1,-1,1,-1], [1,1,-1,-1], [1,-1,1,-1], [1,1,1,1])
    # 右下左下右上左上
    for i in filters:
        w,x,y,z = i[0], i[1], i[2], i[3]
    # Height and width of output image
        Hout = int(image.shape[0]/2)
        Wout = int(image.shape[1]/2)
        output = np.zeros(shape = (Hout, Wout))
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                a = w*image[int(i*2), int(j*2)] + x*image[int(i*2), int(j*2 + 1)]
                b = y*image[int(i*2 + 1), int(j*2)] + z*image[int(i*2 + 1), int(j*2 + 1)]
                c = a+b
                output[i, j] = c/4
        temp.append(normalization(output)) #加在結尾
    if iteration == 1:
        return temp
    elif iteration > 1:
        tp = temp.pop(len(temp)-1) #最後一個拔掉
        return conv(tp, (iteration-1))
def normalization(tt):
    global tat, TAT
    tem = np.zeros(shape = tt.shape)
    for i in range(tt.shape[0]):
        for j in range(tt.shape[1]):
            if tt[i,j] < 0:
                pass
            else:
                tem[i,j] = 256*(tt[i,j]- 0)/(np.max(tt) - 0)
    return tem
###

def save(img):
    filename = asksaveasfilename(title = "Select file",filetypes = ([("PNG", "*.png"),("JPEG", "*.jpg"),("BMP", "*.BMP"),("PPM", "*.ppm"),("All files", "*")]), defaultextension = "*.*")
    print(filename)
    if filename:
        img.save(filename)
        
frame1 = tk.Frame(gui, width= 450, height= 580)
qq = tk.Label(frame1)
qq.pack()
frame2 = tk.Frame(gui, width= 450, height = 580)
qaq = tk.Label(frame2)
qaq.pack()
frame1.place(x = 0, y = 50)
frame2.place(x = 500, y = 50)

e = tk.Entry(gui)
e.place(x = 170, y = 0) 
def insert_point():
    global num
    num = 0
    if e.get():
        if int(e.get()) <= 0:
            qaq.configure(image = pilfile)
        elif int(e.get()) > 9:
            num = 9
        else:
            num = int(e.get())
        if num != 0:
            wavelet(ggg, num)
    
b1 = tk.Button(gui,text="小波轉換做幾圈",width=20,height=1,command=insert_point)
b1.place(x = 174, y = 23) 

lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 450, y = 20)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
#btn2 = tk.Button(gui, text = "儲存檔案", command = lambda: save(tat), font = 80, height = 3, width = 8)
#btn2.place(x = 82, y = 0) 
l1 = tk.Label(gui, text = '輸入影像', width = 10,height = 3, font = 30).place(x = 180, y = 600)
l2 = tk.Label(gui, text = '輸出影像', width = 10,height = 3, font = 30).place(x = 720, y = 600)

gui.mainloop()


# In[ ]:




