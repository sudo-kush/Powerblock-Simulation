"Metric Units"

import numpy as np
import power 

nth, P, Qin = power.Cycle(1.0, 10)
"Basic Set Up"
Nt = 120                                                                         #Number of tanks in system
Od = 2.03                                                                      #Outer Diameter of tank 'm'
Wall = .026                                                                    #Wall thickness of tank 'm'
Id = Od - 2 * (Wall)                                                           #Inner Diameter of tank 'm'
A = 3.14159265 * Id**2 /4                                                      #Area of one tank end 'm2'
At = A * Nt                                                                    #Area of all tanks in system 'm2'
L = 12                                                                         #Height of tank 'm'
V = At * L                                                                     #Total volume of tanks 'm3'
Pi = np.pi

Rhos = 1804                                                                    #Density of salt 'kg/m3'
Cps = 1520

M = -231.48                                                                        #mass flow rate 'kg/s'
Mv = M/Rhos                                                                    #Volumetric flow rate 'm3/s'

Tat = 585 + 273                                                                #Top in Temp 'K'
Tab = 315 + 273                                                                #Bottom out Temp 'K'

"Thermocline Location and timing"

Thh = L * .2                                                                   #Height of the Thermocline 'm'
Thop = Thh                                                                       #Thermocline original position 'm'
t = 0                                                                          #Time elapsed 's'

if M >= 0:
    Thtc = (Tat - Tab) / Thh                                                   #Rate of change of temperature in thermocline 'K/m"
    Thv = Mv / At                                                              #Thermocline Velocity 'm/s'

    Thl = Thop - Thv * t                                                       #Location of Thermocline 'm'

    ttf = (Thl - Thh) / Thv                                                    #Time to fill 's'
    ttfh = ttf / 3600                                                          #Time to fill 'h'

    Tit = Tat                                                                  #Temp in top 'K'
    Tob = Tab                                                                  #Temp out bottom 'K'

    if Thl >= L - Thh:
        Tat = Tit - Thtc * (Thl - L) #Adjusting 
    
    if Thl <= Thh:
        Tob = Tob + Thtc * (Thh - Thl)
        
    print(ttfh,'hours until full')
    
    
if M <= 0:
    Thtc = (Tat - Tab) / Thh                                                   #Rate of change of temperature in thermocline 'K/m"
    Thv = Mv / At                                                              #Thermocline Velocity 'm/s'

    Thl = Thop - Thv * t                                                       #Location of Thermocline 'm'

    tte = (L - Thl) / -Thv                                                     #Time to empty 's'
    tteh = tte / 3600                                                          #Time to empty 'h'

    Tot = Tat                                                                  #Temp out top 'K'
    Tib = Tab                                                                  #Temp in bottom 'K'

    if Thl >= L - Thh:
        Tot = Tot - Thtc * (Thl - L)
    
    if Thl <= Thh:
        Tab = Tib + Thtc * (Thh - Thl)
        
    print(tteh,'hours until empty')
    
    
"Energy Calculations"

"Alumina"
Rhof = 3943                                                                    #Density of filler medium 'kg/m3'
Cp = 1165                                                                      #Specific heat of filler medium 'J/kgK'
Vf = .45                                                                       #Void Fraction
Cf = 700                                                                       #Cost of Filler '$/tonne'

"Steel Slag"
#Rhof = 4110
#Cp = 865
#Vf = .37
#Cf = 500

"Fire Bricks"
#Rhof = 2530
#Cp = 929
#Vf = .37
#Cf = 300

Ed = Rhof * Cp                                                                 #Energy density of filler medium 'J/m3K'
Eds = Rhos * Cps                                                               #Energy density of salt 'J/m3K'
Edsy = (Ed * (1 - Vf)) + (Eds * (Vf))                                          #Combined energy density 'J/m3K'
Edsymwh = Edsy / 3.6e9 * (Tat - Tab)                                           #Combined energy density 'MWh/m3'

Tse = Edsymwh * (V - (At * Thh))                                               #Energy stored 'MWh'

print('Total possible energy stored=',Tse,'MWh')

Vfill = At * (L - Thl)                                                         #Volume of tank currently full 'm3'

Se = Edsymwh * Vfill                                                           #Energy currently stored in tank 'MWh'

