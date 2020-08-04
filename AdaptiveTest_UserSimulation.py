# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:26:20 2020

Simulation of a threshold measurement test using an adaptive method based on the presentation
of next stimulus based on the posterior probability

The user behaviour is simulated to test the efficiency of the test

@author: Marina
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from PsychometricFunctionClass import PsychometricFunction
from MaxLikelihoodEstimation import MLE_search




# Define user
user_threshold = 0.06
user_slope = 40
lapse_error = 0.01
test_gamma = 0
typef= "Logistic"
PF_user = PsychometricFunction(Alpha=user_threshold, Beta=user_slope,
                               Gamma=test_gamma, Lambda=lapse_error,
                               type_func=typef, inv=True)

# Test parameters
MaxTrials = 300 # AFter which the test stops
MinTrials = 0.30*MaxTrials # Stimuli intensity for the first number of trials is presented at random 
StimLevels = np.array([0.01, 0.03, 0.05, 0.07, 0.09, 0.11])
Gamma = test_gamma
Lambda = lapse_error
MaxConsecutive = 3

# Initialise test
trials_counter = 0
NumCorrect = np.zeros(len(StimLevels))
Total = np.zeros(len(StimLevels))
stim = []

while (trials_counter < MaxTrials):
    trials_counter += 1

    if trials_counter<= MinTrials:
        # Choose next stimulus intensity randomly
        StimIndex = random.choice(range(len(StimLevels)))

    else:
        
        if ((stim[-MaxConsecutive:-1]-stim[-1]).sum() == 0) & (len(stim) > MaxConsecutive):
            # Choose next stimulus intensity randomly if the same stimilus 
            # has been presented more than 4 consecutive times
            StimIndex = random.choice(range(len(StimLevels)))
        else:            
            # present values by Psi method: 
            # fitting PF taking the estimate PF as the posterior probablity
            results = MLE_search(Gamma, Lambda, typef, StimLevels, NumCorrect, Total)
            alpha, beta = results.x[0], results.x[1]
            
            print("alpha = ", alpha, " ; beta = ", beta)
            
            # find stim level closest to alpha and set as current 
            diff = abs(StimLevels-alpha)
            StimIndex = np.unravel_index(np.argmin(diff, axis=0), diff.shape)
            
#            # Find a stimulus within the steep region of the PF slope
#            y = PsychometricFunction(Alpha=alpha, Beta=beta,
#                               Gamma=test_gamma, Lambda=lapse_error,
#                               type_func=typef).PF(StimLevels)
#            StimCurrent = random.choice(StimLevels[(y>(Gamma+Lambda)) & (y<1)])
            


    # Current Stimulus level by obtained index
    StimCurrent = StimLevels[StimIndex]
    print("Current stimulus: ",StimCurrent) # Print
    stim.append(StimCurrent)                # Store
    
    # Increment number of total stimuli for the current level
    Total[StimIndex] += 1
        
    # Simulate user response
    # User PF value at current stimulus level
    pCurrent = PF_user.PF(StimCurrent)
    # Record as correct response with a random chance 
    # equal to the velue of the PF at that stimulus level
    if random.random() <= pCurrent:
        NumCorrect[StimIndex] += 1
        
    
results = MLE_search(Gamma, Lambda, typef, StimLevels, NumCorrect, Total)
alpha, beta = results.x[0], results.x[1]
print("End of test!")
print("Simulated threshol:", user_threshold, " ; Measured threshold: ", alpha)
print("Simulated slope:", user_slope, " ; Measured slope: ", beta)

x = np.min(StimLevels)
plt.figure()
PF_user.plot_PF(StimLevels[0],StimLevels[-1],100)
plt.scatter(StimLevels,NumCorrect/Total, s=5*Total)
PsychometricFunction(Alpha=alpha, Beta=beta,
                     Gamma=Gamma, Lambda=Lambda,
                     type_func=typef, inv=True).plot_PF(StimLevels[0],StimLevels[-1],100)
plt.grid()
plt.ylabel("Probability of Correct Response")
plt.xlabel("Stimulus Intensity")
plt.legend(["Simulated User", "Measured Behaviour", "Estimate User"])
plt.ylim(-0.1,1.1)

plt.figure()
plt.plot(np.linspace(1,MaxTrials,MaxTrials), stim,'o-')
plt.xlabel("# Trial")
plt.ylabel("Stimulus Level")
    