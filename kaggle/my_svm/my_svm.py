import numpy as np
import random


def loaddataset(filename):
    datamat=[]
    lablemat=[]
    with open(filename) as f:
        for line in f.readlines():
            linearr=line.strip().split('\t')#strip消除前后空格防止最后出现空的一个数据，split获得其中空格分隔的数据
            datamat.append([float(linearr[0]), float(linearr[1])])
            lablemat.append(float(linearr[2]))
    return datamat,lablemat


def selectJrand(i,m):
    """
    随机从0到m挑选一个不等于i的数
    :param i:
    :param m:
    :return:
    """
    j=i             #排除i
    while (j==i):
        j = int(random.uniform(0,m))
    return j
 
def clipAlpha(aj,H,L):
    """
    将aj剪裁到L(ow)和H(igh)之间
    :param aj:
    :param H:
    :param L:
    :return:
    """
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):#采用了通用接口，便于拼接
    """
    简化版SMO算法
    :param dataMatIn:       X
    :param classLabels:     Y
    :param C:               惩罚参数
    :param toler:           容错率
    :param maxIter:         最大循环次数
    :return:
    """
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()#转置，列向量
    b = 0; m,n = shape(dataMatrix)  # m:=训练实例的个数；n:=每个实例的维度
    alphas = mat(zeros((m,1)))#即书本中的α向量，拉格朗日算子
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0   #alpha是否已经进行了优化
        for i in range(m):
            #   w = alpha * y * x;  f(x_i) = w^T * x_i + b
            fXi = float(multiply(alphas,labelMat).T*dataMatrix*dataMatrix[i,:].T) + b     # 预测的类别,两个列向量matrix multiply后还是matrix，matrix的*直接就是矩阵乘法，最后一个T没有作用，取出的还是一个ndarray（3，）
            Ei = fXi - float(labelMat[i])   #得到误差，如果误差太大，检查是否可能被优化
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)): #必须满足约束
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy()                # 教材中的α_1^old和α_2^old
                if (labelMat[i] != labelMat[j]):                                          # 两者所在的对角线段端点的界
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H: print "L==H"; continue
                # Eta = -(2 * K12 - K11 - K22)，且Eta非负，此处eta = -Eta则非正
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0: print "eta>=0"; continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                #如果内层循环通过以上方法选择的α_2不能使目标函数有足够的下降，那么放弃α_1
                if (abs(alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
        print "iteration number: %d" % iter
    return b,alphas

a,b=loaddataset('testset.txt')
a=np.mat(a)
print(a)