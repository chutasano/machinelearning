from __future__ import division
import DataImport as dataImport
import numpy as np
import matplotlib.pyplot as plt 
from random import shuffle
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

#gets data in xyz coordinates
plotcount = 6  ##note: make this 0 to skip plotting after data extraction
plot = True ##note: make this false to skip plotting during weak modeling
crossval = 6 ##note: this is the 'k' in cross validation
data = dataImport.getDataInstances("lp4.data")

#this section converts the xyz coordinates to spherical (r,theta, phi) coordinates
data2 = []
for datum in data:
    data2l = SphericalData(datum.intFailureType)
    for i in range(0, 15):
        data2l.Frhos.append(np.sqrt(datum.FxVector[i]*datum.FxVector[i] +   datum.FyVector[i]*datum.FyVector[i] + datum.FzVector[i]*datum.FzVector[i]))
        data2l.Trhos.append(np.sqrt(datum.TxVector[i]*datum.TxVector[i] +   datum.TyVector[i]*datum.TyVector[i] + datum.TzVector[i]*datum.TzVector[i]))
        ftheta = 0
        ttheta = 0
        if datum.FxVector[i] == 0: # fix to division by 0 in arctan
            negcheck = 1
            if datum.FyVector[i] < 0:
                negcheck = -1
            ftheta = negcheck*np.pi/2
        else:  # arctan in -pi/2 to pi/2... Let's fix that to -pi/2 to 3pi/2
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

#############

#now extract features from the spherical
data3 = []
for datum in data2:
    dF = []
    dT = []
    for i in range(0, 14):
        dF.append(datum.Frhos[i+1] - datum.Frhos[i])
        dT.append(datum.Trhos[i+1] - datum.Trhos[i])
    data3.append(SummaryData(datum.intFailureType, max(dF), max(dT), np.mean(map(np.square, dF)), np.mean(map(np.square,dT)), min(dF), min(dT), np.mean(datum.Fthetas), np.mean(datum.Tthetas), np.mean(datum.Fphis), np.mean(datum.Tphis)))

#################
#plots
for i in range(plotcount):
    test0 = []
    test1 = []
    test2 = []
    for datum in data3:
        if i == 0:
            whichdata = datum.maxdFr
        elif i == 1:
            whichdata = datum.avgdFr
        elif i == 2:
            whichdata = datum.mindFr
        elif i == 3:
            whichdata = datum.maxdTr
        elif i == 4:
            whichdata = datum.avgdTr
        else:
            whichdata = datum.mindTr
        if datum.intFailureType == 0:
            test0.append(whichdata)
        elif datum.intFailureType == 1:
            test1.append(whichdata)
        else:
            test2.append(whichdata)
    if i == 0:
        plt.xlabel('Max Delta of Force rho')
    elif i == 1:
        plt.xlabel('Avg Delta of Force rho')
    elif i == 2:
        plt.xlabel('Min Delta of Force rho')
    elif i == 3:
        plt.xlabel('Max Delta of Torque rho')
    elif i == 4:
        plt.xlabel('Avg Delta of Torque rho')
    else:
        plt.xlabel('Min Delta of Torque rho')

    plt.ylabel('0: normal, 1: collision, 2: obstruction')
    plt.scatter(test0+test1+test2, [0]*len(test0)+[1]*len(test1)+[2]*len(test2))
    plt.title("Summary Data")
    plt.show()



## example of our classifiers
f = [[],[],[],[],[],[]]
y = []

for datum in data3:
    y.append(datum.intFailureType)
    f[0].append(datum.maxdFr)
    f[1].append(datum.avgdFr)
    f[2].append(datum.mindFr)
    f[3].append(datum.maxdTr)
    f[4].append(datum.avgdTr)
    f[5].append(datum.mindTr) 
m = [[], [], []]
##
## trains each weak model using the entire dataset... just for demonstraion purposes
##
for feature in f:
    for i in range(0,len(m)):
        m[i].append(wm.WeakModeler(feature,y,i))

##
## summarizes weak learners
##
print "\n\nSummary of the weak classifiers:"
print "Note for the plot: blue -> classified as feature, red -> classified as not feature"
for i in range(0,len(m)):
    for j in range(0,len(f)):
        print "class: %d, feature: %d" % (i, j)
        asd = []
        for k in range(0, len(y)):
            if y[k] == i:
                asd.append(f[j][k])
        total = sum(map(m[i][j], f[j]))
        fromknown = sum(map(m[i][j], asd))
        rate = float(total-fromknown)/float(len(f[j]))
        print "total: %d/%d, fromknown: %d/%d, falseposrate: %f" % (total, len(f[j]), fromknown,len(asd), rate)
        if plot:
            testc = asd 
            test0 = []
            test1 = []
            test2 = []
            whichdata = f[j]
            for k in range(len(y)):
                if y[k] == 0:
                    test0.append(whichdata[k])
                elif y[k] == 1:
                    test1.append(whichdata[k])
                else:
                    test2.append(whichdata[k])
                plt.xlabel("Class: %d, Feature: %d" % (i, j))
            plt.ylabel('0: normal, 1: collision, 2: obstruction')
            plt.scatter(test0+test1+test2, [0]*len(test0)+[1]*len(test1)+[2]*len(test2), \
                    c = map(lambda x: 'b' if x else 'r', map(m[i][j], test0+test1+test2)), s = 50)
            plt.title("Weak Classifer Visualization... blue->classified as the class, red ->no")
            plt.show()



