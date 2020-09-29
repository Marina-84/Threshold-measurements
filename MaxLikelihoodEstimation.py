# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 19:38:57 2020

Function to perform the logarithmic Maximum Likelihood Estimation of the alpha 
and beta parameters of a psychometric function

@author: Marina Torrente Rodriguez
"""

from PsychometricFunctionClass import PsychometricFunction
from scipy.optimize import fsolve
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt



def MLE_search(Gamma, Lambda, type_func, StimLevels, NumCorrect, Total):
    
    # Function to calculate the Maximum Likelihood Estimate for a PF
    def MLE_PF(params):
        # Coefficients to be found
        Alpha , Beta = params[0], params[1]
        # Psychometric function
        PF =  PsychometricFunction(Alpha=Alpha, Beta=Beta, Gamma=Gamma, Lambda=Lambda,
                                   type_func=type_func)
        # Negative log likelihood
        LL = - (np.sum(np.log(PF.PF(StimLevels)) * NumCorrect) + 
                np.sum(np.log(1-PF.PF(StimLevels)) * (Total - NumCorrect)))
        
        return LL

    # Function to provide a first guess for the searched parameters
    def DefineInitialMLESearchParam():
        
        # Guess alpha value corresponds to the mid-point of the stimulus levels
        a = StimLevels[0] + (StimLevels[-1]-StimLevels[0])/2
        if a == 0:
            a = 0.1
        
        # Gues beta value corresponds to the PF crossing the guessed alpha
        # and the measured point with the highgest number of measurements
        ind = np.argmax(Total,axis=0)
        x1 = StimLevels[ind]    
        y1 = NumCorrect[ind]/Total[ind]
        def pf(b):    
            PF =  PsychometricFunction(Alpha=a, Beta=b, Gamma=Gamma, Lambda=Lambda, 
                                       type_func=type_func)
            return PF.PF(x1)-y1
        
        b = fsolve(pf,1)

        return [a, b]
    
    guess = DefineInitialMLESearchParam()
    results = minimize(MLE_PF, guess, method = 'Nelder-Mead', options={'disp': True})

    return results


def TestExample(exID):
    
    if exID == 1:
        # Example data 1
        StimLevels = np.array([0.01, 0.03, 0.05, 0.07, 0.09, 0.11])
        NumCorrect = np.array([45, 55, 72, 85, 91, 100])
        Total = np.array([100, 100, 100, 100, 100, 100])
        typef = "Logistic"
        G = 0.5
        L = 0
        
    elif exID == 2:
        # Example data 2
        StimLevels = np.array([0.01, 0.03, 0.05, 0.07, 0.09, 0.11])
        NumCorrect = np.array([2, 5, 9, 13, 11, 12])
        Total = np.array([19, 21, 18, 17, 12, 13])
        typef = "Logistic"
        G = 0
        L = 0.01
    
    elif exID ==3:
        # Example data 3
        StimLevels = np.linspace(-2,2,5)
        NumCorrect = np.array([2, 3, 3, 3, 4])
        Total = 4*np.ones(5)
        typef = "Logistic"
        G = 0.5
        L = 0
        
    elif exID ==4:
        # Example data 4
        StimLevels = np.array([0.01, 0.03, 0.05, 0.07, 0.09, 0.11])
        NumCorrect = np.array([0, 0, 1, 1, 2, 4])
        Total = np.array([6, 2, 3, 4, 2, 3])
        typef = "Logistic"
        G = 0
        L = 0.01
    
    results = MLE_search(G, L, typef, StimLevels, NumCorrect, Total)
    
    print(results)
    alpha = results.x[0]
    beta = results.x[1]
    
    step = StimLevels[1]-StimLevels[0]
    x = np.linspace(StimLevels[0]-step, StimLevels[len(StimLevels)-1]+step, 100)
    y =  PsychometricFunction(Alpha=alpha, Beta=beta, Gamma=G, Lambda=L,
                              type_func=typef).PF(x)
    
    if results.success:
        plt.figure()
        plt.plot(StimLevels, NumCorrect/Total,'o')
        plt.plot(x,y)
        plt.grid()
        plt.ylabel("Probability of Correct Response")
        plt.xlabel("Stimulus Intensity")
        plt.legend(["Measured","PF Estimate by MLE"])
        plt.ylim(-0.1,1.1)
    
    else:
        print("MLE search not treminated succesfully")


# Test MLE search
#TestExample(1)
#TestExample(2)
#TestExample(3)
#TestExample(4)


        
