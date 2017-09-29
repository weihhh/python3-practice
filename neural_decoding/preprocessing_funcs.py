import numpy as np

def bin_spikes(spike_times,dt,wdw_start,wdw_end):
    '''
    将mat格式数据放进 神经元个数x时间窗个数 的矩阵中
    parameters
    ----------
    spike_times:array of arrays,
        第一层数组是神经元，第二层是那个神经元所有的放电次数
    dt: number,时间窗长度
    wdw_start: 时间起点，从此点开始将峰电位放进时间窗
    wdw_end: 同理
    
    returns
    -----------
    neural_data: 时间窗个数x神经元个数

    '''
    edges=np.arange(wdw_start,wdw_end,dt)#得到各个时间窗的边界
    num_bins=edges.shape[0]-1#时间窗个数
    num_neurons=spike_times.shape[0]#神经元个数
    neural_data=np.empty([num_bins,num_neurons])
    #计数时间窗内峰电位个数
    for i in range(num_neurons):
        neural_data[:,i]=np.histogram(spike_times[i],edges)[0]#spike_times存放的是发放时间
    return neural_data

def bin_output(outputs,output_times,dt,wdw_start,wdw_end,downsample_factor=1):
    '''
    将输出放进时间窗


    参数：
    outputs:
        记录的输出时间点的数量x输出特征个数
        其中存放的是特征的值
    output_times:
        记录的输出时间点的数量
        其中存放的是输出时间
    dt:
        时间窗宽度
    wdw_start: number (any format)
        the start time for binning the outputs
    wdw_end: number (any format)
        the end time for binning the outputs
    downsample_factor: integer, optional, default=1
        how much to downsample the outputs prior to binning
        larger values will increase speed, but decrease precision
    Returns
    -------
    outputs_binned: matrix of size "number of time bins" x "number of features in the output"
        the average value of each output feature in every time bin
    '''

    #对于一个样值序列间隔几个样值取样一次，下采样
    if downsample_factor!=1: #Don't downsample if downsample_factor=1
        downsample_idxs=np.arange(0,output_times.shape[0],downsample_factor) #Get the idxs of values we are going to include after downsampling
        outputs=outputs[downsample_idxs,:] #Get the downsampled outputs
        output_times=output_times[downsample_idxs] #Get the downsampled output times
    #函数主体，将数据放进时间窗
    edges=np.arange(wdw_start,wdw_end,dt)#得到各个时间窗的边界
    num_bins=edges.shape[0]-1#时间窗个数
    output_dim=outputs.shape[1]#输出特征个数
    outputs_binned=np.empty([num_bins,output_dim])
    #得到时间窗内平均输出
    for i in range(num_bins):
        idxs=np.where((np.squeeze(output_times)>edges[i]) &(np.squeeze(output_times)<edges[i+1]))[0]#峰电位仅需要统计个数，这里需要计算具体值，所以不能用histogram
        for j in range(output_dim):
            outputs_binned[i,j]=np.mean(outputs[idxs,j])
    return outputs_binned

def get_spikes_with_history(neural_data,bins_before,bins_after,bins_current):
    '''
    生成三维矩阵，原来的一个时间窗对应多个时间窗数据

    参数：
    ----------
    neural_data: a matrix of size "number of time bins" x "number of neurons"
        the number of spikes in each time bin for each neuron
    bins_before: integer
        How many bins of neural data prior to the output are used for decoding
    bins_after: integer
        How many bins of neural data after the output are used for decoding
    bins_current: 0 or 1, optional, default=1
        Whether to use the concurrent time bin of neural data for decoding
    Returns
    -------
    X: a matrix of size "number of total time bins" x "number of surrounding time bins used for prediction" x "number of neurons"
        For every time bin, there are the firing rates of all neurons from the specified number of time bins before (and after) 

    '''

    num_exalmples=neural_data.shape[0]#时间窗个数
    num_neurons=neural_data.shape[1]#神经元个数
    surrounding_bins=bins_before+bins_after+bins_current
    X=np.empty([num_exalmples,surrounding_bins,num_neurons])
    X[:] = np.NaN#开头和结尾的时间窗没有before和after，所以用nan区分，否则0不好区分
    #Loop through each time bin, and collect the spikes occurring in surrounding time bins
    #Note that the first "bins_before" and last "bins_after" rows of X will remain filled with NaNs, since they don't get filled in below.
    #This is because, for example, we cannot collect 10 time bins of spikes before time bin 8
    start_idx=0
    for i in range(num_examples-bins_before-bins_after): #The first bins_before and last bins_after bins don't get filled in     
        end_idx=start_idx+surrounding_bins; #The bins of neural data we will be including are between start_idx and end_idx (which will have length "surrounding_bins")
        X[i+bins_before,:,:]=neural_data[start_idx:end_idx,:] #Put neural data from surrounding bins in X, starting at row "bins_before"
        start_idx=start_idx+1;
    return X