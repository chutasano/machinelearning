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

data = dataImport.getDataInstances("lp4.data")

#print "*****\nDATA\n*****"
#for datum in data:
#    print "\nFailure type %d" % datum.intFailureType
#    print "Force x-component:"
#    print datum.FxVector
#    print "Force y-component:"
#    print datum.FyVector
#    print "Force z-component:"
#    print datum.FzVector
#    print "Torque x-component:"
#    print datum.TxVector
#    print "Torque y-component:"
#    print datum.TyVector
#    print "Torque z-component:"
#    print datum.TzVector
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



for datum in data2:
    print "\nFailure type %d" % datum.intFailureType
    print "Force x-component:"
    print datum.Frhos
    print "Force y-component:"
    print datum.Trhos
    print "Force z-component:"
    print datum.Fphis
    print "Torque x-component:"
    print datum.Tphis
    print "Torque y-component:"
    print datum.Fthetas
    print "Torque z-component:"
    print datum.Tthetas




