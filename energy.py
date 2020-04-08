# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:47:15 2020

@author: Remy
"""
import numpy as np 
import matplotlib.pyplot as plt 
import math 
import storage 

#375,225
'''
July Energy Grid Demand for a 300MWe 
'''

x0 = np.linspace(0,24,101)
x1 = np.linspace(0,2*math.pi,101)
x2 = np.linspace(.6,1,101)
y0 = np.zeros(101)

for i in range(len(y0)):
    y0[i] = -75*math.sin(x1[i]) + 300 
    
plt.plot(x0,y0)

