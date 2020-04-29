# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:38:49 2020

@author: Remy
"""

from storage import storage  
import power
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

# -----------------------------------------------------------------------------
#Set up Testing Conditions 

temp_low = 575 + 273 #K
temp_high = 600 + 273 #K
# -----------------------------------------------------------------------------
#Get values from storage

a = storage()
massflow = a.massflow_salt()*-1
hot_temp = a.hot_temp()
cold_temp = a.cold_temp()
# -----------------------------------------------------------------------------
#Initialize Intermediate Heat Exchanger Massflow 

IHX_massflow = 2400
# -----------------------------------------------------------------------------
#Specific Heat for Salt 

specifich_salt = 1520/1000 #KJ/kg
# -----------------------------------------------------------------------------
#Set up arrays for the Temperature Diff & Salt Enthalpy Gradient 

temp_grad = np.linspace(temp_low-273, temp_high-273, 15)
enthalpy_salt = np.linspace(temp_low*specifich_salt, temp_high*specifich_salt, 15)
# -----------------------------------------------------------------------------
#Set up arrays for Q into Steam Generator and Combined Enthalpys 

Q_sg = np.zeros(15)
new_h = np.zeros(15)
# -----------------------------------------------------------------------------
#Mass Balance 

new_m = massflow + IHX_massflow 
# -----------------------------------------------------------------------------
#Mass Balance with enthalpies 

for i in range(len(new_h)):
    new_h[i] = (IHX_massflow*enthalpy_salt[-1] + massflow*enthalpy_salt[i])/(new_m)
    Q_sg[i] = new_m*(new_h[i] - (cold_temp)*specifich_salt)/1000

# -----------------------------------------------------------------------------
#Set up Inital Design Conditions for Graphing 

steam_massflow = 450 
load = np.linspace(0.91,0.96,100)
tolerance = 1.0
real_load = np.zeros(15) 
# -----------------------------------------------------------------------------
#Run throught iter to find actual load 

for j in range(len(new_h)):
    for k in range(len(load)):
        if (abs(power.CycleQ(steam_massflow,load[k])-Q_sg[j])<tolerance):
            real_load[j] = load[k] 
# -----------------------------------------------------------------------------            
#Initialize arrays for Power and Efficiencies 

Power = np.zeros(15)
nth = np.zeros(15)
temp = 0
# -----------------------------------------------------------------------------
#Iterate through Power Cycle 

for a in range(len(Power)):
    nth[a], Power[a], temp = power.Cycle(real_load[a],steam_massflow)
    nth[a] = nth[a]*100 
# -----------------------------------------------------------------------------   
#Plot TES Exit Temperature vs. Thermal Efficiency     
sns.set_color_codes("pastel")
fig1 = plt.figure()
plt.plot(temp_grad, nth)
plt.xlabel('TES Exit Temperature (C)')
plt.ylabel('Thermal Efficiency %')
plt.title('Powerplant Performance')
# -----------------------------------------------------------------------------
#Plot TES Exit Temperature vs. Power Output 

fig2 = plt.figure()
plt.plot(temp_grad, Power)
plt.xlabel('TES Exit Temperature (C)')
plt.ylabel('Power Output (MWe)')
plt.title('Powerplant Performance') 
# -----------------------------------------------------------------------------
#Print plots to console 

plt.show(fig1)
plt.show(fig2)


