import DataImport as dataImport
import numpy as np

class SphericalData(object):
    def __init__(self, intFailureType):
        self.intFailureType = intFailureType
        self.Frhos = []
        self.Fthetas = []
        self.Fphis = []
        self.Trhos = []
        self.Tthetas = []
        self.Tphis = []

class SummaryData(object):
    def __init__(self, intFailureType, maxdFr, maxdTr, avgdFr, avgdTr, avgFtheta, avgTtheta, avgFphi, avgTphi):
        self.intFailureType = intFailureType
        self.maxdFr = maxdFr
        self.maxdTr = maxdTr
        self.avgdFr = avgdFr
        self.avgdTr = avgdTr
        self.avgFtheta = avgFtheta
        self.avgTtheta = avgTtheta
        self.avgFphi = avgFphi
        self.avgTphi = avgTphi


data = dataImport.getDataInstances("lp4.data")

data2 = []
for datum in data:
    data2l = SphericalData(datum.intFailureType)
    for i in range(0, 15):
        data2l.Frhos.append(np.sqrt(datum.FxVector[i]*datum.FxVector[i] +   datum.FyVector[i]*datum.FyVector[i] + datum.FzVector[i]*datum.FzVector[i]))
        data2l.Trhos.append(np.sqrt(datum.TxVector[i]*datum.TxVector[i] +   datum.TyVector[i]*datum.TyVector[i] + datum.TzVector[i]*datum.TzVector[i]))
        if datum.FxVector[i] == 0:
            negcheck = 1
            if datum.FyVector[i] < 0:
                negcheck = -1
            data2l.Fthetas.append(negcheck* np.pi/2)
        else:
            data2l.Fthetas.append(np.arctan(datum.FyVector[i]/datum.FxVector[i]))
        if datum.TxVector[i] == 0:
            negcheck2 = 1
            if datum.TyVector[i] < 0:
                negcheck2 = -1
            data2l.Tthetas.append(negcheck2 * np.pi/2)
        else:
            data2l.Tthetas.append(np.arctan(datum.TyVector[i]/datum.TxVector[i]))

        data2l.Fphis.append(np.arccos(datum.FzVector[i]/data2l.Frhos[i]))
        data2l.Tphis.append(np.arccos(datum.TzVector[i]/data2l.Trhos[i]))
    data2.append(data2l)

data3 = []
for datum in data2:
    dF = []
    dT = []
    for i in range(0, 14):
        dF.append(datum.Frhos[i] - datum.Frhos[i+1])
        dT.append(datum.Trhos[i] - datum.Trhos[i+1])
    data3.append(SummaryData(datum.intFailureType, max(dF), max(dT), np.mean(dF), np.mean(dT), np.mean(datum.Fthetas), np.mean(datum.Tthetas), np.mean(datum.Fphis), np.mean(datum.Tphis)))


print data[0].FxVector
print data[0].FyVector
print data[0].FzVector
print data2[0].Frhos
print "asdf"

#data3 contains summary data to use
print data3[0].intFailureType
print data3[0].maxdFr
print data3[0].maxdTr
print data3[0].avgdFr
print data3[0].avgdTr


