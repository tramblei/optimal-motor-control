# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:42:44 2018

@author: Ian
"""

import numpy as np

class Arm:
    _m1   = 1.4; # segment mass
    _m2   = 1.1;

    _l1   = 0.3; # segment length
    _l2   = 0.33;

    _s1   = 0.11; # segment center of mass
    _s2   = 0.16;

    _I1   = 0.025; # segment moment of inertia
    _I2   = 0.045;

    _b11  = 0.5; # joint friction
    _b22  = 0.5;  
    _b12  = 0.1; 
    _b21  = 0.1;

    _a1 = _I1 + _I2 + _m2 * _l1**2
    _a2 = _m2 * _l1 * _s2
    _a3 = _I2
    
    def inertia_mtx(self, theta):
        M = np.matrix([[self._a1 + 2 * self._a2 * np.cos(theta[1][0]), self._a3 + self._a2 * np.cos(theta[1][0])],
                       [self._a3 + self._a2 * np.cos(theta[1][0]), self._a3]])
        return M
    
    def coriolis_mtx(self, theta, theta_dot):
        C = np.matrix([[-theta_dot[1][0] * (2 * theta_dot[0][0] + theta_dot[1][0])],
                       [theta_dot[0][0]]])
        return C * self._a2 * np.sin(theta[1][0])
    
    def joint_friction_mtx(self):
        return np.matrix([[self._b11, self._b12], [self._b21, self._b22]])

    def __init__(self):
        self.B = self.joint_friction_mtx()
        
    def xdot(self, x, u):
        x_dot = np.zeros([4, 1])
        x_dot[0][0] = x[2]
        x_dot[1][0] = x[3]

        M = self.inertia_mtx(x[0:2])
        C = self.coriolis_mtx(x[0:2], x[2:])
        
        x_dot[2:] = np.array(np.linalg.inv(M) * (np.matrix(u.reshape([2,1])) - self.B * np.matrix(x[2:].reshape([2,1])) - C))
        return x_dot
        
        