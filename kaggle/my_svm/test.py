import numpy as np

a=np.mat(np.arange(6).reshape((3, 2)))
b=np.array([1,3,4,5])
print(b[None,1])
print(a)
print(a.reshape(2,-1))
# print(type(a[1,:]))
# b=np.mat([[1],[2],[3]]).T
# print(b)
# print(b*a)
# a=[[1],[2],[3]]
# a=np.array(a)
# print(a[2:])
# print(a)
# b=np.mat([[1,2,3]])
# alphas = np.mat([[1],[2],[3]])
# print(alphas)
# print(np.multiply(alphas,alphas).T.shape)
# print(type(np.multiply(alphas,alphas)))
# print(np.multiply(alphas,alphas).T*a)
# r=np.array([1,2,4])
# print(r.shape)