#create training data + testing data from the dataset
print "\n\nStart AdaBoost algorithm ---"
shuffle(data3)
bestP = [0,0,0]
bestH = [None, None, None]
x = [[],[],[],[],[],[]]
y = []
for datum in data3:
    y.append(datum.intFailureType)
    x[0].append(datum.maxdFr)
    x[1].append(datum.avgdFr)
    x[2].append(datum.mindFr)
    x[3].append(datum.maxdTr)
    x[4].append(datum.avgdTr)
    x[5].append(datum.mindTr) 
s = len(y)
for a in range(3):
    print "Training class %d... with cross validation k = %d" % (a, crossval)
    for i in range(crossval):
        testd = [l[int(float(i)/crossval*s) : int(float(i+1)/crossval*s)] for l in x]
        ytestd = y[int(float(i)/crossval*s) : int(float(i+1)/crossval*s)]
        traind = [l[ : int(float(i)/crossval*s)] + l[int(float(i+1)/crossval*s) : ] for l in x]
        ytraind = y[ : int(float(i)/crossval*s)] + y[int(float(i+1)/crossval*s) : ]

        fun = None
        if a == 0:
            fun = lambda x: int(1 - 2 * np.floor(np.sqrt(x)))
        elif a == 1:
            fun = lambda x: int(abs(x-1)*(-2)+1)
        else:
            fun = lambda x: int(-1 + 2*np.floor(x/2))
        initytraind = map(int, ytraind)
        ytraind = map(fun, ytraind)
        ytestd = map(fun, ytestd)
        datasize = len(traind[0])
        weights = np.ones(datasize)/datasize
        fsize = len(traind)
        h = []
        alpha = []


        for j in range(fsize):
            h.append(lambda x: 2* (wm.WeakModeler(traind[j],initytraind,a)(x)) -1)
            e = sum(weights[z] for z in range(datasize) \
                    if ytraind[z] != (h[j](traind[j][z])))
            if e == 0:   #quick fix for the 0 issue
                e = 0.000000001

            alpha.append( 0.5*np.log((1-e)/e))

            for k in range(datasize):
                weights[k] = weights[k] * np.exp(-alpha[j]*ytraind[k]*h[j](traind[j][k]))
            weights = weights/weights.sum()


#        H = lambda x: sum(alpha[j]*h[j](x[j]) for j in range(fsize))
#        corrects = sum(1 for k in range(len(ytestd)) \
#                if np.sign(H([l[k] for l in testd])) == np.sign(ytestd[k]))
#        corrects = sum(1 for k in range(len(ytestd)) \
#                if np.sign(sum(h[j](testd[j][k])) for j in range(fsize) ) == np.sign(ytestd[k]))
        corrects = 0
        for  k in range(len(ytestd)):
            sum2 = 0.0
            for j in range(fsize):
                sum2 = sum2 + alpha[j]*h[j](testd[j][k])
            if np.sign(sum2) == np.sign(ytestd[k]):
                corrects = corrects + 1
        print "    Correctness of boosted model (i = %d)): %3f" % (i, float(corrects)/len(ytestd))
        if float(corrects)/len(ytestd) > bestP[a]:
            bestP[a] = float(corrects)/len(ytestd)
            bestH[a] = (list(alpha), list(h))  #bestH is a tuple(alpha, lambda)
print "Best model successrates using cross validation (normal, collision, obstruction):"
print bestP




print "Now use 1 vs all method with strict thresholding to test on all data:"
successes = 0
unsures = 0
for i in range(len(y)):
    result = []
    for a in range(3):
        sum2 = 0.0
        for j in range(len(x)):
            sum2 = sum2 + bestH[a][0][j]*bestH[a][1][j](x[j][i])
        result.append(np.sign(sum2))
    if sum(result) == -1:  #means 2 disagreed and 1 agreed, aka we have a conclusive answer
        if result[0] == 1 and y[i] == 0:
            successes = successes + 1
        elif result[1] == 1 and y[i] == 1:
            successes = successes + 1
        elif result[2] == 1 and y[i] == 2:
            successes = successes + 1
    else:
        unsures = unsures + 1
print "Successes: %d/%d, Uncertains: %d" % (successes, len(y), unsures)


print "Now use 1 vs all method with loose thresholding to test on all data:"
successes = 0
for i in range(len(y)):
    result = []
    for a in range(3):
        sum2 = 0.0
        for j in range(len(x)):
            sum2 = sum2 + bestH[a][0][j]*bestH[a][1][j](x[j][i])
        result.append(sum2)
    lmax = max(result)
    if result[0] == lmax and y[i] == 0:
        successes = successes + 1
    elif result[1] == lmax and y[i] == 1:
        successes = successes + 1
    elif result[2] == lmax and y[i] == 2:
        successes = successes + 1
print "Successes: %d/%d" % (successes, len(y))
