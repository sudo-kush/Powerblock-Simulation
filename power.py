"""
full cycle as a function
"""

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

'''
PR_HP = 0.5         # pressure ratio of the high pressure turbine
PR_IP = 0.5         # pressure ratio of the intermediate pressure turbine
PR_LP = 0.5         # pressure ratio of the low pressure turbine
pE_A = 5 / 100      # percentExtracted at A
pE_B = 5 / 100      # percentExtracted at B
pE_C = 5 / 100      # percentExtracted at C
pE_D = 5 / 100      # percentExtracted at D
pE_E = 5 / 100      # percentExtracted at E
pE_F = 5 / 100      # percentExtracted at F
'''

def Cycle(load,PR_HP,PR_IP,PR_LP,pE_A,pE_B,pE_C,pE_D,pE_E,pE_F):
    
    # set inital state at the high pressure turbine inlet
    M1 = state()
    M1.T = 585 + 273
    M1.P = 19
    M1.m = 10
    M1.h = steam(T=M1.T, P=M1.P).h
    M1.s = steam(T=M1.T, P=M1.P).s
    
    # high pressure turbine states and function
    M2 = state()
    A = state()
    PowerHP = components.Turbine(M1, M2, A, None, None, pE_A, None, None, PR_HP, load)
    
    # reheat after high pressure turbine
    M3 = state()
    Qin_reheat = components.Reheat(M2, M3, 585+273)
    
    # intermediate pressure turbine states and function
    M4 = state()
    B = state()
    C = state()
    PowerIP = components.Turbine(M3, M4, B, C, None, pE_B, pE_C, None, PR_IP, load)
    
    # low pressure turbine states and function
    M5 = state()
    D = state()
    E = state()
    F = state()
    PowerLP = components.Turbine(M4, M5, D, E, F, pE_D, pE_E, pE_F, PR_LP, load)
    
    # extracted steam through closed feedwater train
    A2 = state()
    B2 = state()
    D2 = state()
    E2 = state()
    F2 = state()
    components.FW_extracted(None,A,A2)
    components.FW_extracted(A2,B,B2)
    components.FW_extracted(None,D,D2)
    components.FW_extracted(D2,E,E2)
    components.FW_extracted(E2,F,F2)
    
    # [main + extracted steam from LP] though condenser
    M6 = state()
    Qout = components.Condenser(F2, M5, M6)
    
    # first pump to reach deaerator pressure
    M7 = state()
    M7.P = C.P
    PowerPump1 = components.Pump(M6, M7, 0.85)
    
    # feedwater heaters for LP section
    M8 = state()
    M9 = state()
    M10 = state()
    M10.m = M9.m = M8.m = M7.m
    components.FW_main(E2,F,F2,M7,M8)
    components.FW_main(D2,E,E2,M8,M9)
    components.FW_main(None,D,D2,M9,M10)
    
    # deaerator combining extracted steam at C, 
    # combined feedwater from HP & IP, and main steam
    M11 = state()
    M11.P = M10.P
    components.Deaerator(B2,C,M10,M11)
    
    # pump 2 to reach high pressure for the HP turbine
    M12 = state()
    M12.P = M1.P
    PowerPump2 = components.Pump(M11, M12, 0.85)
    
    # feedwater heating from HP and IP turbines
    M14 = state()
    M13 = state()
    M13.m=M14.m = M12.m
    components.FW_main(A2,B,B2,M12,M13)
    components.FW_main(None,A,A2,M13,M14)
    
    # heat in from the steam generator
    Qin_main = components.SteamGenerator(M14, M1)
    
    # efficiency calculations
    Power = PowerHP+PowerIP+PowerLP-PowerPump1-PowerPump2
    Qin = Qin_reheat + Qin_main
    nth = Power/Qin
    nc = 1 - M6.T / M1.T
    
    return nth, Power
 








