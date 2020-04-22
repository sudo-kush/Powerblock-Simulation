# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:11:17 2020

@author: Remy
"""


import numpy as np
import power
import matplotlib.pyplot as plt 

'''
3 Hour Fill -> max 370 MWth Storage 
6 Hour Fill -> max 275 MWth Storage 
9 Hour Fill -> max 200 MWth Storage 
12 Hour Fill -> max 173 MWth Storage 
'''

fast = 370 #MW  Most Storage Can Take 
reactor = 1000 #MW 
massflow = 450 #kg/s

x0 = np.linspace(0,100,101) 
y0 = np.linspace(1,fast,101)
eff = np.zeros(len(x0))
P = np.zeros(len(x0))
Q = np.zeros(len(x0))

for i in range(len(x0)):
    eff[i], P[i], Q[i] = power.Cycle(1-y0[i]/reactor, massflow)

fig1 = plt.figure()
plt.plot(y0, eff) 
plt.xlabel('MW Extracted for Storage')
plt.ylabel('Steam Plant Effeciency')

fig2 = plt.figure() 
plt.plot(y0, P)
plt.xlabel('MW Extracted for Storage')
plt.ylabel('Power Output MWe') 

plt.show(fig1)
plt.show(fig2)