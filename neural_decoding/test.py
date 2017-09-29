import numpy as np

# data=np.empty([3,5])
# print(data)
# x,y=np.histogram([1,0,1,9,4],bins=[0,1,5,10])
# print(x)
# data=[[1,2,3,4,5,6]]  
# print(data)
# x=np.array([[[0], [1], [2]]])
# print(np.squeeze(data))
# result=np.where((np.squeeze(data)>3) & (np.squeeze(data)<5))[0]
# print(type(result[0]),result[0])

data1=np.arange(200).reshape(100,2)
num_examples_kf=100
print(data1)
# data2=np.concatenate((data1,data1[-1:,:]))
# print(data1,data2)
training_range=[0, 0.7]
testing_range=[0.7, 0.85]
valid_range=[0.85,1]

training_set=np.arange(np.int(np.round(training_range[0]*num_examples_kf))+1,np.int(np.round(training_range[1]*num_examples_kf))-1)
testing_set=np.arange(np.int(np.round(testing_range[0]*num_examples_kf))+1,np.int(np.round(testing_range[1]*num_examples_kf))-1)
valid_set=np.arange(np.int(np.round(valid_range[0]*num_examples_kf))+1,np.int(np.round(valid_range[1]*num_examples_kf))-1)

X_kf_train=data1[training_set,:]
X_kf_test=data1[testing_set,:]

print(X_kf_train)
print(X_kf_test)