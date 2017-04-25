import DataImport as dataImport
import numpy as np
import matplotlib.pyplot as plt 
import WeakModeler as wm

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
    def __init__(self, intFailureType, maxdFr, maxdTr, avgdFr, avgdTr, mindFr, mindTr, avgFtheta, avgTtheta, avgFphi, avgTphi):
        self.intFailureType = intFailureType
        self.maxdFr = maxdFr
        self.maxdTr = maxdTr
        self.avgdFr = avgdFr
        self.avgdTr = avgdTr
        self.mindFr = mindFr
        self.mindTr = mindTr
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
    data3.append(SummaryData(datum.intFailureType, max(dF), max(dT), np.mean(map(np.square, dF)), np.mean(map(np.square,dT)), min(dF), min(dT), np.mean(datum.Fthetas), np.mean(datum.Tthetas), np.mean(datum.Fphis), np.mean(datum.Tphis)))


test0 = []
test1 = []
test2 = []
for datum in data3:
    if datum.intFailureType == 0:
        test0.append(datum.maxdFr)
    elif datum.intFailureType == 1:
        test1.append(datum.maxdFr)
    else:
        test2.append(datum.maxdFr)

#plt.ylabel('y')
#plt.scatter(test0+test1+test2, [0]*len(test0)+[1]*len(test1)+[2]*len(test2))
#plt.show()

f = []
f.append([])
f.append([])
f.append([])
f.append([])
f.append([])
f.append([])
y = []

for datum in data3:
    y.append(datum.intFailureType)
    f[0].append(datum.maxdFr)
    f[1].append(datum.avgdFr)
    f[2].append(datum.mindFr)
    f[3].append(datum.maxdTr)
    f[4].append(datum.avgdTr)
    f[5].append(datum.mindTr) 
m = []
m.append([])
m.append([])
m.append([])


##
##
##
for feature in f:
    for i in range(0,len(m)):
        m[i].append(wm.WeakModeler(feature,y,i))


##
## summarizes weak learners
##
for i in range(0,len(m)):
    for j in range(0,len(f)):
        print "i: %d, j: %d" % (i, j)
        asd = []
        for k in range(0, len(y)):
            if y[k] == i:
                asd.append(f[j][k])
        total = sum(map(m[i][j], f[j]))
        fromknown = sum(map(m[i][j], asd))
        rate = 1-float(total-fromknown)/float(len(f[j]))
        print "total: %d/%d, fromknown: %d/%d, successrate: %f" % (total, len(f[j]), fromknown,len(asd), rate)



# ##initiliaze uniform distribution
# distribution = list((float(1)/len(data3) for i in range(len(data3))))
#
#
# ## adaboost - go through all weak learners
# for j in range(6):
#    m[0].append(wm.WeakModeler(distribution, y, 0))




