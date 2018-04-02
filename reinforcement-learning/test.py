# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 21:38:44 2018

@author: Ian
"""

import neural_net as nn
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1000) # for repro
function_to_learn = lambda x,y: y*10*np.sin(x*y)

NUM_HIDDEN_NODES = 20
NUM_EXAMPLES = 3000
TRAIN_SPLIT = .8
MINI_BATCH_SIZE = 100
NUM_EPOCHS = 300000

all_x = np.float32(
    np.random.uniform(-2*np.pi, 2*np.pi, (1, NUM_EXAMPLES))).T
np.random.shuffle(all_x)
train_size = int(NUM_EXAMPLES*TRAIN_SPLIT)
trainx = all_x[:train_size]
validx = all_x[train_size:]
trainy1 = function_to_learn(trainx,1)
trainy2 = function_to_learn(trainx,2)
trainy3 = function_to_learn(trainx,4)
validy1 = function_to_learn(validx,1)
validy2 = function_to_learn(validx,2)
validy3 = function_to_learn(validx,4)
trainy = np.concatenate((trainy1,trainy2,trainy3),axis=1)
validy = np.concatenate((validy1,validy2,validy3),axis=1)
N = train_size

Q = nn.Q(1,100,3,'f')
nn.init_vars()
Q.validation(validx, validy)

errors = []
for i in range(NUM_EPOCHS):
    rand_idxs = np.random.permutation(N)[:MINI_BATCH_SIZE]
    Q.update(trainx[rand_idxs], trainy[rand_idxs,:])
    error = Q.mse()
    errors.append(error)
    if i % 20 == 0:
    	print("Epoch: %d, MSE: %f" % (i, errors[-1]))

plt.plot(errors)
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Q-Network Validation: MSE per Epoch')
plt.show()

plt.figure(1)
valid_pred = nn.sess.run(Q.yhat, feed_dict={Q.X: validx})
plt.scatter(validx, valid_pred[:,0],label='y=1')
plt.scatter(validx, valid_pred[:,1],c='r',label='y=2')
plt.scatter(validx, valid_pred[:,2],c='g',label='y=4')
plt.xlabel(r'$x$')
plt.ylabel(r'$Q(x,y;\theta) \approx 10ysin(x*y)$')
plt.title("Q-Network Validation: Function Approximation")
plt.legend()
plt.show()
