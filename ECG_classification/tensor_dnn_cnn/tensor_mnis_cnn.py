from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

'''
卷积神经网络
'''

dir=r'D:\aa_work\mnist'
mnist=input_data.read_data_sets(dir,one_hot=True)

print('训练样本{}，标签： {}'.format(mnist.train.images.shape,mnist.train.labels.shape))
print('测试样本{}，标签： {}'.format(mnist.test.images.shape,mnist.test.labels.shape))
print('验证样本{}，标签： {}'.format(mnist.validation.images.shape,mnist.validation.labels.shape))



#权重初始化
'''
权重在初始化时应该加入少量的噪声来打破对称性以及避免0梯度,
使用的是ReLU神经元，因此比较好的做法是用一个较小的正数来初始化偏置项，以避免神经元节点输出恒为0的问题
'''
def weight_variable(shape):
    initial=tf.truncated_normal(shape,stddev=0.1)#根据stddev方差返回正太分布
    return tf.Variable(initial)

def bias_variable(shape):
    initial=tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

#卷积和池化,1步长（stride size），0边距（padding size）的模板,池化用简单传统的2x2大小的模板
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')


x=tf.placeholder('float',[None,784])#占位符，None表示此张量的第一个维度可以是任何长度的

#回归模型
W=tf.Variable(tf.zeros([784,10]))#10代表预测目标10类
b=tf.Variable(tf.zeros(10))
y=tf.nn.softmax(tf.matmul(x,W)+b)#预测结果

#训练模型，即损失函数之类的
y_=tf.placeholder('float',[None,10])#样本labels
cross_entropy=-tf.reduce_sum(y_*tf.log(y))
#学习率0.01
train_step=tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
#初始化所有变量
init=tf.initialize_all_variables()#tf.global_variables_initializer

sess=tf.Session()
sess.run(init)
for i in range(1000):
    batch_xs,batch_ys=mnist.train.next_batch(100)#随机抓取100个批处理数据点，随机梯度下降
    sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})

correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))#argmax寻找在某一维上其数据最大值所在索引值
accuracy=tf.reduce_mean(tf.cast(correct_prediction,'float'))#cast强制转换
print(sess.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))


