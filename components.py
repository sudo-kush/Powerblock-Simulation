# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:31:44 2020

@author: Remy
"""

# -*- coding: utf-8 -*-
"""
function definitions for steam cycle components
"""
from iapws import IAPWS97 as steam


def Turbine(Mi, Me, A, B, C, PR, load):
    
    efficiency = (0.86-0.72)/(1.0-0.6)*load + 0.72
    
    # find exit properties
    ses = Mi.s # isentropic exit entropy (kJ/kg/K)
    Me.P = Mi.P * PR
    # set rest of state with steam tables 
    hes = steam(P=Me.P, s=ses).h
    Me.h = Mi.h - efficiency * (Mi.h - hes)
    Me.T = steam(h=Me.h, P=Me.P).T
    Me.s = steam(h=Me.h, P=Me.P).s
    
    numExtract = 0
    if(A):
        numExtract += 1
    if(B):
        numExtract += 1
    if(C):
        numExtract += 1

    percentExtracted = 5 / 100
    
    if(numExtract == 1):
        TH = steam(P=Mi.P,x=1).T
        TL = steam(P=Me.P,x=1).T
        TA = 1*(TH-TL)/(numExtract+1) + TL
        A.P = steam(T=TA, x=1).P
        hAs = steam(P=A.P, s=ses).h
        A.h = Mi.h - efficiency * (Mi.h - hAs)
        A.T = steam(P=A.P, h=A.h).T
        A.s = steam(P=A.P, h=A.h).s
        A.m = Mi.m * percentExtracted
        Me.m = Mi.m - A.m
    elif(numExtract == 2):
        TH = steam(P=Mi.P,x=1).T
        TL = steam(P=Me.P,x=1).T
        TA = 2*(TH-TL)/(numExtract+1) + TL
        A.P = steam(T=TA, x=1).P
        hAs = steam(P=A.P, s=ses).h
        A.h = Mi.h - efficiency * (Mi.h - hAs)
        A.T = steam(P=A.P, h=A.h).T
        A.s = steam(P=A.P, h=A.h).s
        A.m = Mi.m * percentExtracted
        TB = 1*(TH-TL)/(numExtract+1) + TL
        B.P = steam(T=TB, x=1).P
        hBs = steam(P=B.P, s=ses).h
        B.h = Mi.h - efficiency * (Mi.h - hBs)
        B.T = steam(P=B.P, h=B.h).T
        B.s = steam(P=B.P, h=B.h).s
        B.m = Mi.m * percentExtracted
        Me.m = Mi.m - A.m - B.m
    elif(numExtract == 3):
        TH = steam(P=Mi.P,x=1).T
        TL = steam(P=Me.P,x=1).T
        TA = 3*(TH-TL)/(numExtract+1) + TL
        A.P = steam(T=TA, x=1).P
        hAs = steam(P=A.P, s=ses).h
        A.h = Mi.h - efficiency * (Mi.h - hAs)
        A.T = steam(P=A.P, h=A.h).T
        A.s = steam(P=A.P, h=A.h).s
        A.m = Mi.m * percentExtracted
        TB = 2*(TH-TL)/(numExtract+1) + TL
        B.P = steam(T=TB, x=1).P
        hBs = steam(P=B.P, s=ses).h
        B.h = Mi.h - efficiency * (Mi.h - hBs)
        B.T = steam(P=B.P, h=B.h).T
        B.s = steam(P=B.P, h=B.h).s
        B.m = Mi.m * percentExtracted
        TC = 1*(TH-TL)/(numExtract+1) + TL
        C.P = steam(T=TC, x=1).P
        hCs = steam(P=C.P, s=ses).h
        C.h = Mi.h - efficiency * (Mi.h - hCs)
        C.T = steam(P=C.P, h=C.h).T
        C.s = steam(P=C.P, h=C.h).s
        C.m = Mi.m * percentExtracted
        Me.m = Mi.m - A.m - B.m - C.m
    else:
        Me.m = Mi.m
        
    Power = Me.m * (Mi.h - Me.h)
    
    return Power

def Reheat(Mi, Me, temp):
    
    Me.T = temp
    Me.P = Mi.P
    Me.m = Mi.m
    Me.h = steam(T=Me.T, P=Me.P).h
    Me.s = steam(T=Me.T, P=Me.P).s
    
    Q = Me.m * (Me.h - Mi.h)
    return Q

def FW_extracted(A2, B1, B2):
    
    if(A2):
        B2.m = B1.m + A2.m
    else:
        B2.m = B1.m
        
    B2.P = B1.P    
    B2.h = steam(P=B1.P, x=0).h 
    B2.s = steam(P=B1.P, x=0).s
    B2.T = steam(P=B1.P, x=0).T
    
def Condenser(F2, Mi, Me):
    
    if(F2):
        mMF = Me.m = Mi.m + F2.m
        hMF = (Mi.m*Mi.h + F2.m*F2.h)/mMF
    else:
        mMF = Me.m = Mi.m
        hMF = Mi.h
    
    Me.P = Mi.P
    Me.h = steam(P=Me.P, x=0).h
    Me.s = steam(P=Me.P, x=0).s
    Me.T = steam(P=Me.P, x=0).T
    
    Q = mMF*(hMF - Me.h)
    return Q
    
def Pump(Mi, Me, efficiency):
    
    Me.m = Mi.m
    ses = Mi.s
    hes = steam(s=ses, P=Me.P).h
    Me.h = (hes - Mi.h)/efficiency + Mi.h
    Me.T = steam(P=Me.P, h=Me.h).T
    Me.s = steam(P=Me.P, h=Me.h).s
    
    Power = Me.m*(Me.h - Mi.h)
    return Power
    
def FW_main(A2, B1, B2, Mi, Me):
    
    if(A2):
        mAB = B1.m + A2.m
        hAB = (A2.m*A2.h + B1.m*B1.h)/mAB
    else:
        mAB = B1.m
        hAB = B1.h
        
    Me.h = Mi.h - mAB*(B2.h - hAB)/Mi.m
    Me.P = Mi.P
    Me.T = steam(P=Me.P, h=Me.h).T
    Me.s = steam(P=Me.P, h=Me.h).s
    
def Deaerator(A2, B, Mi, Me):
    
    if(A2):
        Me.m = A2.m + B.m + Mi.m
        Me.h = (Mi.h*Mi.m + A2.h*A2.m + B.h*B.m)/Me.m
    else:
        Me.m = B.m + Mi.m
        Me.h = (Mi.h*Mi.m + B.h*B.m)/Me.m
    
    Me.T = steam(P=Me.P, x=0).T
    Me.s = steam(P=Me.P, x=0).s
    Me.h = steam(P=Me.P, x=0).h
    Me.P = Mi.P
        
def SteamGenerator(Mi, Me):
    
    if(Mi.m == Me.m):
        Q = Mi.m * (Me.h - Mi.h)
    
    return Q


    



