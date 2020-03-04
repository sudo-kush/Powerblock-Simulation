# -*- coding: utf-8 -*-
"""
optimize cycle for thermal efficiency
"""

import power

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from sklearn import linear_model

"""
area = [2600, 3000, 3200, 3600, 4000]
data = { 'area':        pd.Series(area),
         'bedrooms':    pd.Series([3.0, 4.0, 3.0, 3.0, 5.0]),
         'age':         pd.Series([20, 15, 18, 30, 8]),
         'price':       pd.Series([550000, 565000, 610000, 595000, 760000])}
df = pd.DataFrame(data)
reg = linear_model.LinearRegression()
reg.fit(df[['area','bedrooms','age']], df.price)
"""




PR_HP = np.zeros(9) # pressure ratio of the high pressure turbine
PR_IP = np.zeros(9) # pressure ratio of the intermediate pressure turbine
PR_LP = np.zeros(9) # pressure ratio of the low pressure turbine
load = np.zeros(9)
nth = np.zeros(9)
Power = np.zeros(9)

pE_ALL = np.zeros(9)
pE_A = 5 / 100      # percentExtracted at A
pE_B = 5 / 100      # percentExtracted at B
pE_C = 5 / 100      # percentExtracted at C
pE_D = 5 / 100      # percentExtracted at D
pE_E = 5 / 100      # percentExtracted at E
pE_F = 5 / 100      # percentExtracted at F


for i in range(len(PR_HP)):
    #PR_HP[i] = 1.0 - 0.1*(i+1)
    #PR_IP[i] = 1.0 - 0.1*(i+1)
    #PR_LP[i] = 1.0 - 0.1*(i+1)
    PR_HP[i] = 7/19
    PR_IP[i] = 1/7
    PR_LP[i] = .1/1
    pE_ALL[i] = 0.01*(i+1) + 0.01 
    #pE_ALL[i] = 0.01 
    #load[i] = (1.0-0.6)/(len(PR_HP)-1)*i + 0.6
    nth[i], Power[i] = power.Cycle(1.0,PR_HP[i],PR_IP[i],PR_LP[i],pE_ALL[0],pE_ALL[0],pE_ALL[0],pE_ALL[0],pE_ALL[0],pE_ALL[i])
    
d = {'PR_HP': pd.Series(PR_HP),
     'PR_IP': pd.Series(PR_IP),
     'PR_LP': pd.Series(PR_LP),
     'pE_ALL': pd.Series(pE_ALL),
     'Power': pd.Series(Power),
     'nth':   pd.Series(nth)}
df = pd.DataFrame(d)

plt.plot(pE_ALL, nth)


reg = linear_model.LinearRegression()
reg.fit(df[['PR_HP','PR_IP','PR_LP','pE_ALL','Power']],df.nth)




















