# Tensorflow 入门与实战

- 开发环境
    - Python+tensorflow
    - Jdk+eclipse+pydev
- Tensorflow入门
- 卷积神经网络

## 1.1 tensorflow安装

### Windows：
- 安装python 2或python 3，建议安装python3
> 下载地址：https://www.python.org/downloads/windows/
- GPU版本需安装cuda和cudnn
- 通过pip安装tensorflow：
    - Cpu版本：执行pip install tensorflow==1.2.1  指定版本
    - Gpu版本：执行pip install tensorflow-gpu
    - Whl安装：pip install tensorflow-1.12.0-cp35-cp35m-win_amd64.whl

### Linux：
顺序一样，大同小异

### whl下载：
https://pypi.org/project/tensorflow/#files

### Python常见库：
- Numpy+mkl
- scikit-learn
- matplotlib

### GPU版本对应的Cuda和Cudnn版本：
https://blog.csdn.net/yuejisuo1948/article/details/81043962

## 2. Tensorflow入门

### Tensorflow优势：
- 平台支持性良好，Windows, Linux, macOS等，IOS和Android；
- 提供简单且灵活的Python API接口，内部使用C++进行优化；
- 丰富的算子，可以很容易搭建各种深度学习模型，如CNN和RNN模型；
- 提供可视化工具TensorBoard，这个是TF独有的优势；
- 支持CPU和GPU，支持分布式多机多卡训练；

### 2.1 张量
张量（Tensor）
向量：一维
矩阵：二维
张量：任意维度

张量=shape+数据类型+名字

```python
# tf.ones(shape, dtype=tf.float32, name=None)
b = tf.ones([2, 3], tf.int32) # [[1, 1, 1], [1, 1, 1]]
```

#### 几种常见创建张量的方法：
```python
a = tf.constant([1, 1, 1]) # 定义一个costant张量
b = tf.zeros([2, 3], tf.int32) # [[0, 0, 0], [0, 0, 0]]
c = tf.ones([2, 3], tf.int32) # [[1, 1, 1], [1, 1, 1]]
d = tf.random_normal([5, 5], mean=0.0, stddev=1.0) # 均值为0，标准差为1的高斯分布 
e = tf.random_uniform([5, 5], minval=0, maxval=1) # [0, 1]内的均匀分布
f = tf.placeholder(tf.int32, [3,]) # 定义一个占位张量
```

#### 变量
- 变量是有状态的张量，就是存储的实际值是可以被改变的
- 主要使用两个类：tf.Variable类和tf.train.Saver类
- 变量必须要先被初始化(initialize)，而且可以在训练时和训练后保存(save)到磁盘中。之后可以再恢复(restore)保存的变量值来训练和测试模型

```python
# 变量的声明
a = tf.Variable([[2, 3], [1, 2]])   # 初始值为[[2, 3], [1, 2]]
b = tf.Variable((tf.zeros([10, 10])))  # 初始值为全0，shape为[10,10]的张量
# 初始化
init = tf.global_variables_initializer() # 初始化所有变量的算子
with tf.Session() as sess:
    sess.run(init)   # 执行初始化，此时变量被填值
# 赋值
assign_op = a.assign(b) # a的值用b替换
sess.run(assign_op)
```

#### 计算图（flow）
由一系列节点（nodes）组成的图模型，每个节点对应的是TF的一个算子（operation），每个算子会有输入与输出，并且输入和输出都是张量

```python
a = tf.constant(5)       b = tf.constant(3)
c = tf.multiply(a, b)    d = tf.add(a, b)
e = tf.add(c, d)
```

### 2.3 实例1
```python
#demo_tensor.py
#声明两个张量
m1 = tf.constant([[2, 2]])
m2 = tf.constant([[3], [3]])
#打印张量
print(m1," ",m2.shape)

#声明一个矩阵乘法算子
dot_operation = tf.matmul(m1, m2)
print("result:",dot_operation)  # 没有结果

#方法1：开始会话
sess = tf.Session()
result = sess.run(dot_operation)
print(result)
sess.close()
```

### 2.3 实例3
```python
#demo_placehold.py
#coding:utf-8
import tensorflow as tf
# 定义一个占位张量
a = tf.placeholder(tf.int32, [3,])
# 定义一个costant张量
b = tf.constant([1, 1, 1])

# 计算a+b
c = a + b

with tf.Session() as sess:
    # 给占位张量送入数据，并执行计算图
    print(sess.run(c, feed_dict={a: [1, 2, 3]})) # [2, 3, 4]

# 输出：[2 3 4]
```
