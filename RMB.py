import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import requests
import numpy as np
from PIL import Image, ImageTk



class DisplayImage:
    '''用于展示选择的图片'''
    def __init__(self, master):
        self.master = master
        master.title("GUI")
        self.image_frame = Frame(master, bd=0, height=200, width=800, bg='yellow', highlightthickness=2,
                                 highlightbackground='gray', highlightcolor='black')
        self.image_frame.pack()
        self.Text_label = Label(master, text='图像预览')
        self.Text_label.pack()
        self.Choose_image = Button(master, command=self.choose_pic, text="选择图片",
                                   width=17, default=ACTIVE, borderwidth=0)
        self.Choose_image.pack()
        
        self.Display_image = Button(master, command=self.display_image, text="显示图片",
                                    width=17, default=ACTIVE, borderwidth=0)
        self.Display_image.pack()
        
        self.Analy_image = Button(master, command=self.analy_img, text="分析图片",
                                    width=17, default=ACTIVE, borderwidth=0)
        self.Analy_image.pack()
        global flag
        flag = StringVar()
        flag.set('0元')
        self.filenames = []
        self.pic_filelist = []
        self.imgt_list = []
        self.image_labellist = []
        #显示结果模块
        self.out = Label(master,textvariable = flag)
        self.out.pack()
        
        
    
    def analy_img(self, event=None):
        if self.filenames:
            for k in range(len(self.filenames)):
                password='8907'
                url = "http://www.iinside.cn:7001/api_req"
                filePath= self.filenames[k]#传入图片
                data={
                'password':password,
                'reqmode':'ocr_pp'
                }
                files=[('image_ocr_pp',('wx.PNG',open(filePath,'rb'),'application/octet-stream'))]
                headers = {}
                response = requests.post( url, headers=headers, data=data, files=files)
        txt = response.text
        #计算每一个币有几张
        yi = txt.count("壹圆")
        wu = txt.count("伍圆")
        shi = txt.count("拾圆")
        ershi = txt.count("贰拾圆")
        wushi = txt.count("伍拾圆")
        yibai = txt.count("壹佰圆")
        tshi = shi-ershi-wushi #十元与二十、五十均带有十，用tshi代表真正的十个数
        num = yi+wu+tshi+ershi+wushi+yibai #计算纸币张数
        num = str(num)
        bizhi= yi*1+wu*5+tshi*10+ershi*20+wushi*50+yibai*100 #计算总的币值
        bizhi = str(bizhi)
        over = ("共有纸币"+num+"张,共"+bizhi+"元")
        global flag
        flag.set(over)
   
    def display_image(self, event=None):
        #在重新选择图片时清空原先列表
        self.pic_filelist.clear()
        self.imgt_list.clear()
        self.image_labellist.clear()

        #清空框架中的内容
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        #布局所选图片
        for i in range(len(self.filenames)):
            self.pic_filelist.append(Image.open(self.filenames[i]).resize((200,200)))
            self.imgt_list.append(ImageTk.PhotoImage(image=self.pic_filelist[i]))
            self.image_labellist.append(Label(self.image_frame, highlightthickness=0, borderwidth=0))
            self.image_labellist[i].configure(image=self.imgt_list[i])
            self.image_labellist[i].pack(side=LEFT, expand=True)
        #选取图片
    def choose_pic(self, event=None):
        self.filenames.clear()
        self.filenames += filedialog.askopenfilenames()

def main():
    window = tk.Tk()
    GUI = DisplayImage(window)
    window.title('人民币纸币识别')
    window.geometry('1000x600')
    window.mainloop()

if __name__ == '__main__':
    main()
