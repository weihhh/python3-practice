import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.svm import LinearSVC
from pandas import DataFrame

from plc_sample import plot_learning_curve

np.random.seed(0)#固定了随机种子,那么接下去的产生的随机值会固定！randin产生4
# print(np.random.randint(5))
#生成一些简单的玩具数据
x,y=make_classification(1000,n_features=20,n_informative=2,n_redundant=2,n_classes=2,random_state=0)#If int, random_state is the seed used by the random number generator,informative指的是提供分类信息的特征数，redundant是多余的数据
# print(type(x))#ndarray
df=DataFrame(np.hstack((x,y[:,None])),columns=[i for i in range(20)]+['class'])#np.hstack水平方向拼接，即增加列
# print(df[:5])
#利用seaborn 对数据进行可视化，便于后面的分析
pair_seaborn=sns.pairplot(df[:50],vars=[8,11,12,14,19],hue='class',size=1.5)#hue : 使用指定变量为分类变量画图,vars:data使用，否则使用data的全部列,size指定inches height
#利用热力图直观看到相关性
plt.figure(figsize=(12,10))
_=sns.heatmap(df.corr(),linewidths=0.1,vmax=1.0, square=True,linecolor='white', annot=True)
#利用训练数据直观看到训练的过程和误差
_=plot_learning_curve(LinearSVC(C=10),'svc-c10',x,y,ylim=(0.7, 1.01),cv=4,train_sizes=np.linspace(0.05,0.2, 5))#函数中已经新建了画布，train_size这里是获得了float的小数列表，表示从总数据中取百分比。若整数则代表所取样本数
# _=plot_learning_curve(LinearSVC(C=10),'svc',x[:,[11,14]],y,ylim=(0.7, 1.01),cv=4,train_sizes=np.linspace(0.05,0.2, 5))#这里手动挑选了两个信息量大的特征
# _=plot_learning_curve(Pipeline([("fs", SelectKBest(f_classif, k=2)),("svc", LinearSVC(C=10.0))]),'svc',x,y,ylim=(0.7, 1.01),cv=4,train_sizes=np.linspace(0.05,0.2, 5))#这里使用了自动挑选特征，selectbest函数的k就是最后需要找出的特征数
# _=plot_learning_curve(LinearSVC(C=0.1),'svc-0.1',x,y,ylim=(0.7, 1.01),cv=4,train_sizes=np.linspace(0.05,0.2, 5))#通过减小C,可以减少支持向量，缓解过拟合

plt.show()