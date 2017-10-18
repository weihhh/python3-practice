import csv
import numpy as np
from numpy import *
import operator

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


def classify(inx,dataset,labels,k):
    #inx为输入的单个样本，也就是待测试的特征向量，dataset为训练样本，对应上面的trainDATA,labels对应上面的trainlabel
    dataset=np.mat(dataset)
    datasetsize=dataset.shape[0]

    diffmat=np.tile(inx,(datasetsize,1))-dataset#tile创建了datasize*1的数组，每一行都相同，都是测试特征向量，减去dataset即可求出这个测试样本和所有训练样本的各个特征的差
    sqdiffmat=np.array(diffmat)**2#只有array才能平方
    sqdistances=sqdiffmat.sum(axis=1)#axis为1表示沿着横轴
    distances=sqdistances**0.5
    #print('distance: ',distances[:15])
    sorteddistindice=distances.argsort()#A=array.argsort()  A[0]表示排序后 排在第一个的那个数在原来数组中的下标,默认从小到大
    classcount={}
    for i in range(k):
        #依次得到排名前k 的数据,距离最小的k个
        votelabel=labels[sorteddistindice[i]]#因labels已经是mat格式，虽然只有一行，但还是需要选取0行
        classcount[votelabel]=classcount.get(votelabel,0)+1
    sortedclasscount=sorted(classcount.items(),key=lambda d:d[1],reverse=True)#operator.itemgetter(1)返回一个函数，这个函数会返回index为1的元素
    # print(sortedclasscount)
    return sortedclasscount[0][0]




def handwritingClassTest():  
    trainData,trainLabel=loadtraindata()  
    testData=loadtestdata()  
    m,n=np.shape(testData) 
    print('finish loading!: ',m,n) 
    with open('result.csv','w') as myFile:
        myWriter=csv.writer(myFile,lineterminator='\n')#要加上linetermanator关键词，否则会产生额外空行，默认值是 '\r\n'
        myWriter.writerow(["ImageId","Label"])
        x=0
        index=0
        for i in range(m):  
            classifierResult = classify(testData[i], trainData, trainLabel,5) 
    
            percent = 1.0 * i / m * 100  
            print('finish one!: ',classifierResult,'complete percent:%10.8s%s'%(str(percent),'%'),end='\r')
            
            index=index+1
            myWriter.writerow([index,classifierResult]) 
            
            if x!=10:
                x+=1
            else:
                myFile.flush()
                x=0

handwritingClassTest() 
