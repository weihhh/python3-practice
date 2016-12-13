#!/usr/bin/env python3
# Copyright (c) 2008-11 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import os
import sys
import tkinter


class MainWindow(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)#pack只是简单的布局

        self.principal = tkinter.DoubleVar()
        self.principal.set(1000.0)
        self.rate = tkinter.DoubleVar()
        self.rate.set(5.0)
        self.years = tkinter.IntVar()
        self.amount = tkinter.StringVar()

        principalLabel = tkinter.Label(self, text="Principal $:",
                                       anchor=tkinter.W, underline=0)#anchor表示西对齐，underline表示对第0个字符下划线
        principalScale = tkinter.Scale(self, variable=self.principal,
                command=self.updateUi, from_=100, to=10000000,#updateUI为自己定义的函数，作为scale的命令，scale的值改变，就会自动调用这个函数，from——和to设置最大最小值
                resolution=100, orient=tkinter.HORIZONTAL)
        rateLabel = tkinter.Label(self, text="Rate %:", underline=0,
                                  anchor=tkinter.W)
        rateScale = tkinter.Scale(self, variable=self.rate,
                command=self.updateUi, from_=1, to=100,
                resolution=0.25, digits=5, orient=tkinter.HORIZONTAL)#resolution为点一下框后的递增值，分辨率（步骤大小）。digits设置显示的数字个数
        yearsLabel = tkinter.Label(self, text="Years:", underline=0,
                                   anchor=tkinter.W)
        yearsScale = tkinter.Scale(self, variable=self.years,
                command=self.updateUi, from_=1, to=50,
                orient=tkinter.HORIZONTAL)
        amountLabel = tkinter.Label(self, text="Amount $",
                                    anchor=tkinter.W)
        actualAmountLabel = tkinter.Label(self,
                textvariable=self.amount, relief=tkinter.SUNKEN,#sunken relief使其可视化的 与scales匹配，增加窗口宽度
                anchor=tkinter.E)

        principalLabel.grid(row=0, column=0, padx=10, pady=10,#padx文本左右两侧的空格数
                            sticky=tkinter.W)
        principalScale.grid(row=0, column=1, padx=2, pady=2,
                            sticky=tkinter.EW)
        rateLabel.grid(row=1, column=0, padx=2, pady=2,
                       sticky=tkinter.W)
        rateScale.grid(row=1, column=1, padx=2, pady=2,
                       sticky=tkinter.EW)
        yearsLabel.grid(row=2, column=0, padx=2, pady=2,
                        sticky=tkinter.W)
        yearsScale.grid(row=2, column=1, padx=2, pady=2,
                        sticky=tkinter.EW)
        amountLabel.grid(row=3, column=0, padx=2, pady=2,
                         sticky=tkinter.W)
        actualAmountLabel.grid(row=3, column=1, padx=2, pady=2,
                               sticky=tkinter.EW)#ew使得扩展填充整个可用空间

        principalScale.focus_set()#键盘焦点锁定，即选定哪一个输入框，有一个黑框包围
        self.updateUi()#初始显示，因为一开始就是有一个默认值的
        parent.bind("<Alt-p>", lambda *ignore: principalScale.focus_set())#键盘按键绑定，按下键即执行后面的函数。没有直接绑定是因为再将函数或者方法作为事件绑定的结果进行调用时会将对其进行调用的事件作为第一个参数，所以我们忽略这个参数
        parent.bind("<Alt-r>", lambda *ignore: rateScale.focus_set())
        parent.bind("<Alt-y>", lambda *ignore: yearsScale.focus_set())
        parent.bind("<Control-q>", self.quit)
        parent.bind("<Escape>", self.quit)


    def updateUi(self, *ignore):
        amount = self.principal.get() * (
                 (1 + (self.rate.get() / 100.0)) ** self.years.get())
        self.amount.set("{0:.2f}".format(amount))


    def quit(self, event=None):
        self.parent.destroy()


application = tkinter.Tk()#所有窗口的父窗口，应用程序对象TK
path = os.path.join(os.path.dirname(__file__), "images/")
if sys.platform.startswith("win"):
    icon = path + "interest.ico"
else:
    icon = "@" + path + "interest.xbm"
application.iconbitmap(icon)#程序图标
application.title("Interest")
window = MainWindow(application)
application.protocol("WM_DELETE_WINDOW", window.quit)#规定按关闭按钮的处理方法
application.mainloop()

