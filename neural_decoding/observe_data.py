import pickle
import numpy

#get固话数据pickle
data_folder=''#存储数据的路径
with open(data_folder+'example_data_s1.pickle','rb') as f:
    data=pickle.load(f)
# print(len(data))

#整个数据都是根据时间来排的，时间窗个数61339，输入输出时间窗对应都一样
# neural_data: 时间窗个数x神经元个数
neural_data=data[0]
#时间窗个数x特征数
outputs_binned=data[1]

# print(len(data[1]),len(data[0]))