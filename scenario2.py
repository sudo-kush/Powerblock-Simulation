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

IHX_massflow = massflow * 4

specifich_salt = 1520/1000 #KJ/kgK

temp_grad = np.linspace(temp_low, temp_high, 15)
enthalpy_salt = np.linspace(temp_low*specifich_salt, temp_high*specifich_salt, 15)

Q_sg = np.zeros(15)
new_h = np.zeros(15)

new_m = massflow + IHX_massflow 

for i in range(len(new_h)):
    new_h[i] = (IHX_massflow*enthalpy_salt[-1] + massflow*enthalpy_salt[i])/(new_m)
    Q_sg[i] = new_m*(new_h[i] - (cold_temp+273)*specifich_salt)



