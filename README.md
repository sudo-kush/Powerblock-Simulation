# Powerblock-Simulation
# -----------------------------------------------------------------------
Initial Steps 

Step 1: Download all files into same folder

Step 2: Install iapws (steam tables) via iPython Console or command line <$ pip install iapws> 
Or hit the following link: https://pypi.org/project/iapws/ 

# -----------------------------------------------------------------------
Simulation Files 

Scenario 1: Runs the efficiency and Power output (MWe) given a reactor size and relates it to changing stored energy. 

Scenario 2: Runs through iterations of different outlet temperatures from the TES Storage. Plots Output Temp vs. Efficiency and Power Output. 

Scenario 3: 

# -----------------------------------------------------------------------
Back-End Files 

Components: This file has all the equation that model turbines, condensor, steam generator etc. 

Storage: This file models the thermal energy packed bed thermocline system that is implemented in the scenarios ran. You can see use this file to see total cost of storage, amount of tanks, location of thermocline, time needed to fill for a certain amount of energy, etc.  

Cycle: This file will go through one iteration of steam generation cycle. You can see stuff like carnot efficiency, rankine efficiency, heat input (Qin), power output from each turbine, power required by the pumps, etc. 

Power: This file is basically the cycle file in function form where you can alter the load and the mass flow rate. 

Optimize: This file was used in optimization of the pressure ratios of the turbines and extraction percentages for the feedwater heaters. 

Energy: This file shows the amount of heat in (Qin) you need in the steam generator to model a theorectical grid demand. 
