# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:47:15 2020

@author: Remy
"""
import numpy as np 
import matplotlib.pyplot as plt 
import math 
import power 

#375,225
'''
July Energy Grid Demand for a 300MWe 
'''
massflow = 272.2 #kg/s
tolerence = 5.0
grid = 20

x0 = np.linspace(0,24,grid)
x1 = np.linspace(0,2*math.pi,grid)
x2 = np.linspace(.6,1,grid)
y0 = np.zeros(grid)
y1 = np.zeros(grid)

for i in range(len(y0)):
    y0[i] = -75*math.sin(x1[i]) + 300 
      
#plt.plot(x0,y0)

for j in range(len(y0)):
    for k in range(len(y0)):
        if (abs((power.CycleP(x2[k],massflow)/1000 - y0[j]) < tolerence)):
            y1[j] = x2[k] 
            
            
plt.plot(x0,y1)           
            
            
    
 
    

        