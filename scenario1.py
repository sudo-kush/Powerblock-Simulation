# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:11:17 2020

@author: Remy
"""


import numpy as np
import power
import matplotlib.pyplot as plt 
import seaborn as sns 

# -----------------------------------------------------------------------------
#Things to keep in mind 
'''
3 Hour Fill -> max 370 MWth Storage 
6 Hour Fill -> max 275 MWth Storage 
9 Hour Fill -> max 200 MWth Storage 
12 Hour Fill -> max 173 MWth Storage 
'''
# -----------------------------------------------------------------------------
#Initializing variables 

fast = 250                                  #MW  Most Storage Can Take 
reactor = 1000                              #MW 
massflow = 450                              #kg/s of steam 
grid = 15                                   #amount of grid points 

x0 = np.linspace(0,100,grid)                
y0 = np.linspace(1,fast,grid)               #setting up X 
eff = np.zeros(len(x0))                     #initializing efficiency array
P = np.zeros(len(x0))                       #intitializing power array
Q = np.zeros(len(x0))                       #initializing heat array
Php = np.zeros(len(x0))

# -----------------------------------------------------------------------------
#Run through scenarios 

for i in range(len(x0)):
    eff[i], P[i], Q[i] = power.Cycle(1-y0[i]/reactor, massflow)
    eff[i] = eff[i]*100
    Php[i] = power.CycleHP(1-y0[i]/reactor, massflow)
# -----------------------------------------------------------------------------
#Plotting Efficiency vs. Energy Stored 

fig1 = plt.figure()
plt.plot(y0, eff) 
plt.xlabel('Amount of Energy put in Storage (MW)')
plt.ylabel('Steam Plant Efficiency %')
plt.title('Plant Performance')
plt.ylim(39,43)
# -----------------------------------------------------------------------------
#Plotting Power vs. Energy Stored 

f, ax = plt.subplots(figsize=(6, 6))
sns.set_color_codes("pastel")
sns.barplot(y0, P, label="Total Power", color="b")

bars = ('0','','74','','148','','222','','296','')
sns.set_color_codes("muted")
sns.barplot(y0, Php, label="High Pressure Turbine", color="b")
ax.legend(ncol=1, loc="lower right", frameon=True)
ax.set(title="Plant Performance", ylabel=('Power Output (MWe)'),
        xlabel=('Amount of Energy going to Storage'))
# -----------------------------------------------------------------------------
#Show figures to console 

plt.show(fig1)
