# -*- coding: utf-8 -*-
"""
optimize cycle for thermal efficiency
"""

import power

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from sklearn import linear_model



PR_HP = np.zeros(9) # pressure ratio of the high pressure turbine
PR_IP = np.zeros(9) # pressure ratio of the intermediate pressure turbine
PR_LP = np.zeros(9) # pressure ratio of the low pressure turbine
load = np.zeros(9)
nth = np.zeros(9)
Power = np.zeros(9)

pE_ALL = np.zeros(9)
pE_A = 5 / 100      # percentExtracted at A
pE_B = 5 / 100      # percentExtracted at B
pE_C = 5 / 100    # percentExtracted at C
pE_D = 5 / 100    # percentExtracted at D
pE_E = 5 / 100     # percentExtracted at E
pE_F = 5 / 100    # percentExtracted at F

highPressure = 19
intPressure = 7
lowPressure = 1
condPressure = 0.1


for i in range(len(PR_HP)):
    k = 5/100 
    #PR_HP[i] = 1.0 - 0.1*(i+1)
    #PR_IP[i] = 1.0 - 0.1*(i+1)
    #PR_LP[i] = 1.0 - 0.1*(i+1)
    PR_HP[i] = intPressure/highPressure
    PR_IP[i] = lowPressure/intPressure
    PR_LP[i] = condPressure/lowPressure
    pE_ALL[i] = 0.01*(i+1) + 0.01 
    #pE_ALL[i] = 0.01 
    load[i] = (1.0-0.6)/(len(PR_HP)-1)*i + 0.6
    nth[i], Power[i] = power.Cycle(load[i],PR_HP[i],PR_IP[i],PR_LP[i],pE_ALL[i],pE_ALL[i],pE_ALL[0],pE_ALL[0],pE_ALL[0],pE_ALL[0])
    
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





















