import tkinter as tk  
from PIL import ImageTk,Image, ImageDraw
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from os.path import splitext
import numpy as np 
from math import pi
import cv2
from math import ceil

gui = tk.Tk()

gui.title('AIP 60847047S')
gui.geometry('1070x640')

def Input(): 
    global PILFile, filename
    filename = askopenfilename()
    t1 = splitext(filename)[-1]
    t2 = t1[1:]
    if t2 in {'jpg','BMP','ppm'}:
        PILFile = Image.open(filename)
        width, height = PILFile.size
        lb.config(text = "讀入 "+ str(width) + "X" + str(height) + " " + t2 + " 檔")
        PILFile = PILFile.resize((500, 500), Image.ANTIALIAS)
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
    
def fst(filename):
    #filename = number + '.jpg'
    global img, im, gray, d1, d2, Y, W
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    im = cv2.GaussianBlur(img,(7,7),0)

    low_threshold = 30
    high_threshold = 50
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    median = cv2.medianBlur(edges, 3)
    avg = cv2.blur(median, (9,9))
    candidate = np.int16(edges) - np.int16(avg)
    candidate = cv2.threshold(candidate, 240, 255, cv2.THRESH_BINARY)[1]

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    #img[dst>0.01*dst.max()]=[0,0,255]
    Y = np.array((130, 255, 255))
    Y = np.int16(Y)
    W = np.array((255, 255, 255))
    W = np.int16(W)
    dist1 = 0
    dist2 = 0
    d1 = []
    d2 = []
    using = []    # > np.percentile(dst, 50)
    x, y = np.where(dst > 9)
    for i in range(len(x)):
        if  candidate[x[i], y[i]] == 255:
            B = im[x[i], y[i], 0]
            G = im[x[i], y[i], 1]
            R = im[x[i], y[i], 2]
            color = np.array((B, G, R))
            dist1 = np.linalg.norm(Y-color)
            dist2 = np.linalg.norm(W-color)
            '''
            if x[i] > ceil(dst.shape[0]/2):
                dist1 /= 2
                dist2 /= 2      
            '''
            if (dist2 < 50) | (dist1 < 100):
                using.append((x[i], y[i]))
                d1.append(dist1)
                d2.append(dist2)

    if (len(d1) < 300) | (len(d2) < 300):
        #print('lack')
        dist1 = 0
        dist2 = 0
        d1 = []
        d2 = []
        using = []    # > np.percentile(dst, 50)
        x, y = np.where(dst > 9)
        for i in range(len(x)):
            if  candidate[x[i], y[i]] == 255:
                B = im[x[i], y[i], 0]
                G = im[x[i], y[i], 1]
                R = im[x[i], y[i], 2]
                color = np.array((B, G, R))
                dist1 = np.linalg.norm(Y-color)
                dist2 = np.linalg.norm(W-color)
                if x[i] > ceil(dst.shape[0]/2):
                    dist1 /= 2
                    dist2 /= 2     
                if (dist2 < 50) | (dist1 < 100):
                    using.append((x[i], y[i]))
                    d1.append(dist1)
                    d2.append(dist2)

    if sum(d1) > sum(d2):
        t = True
        col = d2
    else:
        t = False
        col = d1
    deleters = []
    for i in np.where(col > np.percentile(col, 30))[0]:
        deleters.append(using[i])

    #print((len(using), len(deleters)))
    for i in deleters:
        using.remove(i)    
    snd(using)

def direction(input, dir):
    global boundary, initpt, t
    t = []
    x, y = input
    if dir%2 == 0:
        dir = (dir + 7)%8
    else:
        dir = (dir + 6)%8
    while len(t) < 8:
        if dir == 0:
            if homo((x, y), (x+1, y)) == True:
                initpt = (x+1, y)
                boundary.append((x+1, y))
                break
            else:
                #print((x, y), (x+1, y))
                t.append(0)
                dir = 1
        elif dir == 1:
            if homo((x, y), (x+1, y+1)) == True:
                initpt = (x+1, y+1)
                boundary.append((x+1, y+1)) 
                break
            else:
                #print((x, y), (x+1, y+1))
                t.append(1)
                dir = 2
        elif dir == 2:
            if homo((x, y), (x, y+1)) == True:
                initpt = (x, y+1)
                boundary.append((x, y+1))  
                break
            else:
                #print((x, y), (x, y+1))
                t.append(2)
                dir = 3       
        elif dir == 3:
            if homo((x, y), (x-1, y+1)) == True:
                initpt = (x-1, y+1)
                boundary.append((x-1, y+1))   
                break
            else:
                #print((x, y), (x-1, y+1))
                t.append(3)
                dir = 4
        elif dir == 4:
            if homo((x, y), (x-1, y)) == True:
                initpt = (x-1, y)
                boundary.append((x-1, y))
                break
            else:
                #print((x, y), (x-1, y))
                t.append(4)
                dir = 5
        elif dir == 5:
            if homo((x, y), (x-1, y-1)) == True:
                initpt = (x-1, y-1)
                boundary.append((x-1, y-1))
                break
            else:
                #print((x, y), (x-1, y-1))
                t.append(5)
                dir = 6
        elif dir == 6:
            if homo((x, y), (x, y-1)) == True:
                initpt = (x, y-1)
                boundary.append((x, y-1))
                break
            else:
                #print((x, y), (x, y-1))
                t.append(6)
                dir = 7  
        elif dir == 7:
            if homo((x, y), (x+1, y-1)) == True:
                initpt = (x+1, y-1)
                boundary.append((x+1, y-1))
                break
            else:
                #print((x, y), (x+1, y-1))
                t.append(7)
                dir = 0  


