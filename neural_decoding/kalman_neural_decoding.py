#Import standard packages
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from scipy import io
from scipy import stats
import pickle

#Import metrics
from metrics import get_R2
from metrics import get_rho

#Import decoder functions
from decoders import KalmanFilterDecoder

#获得原始数据
data_folder=''#存储数据的路径
with open(data_folder+'example_data_s1.pickle','rb') as f:
    neural_data,vels_binned=pickle.load(f)

#处理原始数据

lag=0 #What time bin of spikes should be used relative to the output
#(lag=-1 means use the spikes 1 bin before the output)相当于可以人工调整滞后
X_kf=neural_data

#格式化输出数据
'''
对于卡尔曼滤波，我们使用位置，速度，加速度作为输出
最终，我们只关注速度的拟合准确度（对于这个数据集）
但是把它们全部最为相关数据可以提高性能

'''
#决定位置
pos_binned=np.zeros(vels_binned.shape) #Initialize 
pos_binned[0,:]=0 #Assume starting position is at [0,0]
#基于速度确定每个时间窗对应位置，速度乘以时间
for i in range(pos_binned.shape[0]-1): 
    pos_binned[i+1,0]=pos_binned[i,0]+vels_binned[i,0]*.05 #Note that .05 is the length of the time bin
    pos_binned[i+1,1]=pos_binned[i,1]+vels_binned[i,1]*.05
#确定加速度？？
temp=np.diff(vels_binned,axis=0) #一维时间窗，二维两个元素，x，y方向速度
acc_binned=np.concatenate((temp,temp[-1:,:]),axis=0) #假设了最后一个时间窗的加速度和倒数第二个相同，这里就是将最后一行的数据复制一份拼接到尾部

#最后的输出协变量,将各种特征拼接在一起，时间窗个数x3个特征（2，2，2）
y_kf=np.concatenate((pos_binned,vels_binned,acc_binned),axis=1)

num_examples=X_kf.shape[0]#时间窗个数

#Re-align data to take lag into account处理人工设置的滞后
if lag<0:
    y_kf=y_kf[-lag:,:]
    X_kf=X_kf[0:num_examples+lag,:]
if lag>0:
    y_kf=y_kf[0:num_examples-lag,:]
    X_kf=X_kf[lag:num_examples,:]

#决定training/testing/validation sets的分配比例
training_range=[0, 0.7]
testing_range=[0.7, 0.85]
valid_range=[0.85,1]

#考虑人工设置滞后的时间窗个数
num_examples_kf=X_kf.shape[0]

#决定数据集的实际坐标范围
#Note that each range has a buffer of 1 bin at the beginning and end
#This makes it so that the different sets don't include overlapping data
training_set=np.arange(np.int(np.round(training_range[0]*num_examples_kf))+1,np.int(np.round(training_range[1]*num_examples_kf))-1)
testing_set=np.arange(np.int(np.round(testing_range[0]*num_examples_kf))+1,np.int(np.round(testing_range[1]*num_examples_kf))-1)
valid_set=np.arange(np.int(np.round(valid_range[0]*num_examples_kf))+1,np.int(np.round(valid_range[1]*num_examples_kf))-1)
#？？？少了好几个数据？比如第一个?也许是为了排除相关性干扰

#Get training data
X_kf_train=X_kf[training_set,:]
y_kf_train=y_kf[training_set,:]

#Get testing data
X_kf_test=X_kf[testing_set,:]
y_kf_test=y_kf[testing_set,:]

#Get validation data
X_kf_valid=X_kf[valid_set,:]
y_kf_valid=y_kf[valid_set,:]


#归一化
#Z-score inputs 
X_kf_train_mean=np.nanmean(X_kf_train,axis=0)
X_kf_train_std=np.nanstd(X_kf_train,axis=0)
X_kf_train=(X_kf_train-X_kf_train_mean)/X_kf_train_std
X_kf_test=(X_kf_test-X_kf_train_mean)/X_kf_train_std
X_kf_valid=(X_kf_valid-X_kf_train_mean)/X_kf_train_std

#Zero-center outputs
y_kf_train_mean=np.mean(y_kf_train,axis=0)
y_kf_train=y_kf_train-y_kf_train_mean
y_kf_test=y_kf_test-y_kf_train_mean
y_kf_valid=y_kf_valid-y_kf_train_mean


#Declare model
model_kf=KalmanFilterDecoder(C=1) #There is one optional parameter that is set to the default in this example (see ReadMe)

#Fit model
model_kf.fit(X_kf_train,y_kf_train)

#Get predictions
y_valid_predicted_kf=model_kf.predict(X_kf_valid,y_kf_valid)

#Get metrics of fit (see read me for more details on the differences between metrics)
#First I'll get the R^2
R2_kf=get_R2(y_kf_valid,y_valid_predicted_kf)
print('R2:',R2_kf[2:4]) #I'm just printing the R^2's of the 3rd and 4th entries that correspond to the velocities
#Next I'll get the rho^2 (the pearson correlation squared)
rho_kf=get_rho(y_kf_valid,y_valid_predicted_kf)
print('rho2:',rho_kf[2:4]**2) #I'm just printing the rho^2's of the 3rd and 4th entries that correspond to the velocities


#As an example, I plot an example 1000 values of the x velocity (column index 2), both true and predicted with the Kalman filter
#Note that I add back in the mean value, so that both true and predicted values are in the original coordinates
fig_x_kf=plt.figure()
plt.plot(y_kf_valid[1000:2000,2]+y_kf_train_mean[2],'b')
plt.plot(y_valid_predicted_kf[1000:2000,2]+y_kf_train_mean[2],'r')
plt.show()
#Save figure
# fig_x_kf.savefig('x_velocity_decoding.eps')