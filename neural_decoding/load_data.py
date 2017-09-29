import numpy as np
from scipy import io
import pickle
from preprocessing_funcs import bin_spikes
from preprocessing_funcs import bin_output

#loaddata
folder='C:/Users/weihh/Desktop/无人机/老师推荐论文/'#数据包路径
# folder='/Users/jig289/Dropbox/MATLAB/Projects/In_Progress/BMI/Processed_Data/' 
data=io.loadmat(folder+'s1_data_raw.mat')
spike_times=data['spike_times']#加载所有神经元的峰电位发放时间数据
vels=data['vels']#加载x，y方向速度
vel_times=data['vel_times']

#用户输入，一些可调参数
dt=0.05#seconds,时间窗口宽度
t_start=vel_times[0]#这里从试验最开始的时间开始
t_end=vel_times[-1]
downsample_factor=1

#将数据进行格式化整理
#When loading the Matlab cell "spike_times", Python puts it in a format with an extra unnecessary dimension
#First, we will put spike_times in a cleaner format: an array of arrays
spike_times=np.squeeze(spike_times)#python 加载mat数据出现冗余的维度，通过squeez函数去除
for i in range(spike_times.shape[0]):
    spike_times[i]=np.squeeze(spike_times[i])
#加上时间窗获得神经元峰电位发放数据
neural_data=bin_spikes(spike_times,dt,t_start,t_end)
#获得时间窗输出数据
vel_binned=bin_output(vels,vel_times,dt,t_start,t_end,downsample_factor)

#固话数据pickle
data_folder=''#存储数据的路径
with open(data_folder+'example_data_s1.pickle','wb') as f:
    pickle.dump([neural_data,vel_binned],f)
print('ok')





