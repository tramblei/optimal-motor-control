# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 11:33:36 2018

@author: Ian
"""

import arm
import math
import utils
a = arm.Arm()
a.xdot = lambda x,u: x
dt = 0.05
xs = []
xs.append(1)
for i in range(0,100):
    xs.append(utils.rung_kutta4(a, xs[-1], 0, dt))
    
