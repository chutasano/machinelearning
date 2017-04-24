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
        ftheta = 0
        ttheta = 0
        if datum.FxVector[i] == 0:
            negcheck = 1
            if datum.FyVector[i] < 0:
                negcheck = -1
            ftheta = negcheck*np.pi/2
        else:
            ftheta = np.arctan(datum.FyVector[i]/datum.FxVector[i])
            if (datum.FxVector[i] < 0 and datum.FyVector[i] < 0) or (datum.FxVector < 0 and datum.FyVector > 0):
                ftheta = ftheta + np.pi

        if datum.TxVector[i] == 0:
            negcheck2 = 1
            if datum.TyVector[i] < 0:
                negcheck2 = -1
            ttheta - negcheck*np.pi/2
        else:
            ttheta = np.arctan(datum.TyVector[i]/datum.TxVector[i])
            if (datum.TxVector[i] < 0 and datum.TyVector[i] < 0) or (datum.TxVector < 0 and datum.TyVector > 0):
                ttheta = ttheta + np.pi

        data2l.Fthetas.append(ftheta)
        data2l.Tthetas.append(ttheta)
        data2l.Fphis.append(np.arccos(datum.FzVector[i]/data2l.Frhos[i]))
        data2l.Tphis.append(np.arccos(datum.TzVector[i]/data2l.Trhos[i]))
    data2.append(data2l)

data3 = []
for datum in data2:
    dF = []
    dT = []
    for i in range(0, 14):
        dF.append(datum.Frhos[i+1] - datum.Frhos[i])
        dT.append(datum.Trhos[i+1] - datum.Trhos[i])
    data3.append(SummaryData(datum.intFailureType, max(map(abs, dF)), max(map(abs, dT)), np.mean(dF), np.mean(dT), np.mean(datum.Fthetas), np.mean(datum.Tthetas), np.mean(datum.Fphis), np.mean(datum.Tphis)))


test0 = []
test1 = []
test2 = []
for datum in data3:
    if datum.intFailureType == 0:
        test0.append(datum.avgdFr)
    elif datum.intFailureType == 1:
        test1.append(datum.avgdFr)
    else:
        test2.append(datum.avgdFr)

print "mean"
print np.mean(test0)
print np.mean(test1)
print np.mean(test2)
print "max"
print max(test0)
print max(test1)
print max(test2)
print "min"
print min(test0)
print min(test1)
print min(test2)
