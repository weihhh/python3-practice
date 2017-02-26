#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__="zhuxiang"

__version__=("0.0.0.0")

__purpose__=r'''Dropsophila'''

__time__=r'''Two Days'''

__date__=r'''20170207-20170208'''

#以下类用于界面
from tkinter import*
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

#以下用于数据处理
import xlrd
import xlwt


#以下类用于文件操作
import os
import sys

#------函数开始-----
global filename
global path
global file
global file1
global ext
global date

filename=None
file=None
path=None
file1=None
ext=None


#打开文件对话框并读取一个文件
def myopen():
    global filename
    global path
    global file
    global file1
    global ext
    global date
    filename=askopenfilename(defaultextension=".bmp",
        filetypes = [("xls文件",".xls"),("xlsx文件",".xlsx "),("所有文件",".*")])
    #path,file = os.path.split(filename)
    file1,ext = os.path.splitext(filename)    
        
def myexit():
    sys.exit()

def mybanben():
    showinfo(title="版本",message="第一版    version - 0.0.0.1")

def mybanquan():
    showinfo(title="版权",message="版权归制作者所有，未经同意可以复制！")

def myguanyu():
    showinfo(title="关于",message="朱想制作，品质保证")
    

def zhuanhuan():
    global filename
    global path
    global file
    global file1
    global ext
    global date
    if filename== None:
        showinfo(title="状态",message="没有选中任何文件")
    else:
        try:
            data = xlrd.open_workbook(filename)
        except Exception as e:
            showinfo(title="状态",message=str(e))
        #if e==0:        
        table = data.sheets()[0] # 打开第一张表
        nrows = table.nrows # 获取表的行数
        ncols = table.ncols# 获取表的列数
         
        #创建workbook和sheet对象
        workbook = xlwt.Workbook() #注意Workbook的开头W要大写
        sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)

        row=1
        for j in range(ncols): # 按列处理
            for i in range(nrows): #找到每一列之后,按行处理每一行的参数
                if i==0:#第一行是标题行直接打印就行了
                    pass
                else:    
                    if j%2==0:#DAY的那一列,需要根据天数来修改
                        xunhuan=table.cell(i,j+1).value
                        while xunhuan:
                        #for a in range(int(float(table.cell(i,j+1).value))):
                            sheet1.write(row,j,table.cell(i,j).value)
                            row=row+1
                            xunhuan=xunhuan-1
            sheet1.write(0,j,table.cell(0,j).value)                
            if j%2 != 0:#非DAY的那一天全部写成1即可也就是状态，我们没有丢失所以全部是1
                for i in range(row):
                    if i==0:
                        pass
                    else: 
                        sheet1.write(i,j,1)
                row=1

        #保存该excel文件,有同名文件时直接覆盖
        try:
            workbook.save(file1+'Survcur'+ext)
            showinfo(title="状态",message="保存成功!"+'\n'+"名字为原文件名+Survcur")
        except Exception as e:
            showinfo(title="状态",message=str(e)+'\n'+'\n'+'可能相同文件名的文件已经打开，请关闭之后再试试!')
           
def GUI():
    root=Tk()
    root.title('Scource to Survcur')
    root.geometry('500x300') 
    menubar=Menu(root)
    
    #以下为文件菜单内容
    
    #直接在顶级菜单menubar下开始
    filemenu=Menu(menubar)

    #以下为文件菜单下面的内容
    filemenu.add_command(label='打开',command=myopen)
    filemenu.add_command(label='退出',command=myexit)
    
    #以下为转换菜单下面的内容
    chepaimenu=Menu(menubar)
    chepaimenu.add_command(label='转换成Survcur格式',command=zhuanhuan)

    
    #以下为帮助菜单内容
    helpmenu=Menu(menubar)
    helpmenu.add_command(label='关于',command=myguanyu)
    helpmenu.add_command(label='版本',command=mybanben)
    helpmenu.add_command(label='版权',command=mybanquan)
 
    
    #以下为顶级菜单
    menubar.add_cascade(label="文件",menu=filemenu)
    menubar.add_cascade(label="转换",menu=chepaimenu)
    menubar.add_cascade(label="帮助",menu=helpmenu)   

    root['menu']=menubar
    #root.iconbitmap('D:\\100.ico')
    root.mainloop()
GUI()

