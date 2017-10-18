from sklearn import datasets
from sklearn import svm


digits=datasets.load_digits()
'''
都是1797个，对应训练数据和标签
The data is always a 2D array, shape (n_samples, n_features),这里是8x8，64像素
'''
print(digits.data[-1:])
print(digits.target)
print(digits.data[-1:])
clf=svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1],digits.target[:-1])
resutl=clf.predict(digits.data[-1:])

