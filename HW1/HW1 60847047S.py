#!/usr/bin/env python
# coding: utf-8

# In[9]:


import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np 

gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1024x640')


def Input(): 
    global PILFile
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP','ppm'}:
        PILFile = Image.open(filename)
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
    qaq.configure(image = pilfile) 
    
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
frame1.place(x = 0, y = 100)
frame2.place(x = 670, y = 100)



lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 450, y = 50)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
btn2 = tk.Button(gui, text = "儲存檔案", command = lambda : save(PILFile), font = 80, height = 3, width = 8)
btn2.place(x = 82, y = 0) 
l1 = tk.Label(gui, text = '輸入影像', width = 10,height = 3, font = 30).place(x = 180, y = 600)
l2 = tk.Label(gui, text = '輸出影像', width = 10,height = 3, font = 30).place(x = 780, y = 600)

gui.mainloop()


# In[ ]:





# In[ ]:




