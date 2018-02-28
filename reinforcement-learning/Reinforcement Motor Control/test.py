# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 21:38:44 2018

@author: Ian
"""

import neural_net as nn
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1000) # for repro
function_to_learn = lambda x: np.sin(x)

NUM_HIDDEN_NODES = 20
NUM_EXAMPLES = 1000
TRAIN_SPLIT = .8
MINI_BATCH_SIZE = 100
NUM_EPOCHS = 800

all_x = np.float32(
    np.random.uniform(-2*np.pi, 2*np.pi, (1, NUM_EXAMPLES))).T
np.random.shuffle(all_x)
train_size = int(NUM_EXAMPLES*TRAIN_SPLIT)
trainx = all_x[:train_size]
validx = all_x[train_size:]
trainy = function_to_learn(trainx)
validy = function_to_learn(validx)

Q = nn.Qnetwork(1,8,1)
Q.validation(validx, validy)

errors = []
for i in range(NUM_EPOCHS):
    for start, end in zip(range(0, len(trainx), MINI_BATCH_SIZE), range(MINI_BATCH_SIZE, len(trainx), MINI_BATCH_SIZE)):
        Q.update(trainx[start:end], trainy[start:end])
        errors.append(Q.mse())
    if i % 20 == 0:
    	print("Epoch: %d, MSE: %f" % (i, errors[-1]))

plt.plot(errors)
plt.xlabel('#epochs')
plt.ylabel('MSE')
plt.show()

plt.figure(1)
plt.scatter(validx, Q.sess.run(Q.yhat, feed_dict={Q.X: validx}))
plt.show()