import csv
import numpy as np
from numpy import *
import operator
import matplotlib.pyplot as plt, matplotlib.image as mpimg


def loadtraindata():
    l=[]
    with open('train.csv') as file:
        lines=csv.reader(file)#可迭代对象，每次返回每一行的逗号分隔的数值的string列表
        # print(type(lines))
        for line in lines:
            l.append(line)
            # print(line) 
    l.remove(l[0]) #删除第一行的说明
    l=np.array(l)
    label=l[:,0]#取第一列，标签列,指示图像中的真是数字
    data=l[:,1:]
    print(label.shape)#(42000,)
    print(data.shape)#(42000, 784)
    print('ok')
    #print(label[:123])
    return normalizing(toInt(data)),toInt(label)

def loadtestdata():
    l=[]
    with open('test.csv') as file:
        lines=csv.reader(file)#可迭代对象，每次返回每一行的逗号分隔的数值的string列表
        # print(type(lines))
        for line in lines:
            l.append(line)
            # print(line) 
    l.remove(l[0])#删除第一行的说明
    data=np.array(l)
    return normalizing(toInt(data))
    

def toInt(array):
    array=array.astype(np.int32)#这里应该是int32，之前int8，导致超过127的像素值全部变成了负数
    return array


def normalizing(array):
    #灰度图像相当于彩色图，我们转换为黑白图,归一化
    array=np.where(array != 0,1,0)
    return array

trainData,trainLabel=loadtraindata()  
testData=loadtestdata()
img=trainData[2].reshape((28,28))#数据像素是28x28
plt.imshow(img,cmap='gray')
plt.show()