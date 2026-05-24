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