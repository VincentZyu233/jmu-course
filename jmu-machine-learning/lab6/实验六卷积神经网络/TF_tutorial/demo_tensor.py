#coding:utf-8
import  tensorflow as tf

#张量
m1 = tf.constant([[2, 2]])
m2 = tf.constant([[3],
                  [3]])
print(m1," ",m2.shape)

#声明一个矩阵乘法算子
dot_operation = tf.matmul(m1, m2)

print("result:",dot_operation)  # 没有结果

#方法1：开始会话
sess = tf.Session()
result = sess.run(dot_operation)
print(result)
sess.close()


#方法2：开始会话
with tf.Session() as sess:
    result_ = sess.run(dot_operation)
    print(result_)
    