def homo(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if (x2 >= (gray.shape[0]-1)) | (y2 >= (gray.shape[1]-1)) | (x2 < 0) | (y2 < 0):
        return False
    else:
        B = im[x1, y1, 0]
        G = im[x1, y1, 1]
        R = im[x1, y1, 2]
        b = im[x2, y2, 0]
        g = im[x2, y2, 1]
        r = im[x2, y2, 2]
        c1 = np.array((B, G, R))
        c2 = np.array((b, g, r))
        c1 = np.int16(c1)
        c2 = np.int16(c2)
        dist = np.sum(c2-c1)
        if sum(d1) > sum(d2):
            d = np.linalg.norm(W - im[x2, y2, :])
        else:
            d = np.linalg.norm(Y - im[x2, y2, :])
        if (dist > -30) & (d < np.percentile(col, 90)):
            return True
        else:
            return False

def snd(using):
    global col, d1, d2, boundary
    d1 = []; d2 = []
    for i in using:
        x, y = i
        B = im[x, y, 0]
        G = im[x, y, 1]
        R = im[x, y, 2]
        color = np.array((B, G, R))
        d1.append(np.linalg.norm(Y-color))
        d2.append(np.linalg.norm(W-color))

    if sum(d1) > sum(d2):
        col = d2
    else: 
        col = d1

    boundary = []
    d = 0
    t2 = using.copy()
    for i in range(len(using)): 
        initpt = using[i]
        d += 1
        tolerate = 0
        dir = 7
        while True:
            if initpt in t2:
                tolerate += 1
                if tolerate > 3:
                    break
                else:
                    direction(initpt, dir)
            else:
                t2.append(initpt)
                direction(initpt, dir)
    using = using + boundary
    using = (list(set(using)))
    trd(using)

def trd(using):
    for i in range(len(using)):
        x, y = using[i]
        cv2.circle(im, (y, x), 3, (0, 0, 255), -1)    

    median = cv2.medianBlur(im[:, :, 2], 13)

    x = np.where(median == 255)[0]
    y = np.where(median == 255)[1]

    b = im[x, y][:,0]
    g = im[x, y][:,1]
    r = im[x, y][:,2]
    Color = np.zeros(shape = im.shape)
    t = []
    for i in [b, g, r]:
        counts = np.bincount(i)
    #返回众数
        t.append(np.argmax(counts))
    Color[:,:,0] = t[0]
    Color[:,:,1] = t[1]
    Color[:,:,2] = t[2]
    a = np.int16(Color) - np.int16(im)
    x1 = []
    y1 = []
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if (np.abs(a[i, j, 0]) + np.abs(a[i, j, 1]) +np.abs(a[ i, j, 2])) < 4:
                x1.append(i)
                y1.append(j)
    x1 = np.array(x1)
    y1 = np.array(y1)
    x = np.append(x, x1)
    y = np.append(y, y1)

    for i in range(len(x)):
        cv2.circle(img, (y[i], x[i]), 1, (0, 0, 255), -1)
    dk = cv2.resize(img, (500, 500), interpolation=cv2.INTER_CUBIC)
    dk = cv2.cvtColor(dk ,cv2.COLOR_BGR2RGB)
    p2(Image.fromarray(dk))
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



lb = tk.Label(gui, text = '', font = 30)
lb.place(x = 470, y = 50)
btn1 = tk.Button(gui, text = "讀入檔案", command = Input, font = 80, height = 3, width = 8)
btn1.place(x = 0, y = 0)
l1 = tk.Label(gui, text = '輸入影像', width = 8,height = 2, font = 10).place(x = 170, y = 600)
l2 = tk.Label(gui, text = '輸出影像', width = 8,height = 2, font = 10).place(x = 790, y = 600)
    
b1 = tk.Button(gui,text="斑馬線偵測",font = 80,width=10,height=3,command=lambda:fst(filename))
b1.place(x = 80, y = 0) 
#b2 = tk.Button(gui,text="影像平滑化",width=20,height=1,command=lambda:insert_point(1))
#b2.place(x = 80, y = 20) 

gui.mainloop()