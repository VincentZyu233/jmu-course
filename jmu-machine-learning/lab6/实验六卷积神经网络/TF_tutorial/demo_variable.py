#coding:utf-8
import tensorflow as tf

a = tf.Variable([1, 1])
b = tf.Variable([2, 2])

assign_op = a.assign(b)   # a的值用b替换

init = tf.global_variables_initializer()  # 初始化所有变量的算子
with tf.Session() as sess:
    sess.run(init)   # 执行初始化，此时变量被填值
    print(sess.run(a))   # [1, 1]
    sess.run(assign_op)  # 执行assign
    print(sess.run(a))   # [2, 2]




