#! /usr/bin/env python
import matplotlib.pyplot as plt
import scipy
import numpy 
from numpy.linalg import *
from scipy.linalg import *
from math import sqrt
import pdb
import decimal



def caculateGamma00(T):
    
    """ Initialize gamma00 """
    
    w, v = scipy.linalg.eig(T,left=True, right=False)
    index = numpy.where(w==1)[0][0]
    p = v[:,index]
    k = 1 / sum(p) 
    gamma00 = k*p

    # Limiting gammma00 elements to two decimal points
    temps = 1
    for i in range (n - 1):
        gamma00[i] = float("{0:.2f}".format(gamma00[i]))
        temps = temps - gamma00[i]
    gamma00[n-1] = temps
    #print gamma00

    return gamma00


def creatMarkovChaine(n, gamma00, lengthChain, lengthStep,
                      minLength, maxLength):
    
    """ Generete Markov chain only for nbState = 2 """
    
    markovChain = scipy.zeros(lengthChain, dtype=scipy.dtype(decimal.Decimal))
    for i in xrange (0, lengthChain):
        # Verify if it's a step 
        if i%lengthStep == 0:
            u = scipy.random.random(1)
            x = 0
            for j in xrange(n):
                # Initialize start state
                if i == 0:
                    x = x + gamma00[j]
                # Make steps through the Markov chain
                else:
                    x = x + T[state, j]
                if (x >= u):
                    newState = j 
                    break
            state = newState
        else:
            newState = state
        # Generate values for Markov chain
        if newState == 0:
            markovChain[i] = minLength
        elif newState == 1:
            markovChain[i] = maxLength

    print sum(markovChain == maxLength)
    print sum (markovChain == minLength)
    plt.plot(markovChain)
    plt.show()
            
    return markovChain


def simulation(l, c, maxLength, minLength, gamma00,
               markovChain, cStar, val):
    """
    Variables for Generatation model
    @param val : choice for genaration Mt approach 1 by random, 2 all 1s, 3 by decision
    """

    #b1 = (maxLength-l) / (maxLength-minLength)
    b2 = 1 - (c / (maxLength-l))
    b3 = c / (l-minLength)
    # Array list who appends all possible values in Markov chain 
    values = []
    values.append(minLength)
    values.append(maxLength)
    ValuesArr = numpy.array(values)

    # Generate of verctor gamma_{t,t} 
    gammaTT = [] # list of gamma_{t}{t}, start with gamma00
    gammaTT.append(gamma00)
    gammaT_1T = [] # List of gamma_{t-1}{t}, start with gamma_{0}{1}
    x = scipy.zeros(lengthChain - 1, dtype=scipy.dtype(decimal.Decimal)) # List of gamma_{t-1}{t}[0](t >= 1), start with gamma_{0}{1}[0]

    """ Generate Mt """
    # Generate Mt[i] by random
    if val == 1:
        Mt = scipy.random.randint(2, size=lengthChain-1)
    # Generate Mt[i] all 1s
    elif val == 2:
        Mt = scipy.ones(lengthChain - 1)
    else :
        Mt = scipy.zeros(lengthChain - 1) # No dicision for gamma00, Mt[t-1] is for caculating gamma_{t}{t}(t >= 1). Initialization with all 0s.
    for i in xrange(0, lengthChain-1):
        # Caculate gammaT_1T[i] and x[i]
        gamma = gammaTT[i].dot(T)
        gammaT_1T.append(gamma)
        x[i] = gamma[0]
        # Generate Mt[i] by decision if val1 == 3
        if val == 3:
            if c < cStar :
                if x[i] > b2 or x[i] == b2:
                    Mt[i] = 0
                elif (x[i] > b3 or x[i] == b3) and x[i] < b2 :
                    Mt[i] = 1
                elif x[i] < b3 :
                    Mt[i] = 0
                #print Mt[i]
            else:
                Mt[i] = 0
        # Caculate gammaTT[i+1] 
        e = scipy.zeros(n, dtype=scipy.dtype(decimal.Decimal)) 
        if Mt[i] == 1:
            # if choose markov chain, e is a line verctor with one 1, 0 for others
            index = numpy.where(ValuesArr==markovChain[i+1])[0][0]
            e[index] = 1.
        elif Mt[i] == 0:
            e = gammaTT[i].dot(T)
        gammaTT.append(e)

    # Calculate gain Gt, Ct and GtExpected
    GtExpected = scipy.zeros(lengthChain-1, dtype=scipy.dtype(decimal.Decimal))
    Gt = scipy.zeros(lengthChain-1, dtype=scipy.dtype(decimal.Decimal))
    Ct = scipy.zeros(lengthChain - 1)
    for i in xrange (lengthChain - 1):
            if Mt[i] == 1:
                if markovChain[i+1] == minLength:
                    Ct[i] = 1
                    Gt[i] = l - minLength - c
                if markovChain[i+1] == maxLength:
                    Ct[i] = 0
                    Gt[i] = -c
            if Mt[i] == 0:
                cTemps = decimal.Decimal((l-minLength)*x[i] - (maxLength-l)*(1-x[i]))
                #p = gammaTT[i].dot(T)
                #gamma = gammaT_1T[i]
                #cTemps1 = decimal.Decimal((l-minLength)*p[0] - (maxLength-l)*(1-p[0]))
                #cTemps2 = decimal.Decimal((l-minLength)*gamma[0] - (maxLength-l)*(1-gamma[0]))
                if cTemps > 0 :
                    Ct[i] = 1
                    GtExpected[i] = cTemps
                    if markovChain[i+1] == minLength:
                        Gt[i] = l - minLength
                    if markovChain[i+1] == maxLength:
                        Gt[i] = l - maxLength
                else:
                    Ct[i] = 0
                    Gt[i] = 0
    return Ct, Mt, Gt, GtExpected


