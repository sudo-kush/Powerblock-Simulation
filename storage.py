"Metric Units"
    
import numpy as np
import power 
 
    
class storage():
    
    Q = 250
        
    "Basic Set Up"
    Nt = 340                                                                       #Number of tanks in system
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
    
    Tat = 600 + 273                                                                #Top in Temp 'K'
    Tab = 315 + 273                                                                #Bottom out Temp 'K'
    
    M = 0                                                                          #mass flow rate 'kg/s'                                                                  #Power out 'MW'
    
    if Q >= 0:
        
        M = -Q / Cps / (Tat - Tab) * 1000 * 1000                                   #Mass flow salt 'kg/s'
        
    if Q <= 0:
        
        M = Q / Cps / (Tat - Tab) * 1000 * 1000                                    #Mass flow salt 'kg/s'
     
    #M = -840                                                                       #Redefining M for testing purposes  
    Mv = M/Rhos                                                                    #Volumetric flow rate 'm3/s'
    
    
    "Thermocline Location and timing"
    
    tf = .2                                                                        #Size of Thermocline via percentage of tank height
    Thh = L * tf                                                                   #Height of the Thermocline 'm'
    Thop = Thh                                                                     #Thermocline original position 'm'
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
            
        #print(round(ttfh,2),'hours until full')
        
        
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
            
        #print(round(tteh,2),'hours until empty')

    K = 12                                                                         #Thermal Conductivity of Solid     
    Vtt = V * .64                                                                  #Total volume of filler
    r = .002                                                                       #Radius of filler
    Vpb = 4/3 * 3.14159265 * r**3                                                  #Volume of 1 ball
    Sapb = 4 * 3.14159265 * r**2                                                   #Surface area of 1 ball
    Nb = Vtt / Vpb                                                                 #Number of balls
    Sat = Nb * Sapb                                                                #Total Surface area
    Saic = Sat * tf                                                                #Surface area in contact with thermocline
    U = 1/(1/13+1/K)                                                               #Overall heat transfer rate
    Qmax = Saic * U * 10 /1000/1000                                                #Max heat transfer rate of storage

    "Energy Calculations"
    
    "Alumina"
    Rhof = 3943                                                                    #Density of filler medium 'kg/m3'
    Cp = 1165                                                                      #Specific heat of filler medium 'J/kgK'
    Vf = .44                                                                       #Void Fraction
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
    
    #print('Total possible energy stored =',round(Tse,2),'MWh')
    
    Vfill = At * (L - Thl)                                                         #Volume of tank currently full 'm3'
    
    Se = Edsymwh * Vfill                                                           #Energy currently stored in tank 'MWh'
    
    #print('Energy currently in storage =',round(Se,2),'MWh')
    
    if M <= 0:
        Qo = Cps * (Tot - Tib) * -M / 1000 / 1000
        
        #print('Energy out',round(Qo,2),'MJ/s')
        
    if M >= 0:
        Qi = Cps * (Tit - Tob) * M / 1000 / 1000
    
        #print('Energy in',round(Qi,2),'MJ/s')
    
    
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
    Thoi = .1508                                                                   #Thickness of insulation 'm'
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
    
    Thcs = 13
    Thca = 11
    
    Tr = 1/11 + 1/13
    
    U = 1 / Tr
    
    
    
    Hlr = (Tat - Tab) / Se  #Heat loss rate 'K/hr'
    
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
    Rhoi = 86                                                                      #Density of insulation 'kg/m3'
    Vi = ((Od + 2 * Thoi)**2 * np.pi / 4  - Od**2 * np.pi / 4) * L * Nt            #Volume of insulation                                                         
    Tci = Cpt * Vi * Rhoi / 1000                                                   #Total cost of insulation
    
    "Total"
    C = Ttc + Tcs + Tcf + Tcp + Tci                                                #Total cost '$'
    Cpkwh = C / Tse / 1000    

    "Checking minimum size of particle"

    "Alumina"
    
    Ka = 12                                                                        #Thermal Conductivity of Solid     
    Vtta = V * .64                                                                 #Total volume of filler
    ra = .002                                                                      #Radius of filler
    Vpba = 4/3 * 3.14159265 * ra**3                                                #Volume of 1 ball
    Sapba = 4 * 3.14159265 * ra**2                                                 #Surface area of 1 ball
    Nba = Vtta / Vpba                                                              #Number of balls
    Sata = Nba * Sapba                                                             #Total Surface area
    Saica = Sata * tf                                                              #Surface area in contact with thermocline
    Ua = 1/(1/13+1/Ka)
    Qmaxa = Saica * Ua * 10 /1000/1000  
    
    "Steel Slag"
    
    Ks = 1.51                                                                      #Thermal Conductivity of Solid     
    Vtts = V * .64                                                                 #Total volume of filler
    rs = .002   #.00034                                                            #Radius of filler
    Vpbs = 4/3 * 3.14159265 * rs**3                                                #Volume of 1 ball
    Sapbs = 4 * 3.14159265 * rs**2                                                 #Surface area of 1 ball
    Nbs = Vtts / Vpbs                                                              #Number of balls
    Sats = Nbs * Sapbs                                                             #Total Surface area
    Saics = Sats * tf                                                              #Surface area in contact with thermocline
    Us = 1/(1/13+1/Ks)
    Qmaxs = Saics * Us * 10 /1000/1000  
    
    "Fire Brick"
    
    Kf = 3.8                                                                       #Thermal Conductivity of Solid     
    Vttf = V * .64                                                                 #Total volume of filler
    rf = .002   #.00094                                                            #Radius of filler
    Vpbf = 4/3 * 3.14159265 * rf**3                                                #Volume of 1 ball
    Sapbf = 4 * 3.14159265 * rf**2                                                 #Surface area of 1 ball
    Nbf = Vttf / Vpbf                                                              #Number of balls
    Satf = Nbf * Sapbf                                                             #Total Surface area
    Saicf = Satf * tf                                                              #Surface area in contact with thermocline
    Uf = 1/(1/13+1/Kf)
    Qmaxf = Saicf * Uf * 10 /1000/1000  
    
    
    
    def storage_cost(self):
       return print('Total cost of storage $',round(storage.C/1000000,2),'million')
        
    def costperkWh(self):
        return print('Cost per KWh',round(storage.Cpkwh,2),'$/KWh')
    
    def max_stored(self):
        return print('Total possible energy stored =',round(storage.Tse,2),'MWh')
    
    def energy_stored(self):
        return print('Energy currently in storage =',round(storage.Se,2),'MWh')
    
    def energy_in(self):
        return print('Energy in',round(storage.Qi,2),'MJ/s') 
    
    def energy_out(self):
        return print('Energy out',round(storage.Qo,2),'MJ/s')
    
    def time_2fill(self):
        return print(round(storage.ttfh,2),'hours until full')
    
    def time_2empty(self): 
        return print(round(storage.tteh,2),'hours until empty')
    
    def location_of_thermocline(self, t):
        M = storage.M
        tf = .2                                                                   #Size of Thermocline via percentage of tank height
        Thh = storage.L * tf                                                      #Height of the Thermocline 'm'
        Thop = Thh                                                                #Thermocline original position 'm'
                                                                            
        
        if M >= 0:
            Thtc = (storage.Tat - storage.Tab) / Thh                              #Rate of change of temperature in thermocline 'K/m"
            Thv = storage.Mv / storage.At                                         #Thermocline Velocity 'm/s'
        
            Thl = Thv * t
            
            if Thl > Thh:
                Thl = Thh
                    
                   
        if M <= 0:
            Thtc = (storage.Tat - storage.Tab) / Thh                              #Rate of change of temperature in thermocline 'K/m"
            Thv = storage.Mv / storage.At                                         #Thermocline Velocity 'm/s'
        
            Thl = Thop + Thv * t  
            
            if Thl < 0:
                Thl = 0                                                           #Location of Thermocline 'm'
    
        
        return Thl
    
    def massflow_salt(self):
        return storage.M
    
    def hot_temp(self):
        return storage.Tat
    
    def cold_temp(self):
        return storage.Tab 