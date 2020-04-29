"""
senario 3
"""
import numpy as np
import matplotlib.pyplot as plt
import power

# national grid demand on 2/25/20
demandCurve = [401500.8,
               390112.8,
               384000.0,
               382496.5,
               385849.3,
               399866.0,
               430020.5,
               457519.5,
               468380.0,
               471400.8,
               469545.8,
               463723.8,
               457400.0,
               452088.8,
               448430.5,
               444356.3,
               447003.0,
               453977.0,
               467393.5,
               478046.0,
               479302.0,
               470535.0,
               451562.3,
               431344.5]

steamFlow = 155
nmax,Qmax,Pmax = power.Cycle(1.0,steamFlow)

demandPercent = np.zeros(len(demandCurve))
requiredPower = np.zeros(len(demandCurve))
requiredHeat  = np.zeros(len(demandCurve))
saltFlow      = np.zeros(len(demandCurve))
tankFlow      = np.zeros(len(demandCurve))
zeroLine      = np.zeros(len(demandCurve))
reactorLine   = np.zeros(len(demandCurve))
hour          = np.zeros(len(demandCurve))

for i in range(len(demandCurve)):
    demandPercent[i] = demandCurve[i]/np.max(demandCurve)
    nth,Q,P = power.Cycle(1.0,steamFlow)
    for j in range(40):
        load = 1 - j/100
        nth,Q,P = power.Cycle(load,steamFlow)
        hour[i] = i+1
        if(P >= demandPercent[i]*Pmax):
            requiredPower[i] = P
            requiredHeat[i] = Q
            saltFlow[i] = Q / 447.0714
            tankFlow[i] = saltFlow[i] - 1100
            zeroLine[i] = 0
            reactorLine[i] = 1100
        else:
            break

plt.title("Required power and heat for power cycle")
plt.ylim(0, 650000)
plt.ylabel("(MW)")
plt.xlabel("time of day (hr)")
plt.plot(hour, requiredPower, 'b')
plt.plot(hour, requiredHeat, 'r')
plt.show()

plt.title("Flow of salt through steam gen.")
plt.ylim(800, 1300)
plt.ylabel("(kg/s)")
plt.xlabel("time of day (hr)")
plt.plot(hour, saltFlow)
plt.plot(hour, reactorLine, ':k')
plt.show()

plt.style.use('seaborn')
plt.title("Flow of salt in/out of tanks")
plt.ylim(-200, 200)
plt.ylabel("(kg/s)")
plt.xlabel("time of day (hr)")
plt.plot(hour, tankFlow)
plt.plot(hour, zeroLine, ':k')
plt.show()






