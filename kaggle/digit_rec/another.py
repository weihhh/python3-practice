from numpy import * 
import numpy as np 
import operator  
import csv,logging,time  
import logging.config  
  
def loadTrainData():  
    ''''' 
    Load the train data from train.csv,and split label and data. 
    '''  
    I = []  
    with open('train.csv') as file:  
        lines = csv.reader(file)  
        for line in lines:  
            I.append(line) #42001*785  
    I.remove(I[0]) # Remove the describe row  
    I = array(I)   # Array the train data  
    label = I[:,0] #42000*1,Get the label column  
    data = I[:,1:] #42000*784, Get the data block  
    return normalizing(toInt(data)),toInt(label)  
  
def loadTestData():  
    ''''' 
    Load the test data from test.csv,and cut the description. 
    '''  
    I = []  
    with open('test.csv') as file:  
        lines = csv.reader(file)  
        for line in lines:  
            I.append(line) #28001*784  
    I.remove(I[0]) #remove description  
    array_I = array(I) #28000*784  
    return normalizing(toInt(array_I))  
  


def toInt(array):
    array=array.astype(np.int32)
    return array
# def toInt(array):
#     #csv读取的是string，转换为int
#     array=np.mat(array)
#     m,n=np.shape(array)
#     newarray=np.zeros((m,n),dtype=np.int8)
#     for i in range(m):
#         for j in range(n):
#             newarray[i][j]=int(array[i,j])
#     return newarray

def normalizing(array):
    #灰度图像相当于彩色图，我们转换为黑白图,归一化
    array=np.where(array！=0,1,0)
    return array


'''
def toInt(array):  
    array=mat(array)     
    rows,lines = shape(array)  
    newArray = zeros((rows,lines))  
    for i in range(rows):  
        for j in range(lines):  
            newArray[i,j] = int(array[i,j])  
    return newArray  
  
def normalizing(array):  
    rows,lines = shape(array)  
    for i in range(rows):  
        for j in range(lines):  
            if array[i,j]!=0:  
                array[i,j]=1  
    return array  
'''

def classify(inx,dataset,labels,k):
    #inx为输入的单个样本，也就是待测试的特征向量，dataset为训练样本，对应上面的trainDATA,labels对应上面的trainlabel
    dataset=np.mat(dataset)
    datasetsize=dataset.shape[0]
    labels = mat(labels)  
    diffmat=np.tile(inx,(datasetsize,1))-dataset#tile创建了datasize*1的数组，每一行都相同，都是测试特征向量，减去dataset即可求出这个测试样本和所有训练样本的各个特征的差
    sqdiffmat=np.array(diffmat)**2#只有array才能平方
    print('shape: ',sqdiffmat.shape)
    sqdistances=sqdiffmat.sum(axis=1)#axis为1表示沿着横轴
    print('size22: ',sqdistances.shape)
    distances=sqdistances**0.5
    #print('distance: ',distances[:15])
    sorteddistindice=distances.argsort()#A=array.argsort()  A[0]表示排序后 排在第一个的那个数在原来数组中的下标,默认从小到大
    classcount={}
    for i in range(k):
        #依次得到排名前k 的数据,距离最小的k个
        votelabel = labels[0,sorteddistindice[i]]#因labels已经是mat格式，虽然只有一行，但还是需要选取0行
        classcount[votelabel]=classcount.get(votelabel,0)+1
    sortedclasscount=sorted(classcount.items(),key=lambda d:d[1],reverse=True)#operator.itemgetter(1)返回一个函数，这个函数会返回index为1的元素
    print(sortedclasscount)
    return sortedclasscount[0][0]
'''
def classify(inX,dataSet,labels,k):  
    inX = mat(inX)  
    dataSet = mat(dataSet)  
    labels = mat(labels)  
    dataSetSize = dataSet.shape[0]  
    diffMat = tile(inX,(dataSetSize,1)) - dataSet # Make a diff between train data and test data  
    sqDiffMat = array(diffMat)**2  # Make square for diffMat  
    sqDistance = sqDiffMat.sum(axis=1) # Sum by row  
    distance = sqDistance**0.5  
    sortedDistIndecies = distance.argsort()  
    classCount={}  
    for i in range(k):  
        votellabel = labels[0,sortedDistIndecies[i]]  
        classCount[votellabel] = classCount.get(votellabel,0)+1  
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)  
    return sortedClassCount[0][0]
'''


def saveResult(result):  
    ''''' 
    Write the result to the result file. 
    '''  
    with open('result.csv','wb') as myFile:  
        myWriter = csv.writer(myFile)  
        for i in result:  
            tmp=[]  
            tmp.append(i)  
            myWriter.writerow(tmp)  

def handwritingClassTest():  
    # start_time = time.time()  
    # logger = logging.getLogger('example01')  
    # logging.config.fileConfig('log.conf')  
  
    # loadTrainDataTime_start = time.time()  
    traintData,traintLabel = loadTrainData()  
    # loadTrainDataTime_end = time.time()  
    # logger.info('Traint data load successful! And load-time is:'+str(loadTrainDataTime_end-loadTrainDataTime_start))  
      
    # loadTestDataTime_start = time.time()  
    testData = loadTestData()  
    # loadTestDataTime_end = time.time()  
    # logger.info('Test data load successful! And load-time is:'+str(loadTestDataTime_end-loadTestDataTime_start))  
    m,n = shape(testData)  
    resultList = []  
    # logger.info('Digit distinguish start!')  
    for i in range(m):  
        classifierResult = classify(testData[i],traintData,traintLabel,5)  
        resultList.append(classifierResult)  
        print(classifierResult)
        # if (i+1)%1000==0:  
            # logger.info(str(i+1)+'lines data were deal succeessful.')  
    # saveResult(resultList)  
      
    # lost_time = (time.time() - start_time)/60  
    # logger.info('The process is succeessful! Time:'+str(lost_time))

handwritingClassTest()