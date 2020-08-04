# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:15:38 2020

Definion of a class Psychometric Function (PF) that allows the calculation of 
several type of PFs, plotting the results and calculating the inverse values

@author: Marina
"""



# Import required libraries
import numpy as np
from pynverse import inversefunc
import matplotlib.pyplot as plt

# Define a Psychometric Function class of default type Logistic
class PsychometricFunction():
    def __init__(self, Alpha, Beta, Gamma, Lambda, type_func="Logistic", inv=False):
        self.Alpha = Alpha
        self.Beta = Beta
        self.Gamma = Gamma
        self.Lambda = Lambda
        self.type_func = type_func
        

        if self.type_func == "Logistic":
            self.PF = lambda x: self.Gamma+ (1-self.Gamma-self.Lambda) * (1 / (1 + np.exp(-self.Beta*(x-self.Alpha))))
        
        elif self.type_func == "Weibull":
            self.PF = lambda x: self.Gamma+ (1-self.Gamma-self.Lambda) * (1 - np.exp(-((x/self.Alpha)**self.Beta)))
            
        elif self.type_func == "Gumbel":
            self.PF = lambda x: self.Gamma+ (1-self.Gamma-self.Lambda) * (1 - np.exp(-10**(self.Beta*(x-self.Alpha)))) 
            
        else:
            print("Error: Psychometric function type not identified!")
                    
            
        if inv:
            self.invPF = lambda y: inversefunc(self.PF, y_values=y)
        
    
    def plot_PF(self, start, end, num_points, title=""):
        x = np.linspace(start, end, num=num_points)
        fx = self.PF(x)
#        plt.figure()
        plt.plot(x,fx)
        plt.title(title)
        plt.ylim(0,1)
        plt.grid()
        plt.show()
        

## Use example
def PFexample():
        
    # Create an element class
    myPF = PsychometricFunction(Alpha=1, Beta=3, Gamma=0.5, Lambda=0.01,
                                 type_func="Logistic", inv=True)
    # Plot psychometric function
    myPF.plot_PF(-5,5,2000, title="Logistic example")
    # Add labels
    plt.ylabel("Proportion of Correct Responses")
    plt.xlabel("Stimuli Intensity")
    # Print threshold value: @ mid-point of the PF in Logistic form
    print("The thrshold value is ", myPF.invPF(0.75))
    # Show threshold point in plot
    plt.plot(myPF.invPF(0.75), 0.75, 'o')

#PFexample()

## Weigbull example (ONLY for positive values of x, alpha & beta)
#myPF_w = PsychometricFunction(Alpha=1,Beta=3, Gamma=0, Lambda=0,
#                             type_func="Weibull", inv=True)
#myPF_w.plot_PF(0,5,2000, title="Weigbull example")
#
#
## Gumbel example(for log transform of x, B>0)
#myPF_w = PsychometricFunction(Alpha=1,Beta=3, Gamma=0, Lambda=0,
#                             type_func="Gumbel", inv=True)
#myPF_w.plot_PF(0,5,2000, title="Gumbel example")

