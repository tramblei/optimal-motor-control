# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:51:09 2018

@author: Ian
"""

import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from collections import namedtuple

memory = namedtuple('Memory',['state','action','reward','next_state'])

class Qnetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        tf.reset_default_graph()

        self.X = tf.placeholder(tf.float32, shape=[None,input_dim], name="X")
        self.y = tf.placeholder(tf.float32, shape=[None,output_dim], name="y")
        
        self.a1 = tf.layers.dense(self.X, hidden_dim, activation=tf.nn.relu)
        self.a2 = tf.layers.dense(self.a1, hidden_dim, activation=tf.nn.relu)
        self.yhat = tf.layers.dense(self.a2, output_dim) # default activation is linear
        
#        w_h0 = tf.get_variable("w_h0", shape=[input_dim, hidden_dim], initializer=tf.contrib.layers.xavier_initializer())
#        b_h0= tf.get_variable("b_h0", shape = [hidden_dim], initializer=tf.constant_initializer(0.))
#        a_h0 = tf.nn.relu(tf.matmul(self.X, w_h0) + b_h0)
#        
#        w_h1 = tf.get_variable("w_h1", shape=[hidden_dim, hidden_dim], initializer=tf.contrib.layers.xavier_initializer())
#        b_h1= tf.get_variable("b_h1", shape = [hidden_dim], initializer=tf.constant_initializer(0.))
#        a_h1 = tf.nn.relu(tf.matmul(a_h0, w_h1) + b_h1)
#        
#        w_h2 = tf.get_variable("w_h2", shape=[hidden_dim, hidden_dim], initializer=tf.contrib.layers.xavier_initializer())
#        b_h2= tf.get_variable("b_h2", shape = [hidden_dim], initializer=tf.constant_initializer(0.))
#        a_h2 = tf.nn.relu(tf.matmul(a_h1, w_h2) + b_h2)    
#        w_out = tf.get_variable("w_out", shape=[hidden_dim, output_dim], initializer=tf.random_normal_initializer(stddev=.1))
        
        self.loss = tf.nn.l2_loss(self.yhat - self.y)
        self.train_op = tf.train.AdamOptimizer().minimize(self.loss)
        
        self.sess = tf.Session()
        init = tf.global_variables_initializer()
        self.sess.run(init)
    
    def predict(self, X):
        return self.sess.run(self.yhat, feed_dict={self.X: X})

    def validation(self, validX, validy):
        self.validX = validX
        self.validy = validy
        
    def update(self, X, y):
        self.sess.run(self.train_op, feed_dict={self.X: X, self.y: y})
    
    def mse(self):
        return self.sess.run(tf.nn.l2_loss(self.yhat - self.validy), feed_dict={self.X: self.validX})
    
class replay_buffer:
    def __init__(self, buff_size):
        self.max_buff_size = 80
        self.curr_buff_size = 0
        self.buff = [0] * self.max_buff_size
    def insert(self, memory):
        self.buff[self.curr_buff_size % self.max_buff_size] = memory
        self.curr_buff_size += 1