print('Energy currently in storage=',Se,'MWh')

if M <= 0:
    Qo = Cps * (Tot - Tib) * -M / 1000 / 1000
    
    print('Energy out',Qo,'MJ/s')
    
if M >= 0:
    Qi = Cps * (Tit - Tob) * M / 1000 / 1000

    print('Energy in',Qi,'MJ/s')


"Heat Transfer"

#Hexagonal tank arrangement

Aet = Pi * Od**2 /4                                                            #Area of top of one tank 'm3'
Aett = Aet * Nt / .9068996821                                                  #Area of top of hexagon 'm3'
a = np.sqrt((2 * Aett) / (3 * np.sqrt(3)))                                     #Side length of the hexagon 'm'
Aw = L * a                                                                     #Area of side wall 'm3'
Tea = Aett + (Aw * 6)

ks = 22.6                                                                      #Heat capacity of AISI 304 steel 'W/mK'
Thos = (Od - Id) / 2                                                           #Thickness of steel wall 'm'
Rdps = Thos / ks                                                               #Thermal resistance of steel tank 'm2K/W'

ki = .1226                                                                     #Heat capacity of insulation
Thoi = .0508                                                                   #Thickness of insulation 'm'
Rdpi = Thoi / ki                                                               #Thermal resistance of insulation 'm2K/W'

h = 50                                                                         #Convection Coefficient of air 'W/m2K'
Rdpa = 1 / h                                                                   #Thermal resistance of air 'm2K/W'

sigma = 5.67e-8                                                                #Sigma
eps = .9                                                                       #Epsilon
Tsurr = 298                                                                    #Tsurrounding 'K'
Tsurf = 321.12                                                                 #Tsurface 'K'

hr = sigma * eps * (Tsurf - Tsurr) * (Tsurf**2 + Tsurr**2)                     #hr radiation 'W/m2K'
Rdpr = 1 / hr                                                                  #Thermal Resistance of radiation 'm2K/W'

Rdpt = Rdps + Rdpi + ((( 1 / Rdpa) + (1 / Rdpr))**(-1))                        #Total thermal resistance 'm2K/W'

qdp = (Tat - 298) / Rdpt                                                       #Heat flux 'W/m2'

qt = qdp * Tea / 1000 / 1000                                                   #Heat transfer 'MW'


"Cost of Everything"

"Tank"
Tc = 500                                                                       #Cost of tanks per ton '$/tonen'
Rhot = 7800                                                                    #Density of steel tank 'kg/m3'
Vt = ((Od**2 * Pi / 4) - (Id**2 * Pi / 4)) * L                                 #Volume of tank material 'm3'
Mt = Vt * Rhot * Nt                                                            #Total mass of all tanks 'kg'
Ttc= Mt * Tc / 1000                                                            #Total cost of tanks '$'

"Salt"
Cs = 1100                                                                      #Cost of salt $/tonne
Ms = Rhos * (V * Vf)                                                           #Mass of salt 'kg'
Tcs = Ms * Cs / 1000                                                           #Total cost of salt '$'

"Filler"
Mf = Rhof * (V * (1 - Vf))                                                     #Mass of filler 'kg'
Tcf = Mf * Cf / 1000                                                           #Total cost of filler '$'

"Pump"
Cpp = 1200                                                                     #Cost per pump
Tpp = 10                                                                       #Tanks per pump
Tcp = Cpp * Nt / Tpp                                                           #Total cost of pumps

"Insulation"
Cpt = 1700                                                                     #Cost of insulation per tonne


"Total"
C = Ttc + Tcs + Tcf + Tcp                                                      #Total cost '$'
Cpkwh = C / Tse / 1000                                                         #Cost per KWh '$/KWh'

print('Total cost of storage $',C,)
print('Cost per KWh',Cpkwh,'$/KWh')
print('Electric Power Out: ',round(P/1000,2),'MWe')
print('Thermal Efficiency: ',round(nth*100,2),'%')
#%%

Q = 95

if M >= 0:
    Q = Q * -1

if Q >= 0:
    
    Msf = Q / Cps / (Tot - Tib) * 1000 * 1000
    
if Q <= 0:
    
    Msf = Q / Cps / (Tit - Tob) * 1000 * 1000
 
