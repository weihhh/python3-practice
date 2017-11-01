from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

'''
简单线性回归
'''

dir=r'D:\aa_work\mnist'
mnist=input_data.read_data_sets(dir,one_hot=True)

print('训练样本{}，标签： {}'.format(mnist.train.images.shape,mnist.train.labels.shape))
print('测试样本{}，标签： {}'.format(mnist.test.images.shape,mnist.test.labels.shape))
print('验证样本{}，标签： {}'.format(mnist.validation.images.shape,mnist.validation.labels.shape))



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


