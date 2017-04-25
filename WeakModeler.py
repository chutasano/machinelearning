import numpy as np
# x : nump of points
# y : expected response
# c : class to classify
# alpha : learning rate
def WeakModeler(x, y, c):
    xc = []
    x1 = []
    x2 = []
    for i in range(0, len(x)):
        if y[i] == c:
            xc.append(x[i])
        elif y[i] == (c+1)%3:
            x1.append(x[i])
        else:
            x2.append(x[i])
    a = min(xc)
    b = max(xc)
    m1 = train(x1, xc)
    m2 = train(x2, xc)
    return lambda x: m1(x) and m2(x)

def train(x, xc):
    xt = list(set(x + xc))
    best = 0
    bestt = -1
    bestflag = 0
    if np.median(x) < np.median(xc):
        bestflag = 0
        for xi in xt:
            a = float(numls(x, xi))/len(x) + float(numgt(xc, xi))/len(xc)
            if a > best:
                best = a
                bestt = xi
    elif np.median(x) > np.median(xc):
        bestflag = 1
        for xi in xt:
            a = float(numgt(x, xi))/len(x) + float(numls(xc, xi))/len(xc)
            if a > best:
                best = a
                bestt = xi
                bestflag = 1
    else:
        for xi in xt:
            a = float(numls(x, xi))/len(x) + float(numgt(xc, xi))/len(xc)
            if a > best:
                best = a
                bestt = xi
        for xi in xt:
            a = float(numgt(x, xi))/len(x) + float(numls(xc, xi))/len(xc)
            if a > best:
                best = a
                bestt = xi
                bestflag = 1
    print "bestt, best"
    print bestt
    print best
    print bestflag
    if bestflag == 0:
        return lambda x: x >= bestt
    else:
        return lambda x: x <= bestt

# number of times an element in x is greater than num
# x : list
# num: num
def numgt(x, num):
    return sum(1 for i in x if i >= num)

def numls(x, num):
    return sum(1 for i in x if i <= num)
