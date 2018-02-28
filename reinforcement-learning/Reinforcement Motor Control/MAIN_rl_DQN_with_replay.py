# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:23:58 2018

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
rand_eps = 0.6
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
replay = nn.replay_buffer(80)
myarm = arm.Arm()
mean_rewards = []
success_freq = []
successes = []
for ep in range(max_episodes):
    x = np.zeros([n, max_it])
    x[:,0] = np.array([pi/2, pi/2, 0, 0])
    y = np.zeros([num_actions, max_it])
    mean_reward  = 0
    success = 0
    end = -1
    for i in range(0, max_it - 1):
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

        if utils.close_enough(new_state, target_state):
            end = i + 1
            success = 1
            break
        
        if replay.curr_buff_size < replay.max_buff_size:
            replay.insert(nn.memory(state, action, reward, new_state))
        else:
            replay.insert(nn.memory(state, action, reward, new_state))
            minibatch = random.sample(replay.buff, 40)
            x_train = np.zeros([40,n])
            y_train = np.zeros([40,num_actions])
            for idx, memory in enumerate(minibatch):
                old_state, action, reward, new_state = memory
                oldq = Q.predict(old_state.reshape([1,n]))
                newq = Q.predict(new_state.reshape([1,n]))
                maxq = np.max(newq)
                ytmp = np.zeros([1,num_actions])
                ytmp[:] = oldq[:]
                if utils.close_enough(new_state, target_state):
                    bonus = 1000
                else:
                    bonus = 0
                ytmp[0,action] = reward + gamma * maxq + bonus
                x_train[idx,:] = old_state.reshape([n])
                y_train[idx,:] = ytmp.reshape([num_actions])
    
                Q.update(x_train, y_train)
        
        if rand_eps > 0.1:
            rand_eps= rand_eps * eps_decay
    if success:
        successes.append(1)
    else:
        successes.append(0)
    success_freq.append(sum(successes[-100:])/len(successes[-100:]))
    mean_rewards.append(mean_reward)
    print("Episode: %d (%d), final position: (%f, %f), mean reward: %f, success freq: %f" % (ep, success, x[0,end], x[1,end], mean_reward, success_freq[-1]))

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