def showTrace(vector, title, xLabel, yLabel):
    size = len(vector)
    x = scipy.linspace(0, size, size)
    f=plt.figure()
    ax = f.add_subplot(111)
    ax.scatter(x, vector,  s=150, marker = ".")
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_xlim = ([0, size+10])
    ax.set_ylim = ([min(vector)-3, max(vector)+3])
    ax.set_title( title )
    plt.draw()
    # to save image
    '''
    path = []
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../image'))
    f.savefig(path +'/cumulativeDif2.png')
    '''
    f.show()


 

if __name__ == "__main__":
    
    """
    Simulation Model
    """

    """ Globle Variables """
    n = 2   # Top boundary, number of states 0..n-1 is n
    nbSteps = 1000 # Number of steps where markov chain verify if it change state
    lengthStep = 3 # Between each two steps, include two sub time slot 
    lengthChain = lengthStep*nbSteps + 1 # + start state

    """ Transition matrix """
    T = scipy.diag(scipy.ones(n-1, dtype=scipy.dtype(decimal.Decimal)), 1)
    T[0,0] = 0.3; T[0,1] = 0.7;
    T[1,0] = 0.15; T[1,1] = 0.85;

    gamma00 = caculateGamma00(T)

    """ Variables for genaration Markov chain for only two states in the chain """
    minLength = 100.
    maxLength = 600.
    markovChain = creatMarkovChaine(n, gamma00, lengthChain,
                                    lengthStep, minLength, maxLength)

    """ Variables for simulation """
    l = 300.
    cStar = (maxLength-l) * (l-minLength) / (maxLength-minLength)
    c = 60 #scipy.random.randint(0,2*cStar)

    
    """choice for genaration Mt approach 1 by random, 2 all 1s, 3 by decision"""
    #Ct1, Mt1, Gt1, GtExpected1 = simulation(l, c, maxLength,
                                        #minLength, gamma00,
                                        #markovChain, cStar, 1)

    Ct2, Mt2, Gt2, GtExpected2 = simulation(l, c, maxLength,
                                            minLength, gamma00,
                                            markovChain, cStar, 2)

    Ct3, Mt3, Gt3, GtExpected3 = simulation(l, c, maxLength,
                                            minLength, gamma00,
                                            markovChain, cStar, 3)

    #showTrace(Ct2, 'Ct2', 'time', 'decision')
    print 'results Ct for 1s'
    print sum(Ct2 == 1)
    print sum(Ct2 == 0)
    #showTrace(Ct3, 'Ct3', 'time', 'decision')
    print 'results Mt for 1s'
    print sum(Mt2 == 1)
    print sum(Mt2 == 0)
    print 'results Ct for decision'
    print sum(Ct3 == 1)
    print sum(Ct3 == 0)
    #showTrace(Mt3, 'Mt3', 'time', 'decision')
    print 'results Mt for decision'
    print sum(Mt3 == 1)
    print sum(Mt3 == 0)
    #showTrace(Gt2, 'Gt2', 'gain', 'time')
    print 'results for all 1s Gt'
    print sum(Gt2 == 0)
    print sum(Gt2 == 200)
    print sum(Gt2 == -300)
    print sum(Gt2 == 140)
    print sum(Gt2 == -60)
    print sum(Gt2)
    #showTrace(Gt3, 'Gt3', 'time', 'gain')
    print 'results Gt for decision'
    print sum(Gt3 == 0)
    print sum(Gt3 == 200)
    print sum(Gt3 == -300)
    print sum(Gt3 == 140)
    print sum(Gt3 == -60)
    print sum(Gt3)

    
    #showTrace(Mt2, 'Mt2', 'time', 'Mt')
    #showTrace(Ct2, 'Ct2', 'time', 'Ct')
    #showTrace(Mt3, 'Mt3', 'time', 'Mt')
    #showTrace(Ct3, 'Ct3', 'time', 'Ct')



    


