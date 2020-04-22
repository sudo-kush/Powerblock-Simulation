# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:38:49 2020

@author: Remy
"""

from storage import storage  
import power
import numpy as np 
import matplotlib.pyplot as plt 

temp_low = 575 + 273 #K
temp_high = 600 + 273 #K

a = storage()
massflow = a.massflow_salt()*-1
hot_temp = a.hot_temp()
cold_temp = a.cold_temp()

IHX_massflow = 2400

specifich_salt = 1520/1000 #KJ/kg

temp_grad = np.linspace(temp_low-273, temp_high-273, 15)
enthalpy_salt = np.linspace(temp_low*specifich_salt, temp_high*specifich_salt, 15)

Q_sg = np.zeros(15)
new_h = np.zeros(15)

new_m = massflow + IHX_massflow 

for i in range(len(new_h)):
    new_h[i] = (IHX_massflow*enthalpy_salt[-1] + massflow*enthalpy_salt[i])/(new_m)
    Q_sg[i] = new_m*(new_h[i] - (cold_temp)*specifich_salt)/1000


steam_massflow = 500 
load = np.linspace(0.9,0.95,40)
tolerance = 5.0
real_load = np.zeros(15) 

for j in range(len(new_h)):
    for k in range(len(load)):
        if (abs(power.CycleQ(steam_massflow,load[k])-Q_sg[j])<tolerance):
            real_load[j] = load[k] 
            
Power = np.zeros(15)
nth = np.zeros(15)
temp = 0

for a in range(len(Power)):
    nth[a], Power[a], temp = power.Cycle(real_load[a],steam_massflow)
    nth[a] = round(nth[a]*100,2)
    Power[a] = round(Power[a],2)
    
fig1 = plt.figure()
plt.plot(temp_grad, nth)
plt.xlabel('TES Exit Temperature (K)')
plt.ylabel('Thermal Efficiency %')

fig2 = plt.figure()
plt.plot(temp_grad, Power)
plt.xlabel('TES Exit Temperature (K)')
plt.ylabel('Power Output (MWe)')

plt.show(fig1)
plt.show(fig2)


