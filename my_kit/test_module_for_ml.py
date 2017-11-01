#test_module_for_ml

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,classification_report #模型准确率,查准率，查全率,f1_score,all

x,y=np.arange(10).reshape((5,2)),range(5)
print(x,list(y))

#训练数据和测试数据切分
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)#random_state=42 随机种子，shuffle=True 是否在切割前乱序，默认打乱
print(x_train,y_train)



