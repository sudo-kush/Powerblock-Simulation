# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:32:50 2020

@author: Remy
"""

# -*- coding: utf-8 -*-  
"""
implement components into full cycle
"""
#import matplotlib.pyplot as plt
#import numpy as np
import components
from iapws import IAPWS97 as steam

class state():
    T = 0.0 # inlet temperature (K)
    P = 0.0 # inlet pressure (MPa)
    m = 0.0 # mass flow rate (kg/s)
    h = 0.0 # specific enthalpy (kJ/kg)
    s = 0.0 # specific entropy (kJ/kgK)
    
def PRINT(M):
    print("T = ", M.T)
    print("P = ", M.P)
    print("m = ", M.m)
    print("h = ", M.h)
    print("s = ", M.s)
    print()

load = 0.6

M1 = state()
M1.T = 585 + 273
M1.P = 19
M1.m = 10
M1.h = steam(T=M1.T, P=M1.P).h
M1.s = steam(T=M1.T, P=M1.P).s

M2 = state()
A = state()

PR_HP = 10 / M1.P
PowerHP = components.Turbine(M1, M2, A, None, None, PR_HP, load)

M3 = state()
Qin_reheat = components.Reheat(M2, M3, 585+273)

M4 = state()
B = state()
C = state()

PR_IP = 3 / M3.P
PowerIP = components.Turbine(M3, M4, B, C, None, PR_IP, load)

M5 = state()
D = state()
E = state()
F = state()

PR_LP = 0.5 / M4.P
PowerLP = components.Turbine(M4, M5, D, E, F, PR_LP, load)



A2 = state()
B2 = state()
C2 = state()
D2 = state()
E2 = state()
F2 = state()

components.FW_extracted(None,A,A2)
components.FW_extracted(A2,B,B2)
#components.FW_extracted(B2,C,C2)
components.FW_extracted(None,D,D2)
components.FW_extracted(D2,E,E2)
components.FW_extracted(E2,F,F2)

M6 = state()

Qout = components.Condenser(F2, M5, M6)

M7 = state()
M7.P = C.P

PowerPump1 = components.Pump(M6, M7, 0.85)

M8 = state()
M9 = state()
M10 = state()
M10.m = M9.m = M8.m = M7.m

components.FW_main(E2,F,F2,M7,M8)
components.FW_main(D2,E,E2,M8,M9)
components.FW_main(None,D,D2,M9,M10)

M11 = state()
M11.P = M10.P
#components.FW_main(B2,C,C2,M10,M11)
components.Deaerator(B2,C,M10,M11)

M12 = state()
M12.P = M1.P
PowerPump2 = components.Pump(M11, M12, 0.85)

M14 = state()
M13 = state()
M13.m=M14.m = M12.m
components.FW_main(A2,B,B2,M12,M13)
components.FW_main(None,A,A2,M13,M14)

Qin_main = components.SteamGenerator(M14, M1)

nth = (PowerHP+PowerIP+PowerLP-PowerPump1-PowerPump2)/(Qin_reheat + Qin_main)

nc = 1 - M6.T / M1.T

TotalPower = (PowerLP+PowerIP+PowerHP-PowerPump1-PowerPump2)/1000 





