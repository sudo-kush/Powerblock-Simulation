# -*- coding: utf-8 -*-
"""
optimize cycle for thermal efficiency
"""
import power
from power import Cycle 
from scipy.optimize import minimize 

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

pE_ALL = np.zeros(10)

'''
pE_A = 5 / 100      # percentExtracted at A
pE_B = 5 / 100      # percentExtracted at B
pE_C = 5 / 100      # percentExtracted at C
pE_D = 5 / 100      # percentExtracted at D
pE_E = 5 / 100      # percentExtracted at E
pE_F = 5 / 100      # percentExtracted at F


'''
pE_ALL[0] = 1.0 
pE_ALL[1] = 7/19
pE_ALL[2] = 1/7 
pE_ALL[3] = .1
pE_ALL[4] = 5 / 100      # percentExtracted at A
pE_ALL[5] = 5 / 100      # percentExtracted at B
pE_ALL[6] = 5 / 100      # percentExtracted at C
pE_ALL[7] = 5 / 100      # percentExtracted at D
pE_ALL[8] = 5 / 100      # percentExtracted at E
pE_ALL[9] = 5 / 100      # percentExtracted at F
'''

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

#plt.plot(pE_ALL, nth)


reg = linear_model.LinearRegression()
reg.fit(df[['PR_HP','PR_IP','PR_LP','pE_ALL','Power']],df.nth)

'''

cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
        {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
        {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})


bnds = ((0.1,.99),(0.1,.99),(0.1,.99),(0.1,.99),(0.05,.20),(0.05,.20),(0.05,.20),(0.05,.20),(0.05,.20),(0.05,.20))

result = minimize(Cycle, pE_ALL, bounds=bnds)
                  
print(result)



















