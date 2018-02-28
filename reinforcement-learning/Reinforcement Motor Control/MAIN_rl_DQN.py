# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:42:44 2018

@author: Ian
"""

import arm
import utils
import numpy as np
import matplotlib.pyplot as plt
import itertools
import neural_net as nn
import random

gamma = 0.8
rand_eps = 0.7
eps_decay = 0.98
hidden_layers = 10

n = 4
m = 2

pi = np.pi
distance = pi / 4
alpha = pi / 4
initial = np.array([pi/2, pi/2])
target_theta = initial + distance * np.array([np.cos(alpha), np.sin(alpha)])
target_state = np.append(target_theta, [0, 0]).reshape([n,1])

max_episodes = 5000
max_it = 200
t = 0.5
dt = t / max_it
batch_size = 1


num_inputs = 3
input_bound = 5
single_actions = np.linspace(-input_bound, input_bound, num_inputs)
actions = []
for action in itertools.combinations_with_replacement(single_actions, m):
    actions.append(np.array(action))
num_actions = len(actions)

Q = nn.Qnetwork(n, hidden_layers, num_actions)
myarm = arm.Arm()
mean_rewards = []
success_freq = []
successes = []
for ep in range(max_episodes):
    x = np.zeros([n, max_it])
    x[:,0] = np.array([pi/2, pi/2, 0, 0])
    y = np.zeros([num_actions, max_it])
    mean_reward  = 0
    success = False
    for i in range(1, max_it - 1):
        state = x[:, i]
        qval = Q.predict(state.reshape([1, n]))
        if (random.random() < rand_eps):
            action = np.random.randint(0, num_actions)
        else:
            action = np.argmax(qval)
        u = actions[action]
        
        new_state = utils.rung_kutta4(myarm, state.reshape([n,1]), u, dt)
        x[:, i + 1] = new_state.reshape([4])
        reward = utils.reward(new_state, u, target_state)
        mean_reward += reward / max_it
        
        newQ = Q.predict(new_state.reshape([1,n]))
        maxQ = np.max(newQ)
        y[:, i + 1] = qval[:]
        
        if utils.close_enough(new_state, target_state):
            bonus = 1000
        else:
            bonus = 0
        y[action,i] = reward + gamma * maxQ + bonus
        if i != 0 and i % batch_size == 0:
            Q.update(np.transpose(x[:, i - batch_size: i]), np.transpose(y[:, i - batch_size: i]))
        
        if bonus != 0:
            success = True 
            print("Success!")
            break
        
        if rand_eps > 0.1:
            rand_eps= rand_eps * eps_decay
    if success:
        successes.append(1)
    else:
        successes.append(0)
    success_freq.append(sum(successes[-100:])/len(successes[-100:]))
    mean_rewards.append(mean_reward)
    print("Episode: %d, final position: (%f, %f), mean reward: %f, success freq: %f" % (ep, x[0,-1], x[1,-1], mean_reward, success_freq[-1]))

plt.scatter(np.arange(0, max_episodes), mean_rewards)
plt.title("Mean rewards per episode")
plt.xlabel("Episode")
plt.ylabel("Mean reward")
plt.show()

plt.plot(success_freq)
plt.title("Success frequency over last 100 episodes")
plt.xlabel("Episode")
plt.ylabel("Sucess frequency")
plt.show()