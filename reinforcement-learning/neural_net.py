# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:51:09 2018

@author: Ian
"""

import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from collections import namedtuple
import random

memory = namedtuple('Memory',['state','action','reward','next_state'])

tf.reset_default_graph()
sess = tf.Session()

class Q:
    '''
    Q(s,a) is (expected) value of taking action a from state s 
    '''
    def __init__(self, input_dim, hidden_dim, output_dim, name):

        self.X = tf.placeholder(tf.float32, shape=[None,input_dim], name="X")
        self.y = tf.placeholder(tf.float32, shape=[None,output_dim], name="y")
        
        self.a1 = tf.layers.dense(self.X, hidden_dim, activation=tf.nn.leaky_relu, name=name+'/layer1')
        self.a2 = tf.layers.dense(self.a1, hidden_dim, activation=tf.nn.leaky_relu, name=name+'/layer2')
        self.a3 = tf.layers.dense(self.a2, hidden_dim, activation=tf.nn.leaky_relu, name=name+'/layer3')
        self.yhat = tf.layers.dense(self.a3, output_dim) # default activation is linear
        
        self.loss = tf.nn.l2_loss(self.yhat - self.y)
        self.train_op = tf.train.AdamOptimizer(0.001).minimize(self.loss)
        
    def predict(self, X):
        return sess.run(self.yhat, feed_dict={self.X: X})

    def validation(self, validX, validy):
        self.validX = validX
        self.validy = validy
        
    def update(self, X, y):
        sess.run(self.train_op, feed_dict={self.X: X, self.y: y})
    
    def mse(self, X, y):
        return sess.run(self.loss, feed_dict={self.X: X, self.y: y})
    
    def target_update(self, op_holder):
        for op in op_holder:
            sess.run(op)
    
    def target_init(self):
        ops = update_target_graph(1)
        self.target_update(ops)
        
    def mse(self):
        return sess.run(self.loss, feed_dict={self.X:self.validX, self.y: self.validy})
        
                
def init_vars():
        init = tf.global_variables_initializer()
        sess.run(init)
        pass
        
def update_target_graph(tau):
    trainables = tf.trainable_variables()
    total_vars = len(trainables)
    op_holder = []
    for idx,var in enumerate(trainables[0:total_vars//2]):
        op_holder.append(trainables[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*trainables[idx+total_vars//2].value())))
    return op_holder
    
class replay_buffer:
    def __init__(self, buff_size):
        self.max_buff_size = 80
        self.curr_buff_size = 0
        self.buff = [0] * self.max_buff_size
        
    def insert(self, memory):
        self.buff[self.curr_buff_size % self.max_buff_size] = memory
        self.curr_buff_size += 1

    def sample(self, num_samples):
        minibatch = random.sample(self.buff, num_samples)
        return minibatch
