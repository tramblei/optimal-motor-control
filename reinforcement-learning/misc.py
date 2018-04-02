# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:11:55 2018

@author: Ian
"""
import numpy as np
import arm

def rung_kutta4t(obj, x1, u, dt):
    obj = arm.Arm()
    k1 = obj.xdot(x1, u)
    k2 = obj.xdot(x1 + dt / 2 * k1, u)
    k3 = obj.xdot(x1 + dt / 2 * k2, u)
    k4 = obj.xdot(x1 + dt * k3, u)
    
    x2 = x1 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x2

def rung_kutta4(obj, x1, u, dt):
    k1 = obj.xdot(x1, u)
    k2 = obj.xdot(x1 + dt / 2 * k1, u)
    k3 = obj.xdot(x1 + dt / 2 * k2, u)
    k4 = obj.xdot(x1 + dt * k3, u)
    
    x2 = x1 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x2

def close_enough(x, target):
    ptol = 0.1
    vtol = 0.2
    
    return (np.linalg.norm(x[0:2]) < ptol) and (np.linalg.norm(x[2:]) < vtol)
    
def reward(x, u, target):
    pos_pen = 10
    vel_pen = 0.01
    u_pen = 0.001
    cost = pos_pen * np.linalg.norm(x[0:2]-target[0:2]) + vel_pen * np.linalg.norm(x[2:]-target[2:]) + u_pen * np.linalg.norm(u)
    return -cost