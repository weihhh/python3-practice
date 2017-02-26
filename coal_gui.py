#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.testname=''
        self.testnumber='1'
        self.filename=StringVar()
        self.up_value=IntVar()
        self.down_value=IntVar()
        self.createWidgets()
        
    def createWidgets(self):        
        
        
        self.noteLabel1 = Label(self, text='1.input your testname here !')
        self.noteLabel1.grid(row=0,sticky=W)#提示标签
        self.testnameInput = Entry(self)
        self.testnameInput.grid(row=0,column=1)#输入框
        
        self.noteLabel2 = Label(self, text='2.input your testnumber here !')
        self.noteLabel2.grid(row=1,sticky=W)#提示标签
        self.testnumberInput = Entry(self)
        self.testnumberInput.grid(row=1,column=1)#输入框
        self.confirmButton1 = Button(self, text='ok', command=self.setvar)
        self.confirmButton1.grid(row=1,column=2)#确认输入按钮
        
        
        self.noteLabel3=Label(self)
        self.noteLabel3['textvariable']=self.filename        
        self.noteLabel3.grid(row=2,sticky=W)#显示当前读取文件名
        
        self.noteLabel4=Label(self,text='3.choose up or down datapath or both')
        self.noteLabel4.grid(row=3,sticky=W)
        self.up_choose=Checkbutton(self,text='choose up ',variable=self.up_value)
        self.down_choose=Checkbutton(self,text='choose down ',variable=self.down_value)
        self.up_choose.grid(row=3,column=1)
        self.down_choose.grid(row=3,column=2)
        
        self.noteLabel5 = Label(self, text='4.input the row you want !')
        self.noteLabel5.grid(row=4,sticky=W)#提示标签
        self.start_rowInput = Entry(self)
        self.start_rowInput.grid(row=5)#输入框
        self.end_rowInput = Entry(self)
        self.end_rowInput.grid(row=5,column=1)#输入框
        self.confirmButton2 = Button(self, text='ok', command=self.setvar)
        self.confirmButton2.grid(row=5,column=2)#确认输入按钮
        self.backButton = Button(self, text='back', command=self.setvar)
        self.backButton.grid(row=6,column=0)#确认输入按钮
        self.nextButton = Button(self, text='next', command=self.setvar)
        self.nextButton.grid(row=6,column=1)#确认输入按钮
        
        
        
        
    def setvar(self):
        self.testname = self.testnameInput.get()
        self.testnumber = self.testnumberInput.get() or self.testnumber
        print(self.up_value.get())#checkbutton的值为0或1，通过绑定一个intvar到本身变量
        self.filename.set(self.testname+self.testnumber)
        

app = Application()
# 设置窗口标题:
app.master.title('coal_data_handle')
# 主消息循环:
app.mainloop()