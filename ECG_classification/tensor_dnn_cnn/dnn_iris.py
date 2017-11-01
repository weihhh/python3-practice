import tensorflow as tf
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split#训练数据、测试数据切分


iris = datasets.load_iris()  
X = iris.data  
y = iris.target

feature_columns=[tf.contrib.layers.real_valued_column('',dimension=4)]
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.5)
print('训练集规模： {}，测试集规模： {}'.format(x_train.shape,x_test.shape))


#声明特征取值
classifier=tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,hidden_units=[10,20,10],n_classes=3,model_dir=r'D:\aa_work\model')

classifier.fit(x=x_train,y=y_train,steps=2000)

accuracy_score = classifier.evaluate(x=x_test,
                                     y=y_test)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))

# 直接创建数据来进行预测
new_samples = np.array(
    [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
y = classifier.predict(new_samples)
print('Predictions: {}'.format(list(y)))