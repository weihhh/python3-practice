import csv
import numpy as np
from numpy import *
import operator
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV#用于调参
from sklearn import preprocessing
import time

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
    
    print('data loaded! ')
    print('labelshape: ',label.shape)#(42000,)
    print('datashape: ',data.shape)#(42000, 784)

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

def makeclassify(dataset,labels):
    # clf=svm.SVC(gamma=0.001, C=100) #1
    tuned_parameters=[{'kernel': ['rbf'], 'gamma': [0.001,0.01,0.1],
                     'C': [1,10,20,30,50,100]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    # tuned_parameters=[{'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    clf=GridSearchCV(svm.SVC(),tuned_parameters,cv=4,verbose=5)#verbose日志冗余程度，默认0不输出
    clf.fit(dataset,labels)
    print(clf.best_params_, clf.best_score_)
    return clf

def predict(clf,inx):
    return clf.predict(inx)

def main():
    time1=time.time()
    trainData,trainLabel=loadtraindata()  
    testData=loadtestdata()
    trainData=preprocessing.scale(trainData)

    m,n=np.shape(testData) 
    print('finish load and trans!: ',time.time()-time1)
    x=time.time()
    clf=makeclassify(trainData,trainLabel) 
    print('training time: ',time.time()-x)
    joblib.dump(clf, 'clr.pkl')
    # clf = joblib.load('clr.pkl') 
    with open('result.csv','w') as myFile:
        myWriter=csv.writer(myFile,lineterminator='\n')#要加上linetermanator关键词，否则会产生额外空行，默认值是 '\r\n'
        myWriter.writerow(["ImageId","Label"])
        x=0
        index=0
        for i in range(m):  
            classifierResult = predict(clf,[testData[i]])[0]#提示要输入2维数据，但给了一维，加上reshape(1,-1)就行了？为什么？见notebook，搜索predict函数
    
            percent = 1.0 * i / m * 100  
            print('finish one!: ',classifierResult,'complete percent:%10.8s%s'%(str(percent),'%'),end='\r')
            
            index=index+1
            myWriter.writerow([index,classifierResult]) 
            
            if x!=10:
                x+=1
            else:
                myFile.flush()
                x=0

main()