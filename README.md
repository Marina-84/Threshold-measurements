# github-psycophysics
## Adaptive method to measure sensory thresholds
An adaptive method based on the posterior distribution is implemented, resulting in a lower number of trials required to measure sensory thresholds. The method is known as the Psi method according to [1] and it is modified to avoid the same stimulus being presented in multiple consecutive times throughout the test, thus gaining more confidence
on the threshold value and slope of the psychometric function. 

[1] Psychophysics. A practical introduction. F. A. A. Kingdom & N. Prins

## Usage
- Use the simulation script 'AdaptiveTest_UserSimulation.py' to adjust the experiment parameters 
- Run the experiment script 'LinesLengthJNDThreshold.py' to take a test based on the adaptive procedure implemented. In this test your ability to distinguish between the length of two lines is assessed. Your results are shown at the end of the experiment.

<img src="https://github.com/Marina-84/Threshold-measurements/blob/master/Lines_GUI.PNG" width="40%">

## Customisation
The following parameters can be customized to design a suitable experiment depending on the application:
```
# Test parameters
MaxTrials = 50                  # After which the test stops
MinTrials = 0.10*MaxTrials      # Stimuli intensity for the first number of trials is presented at random 
StimLevels = np.arange(0,15,1)  # Array of stimulus intensity levels
Gamma = 1/2                     # Depends on the type of test; the M-Force Choice methods Gamma = 1/M
Lambda = 0.01                   # If not known from experience, this is usually set to 0.01
MaxConsecutive = 3              # Maximum number of time the same value of stimulus intensity can be presented consecutively
```
Different subjects' behaviour can be simulated by manipulating the following parameters:
```
# Define user         
user_threshold = 3    # Simulated user threshold
user_slope = 40       # Simulated user slope
lapse_error = 0.01    # Typical value of lapse error
test_gamma = 1/2      # Given by the type of test
typef= "Logistic"     # Simulated type of behaviour

```
The performance of the algorithm is shown at the end of the simulation, as shown in the figure below. This shows the number of trials required for the estimation to converge towards the 'true' thresjold and slope.

<img src="https://github.com/Marina-84/Threshold-measurements/blob/master/Method_performance_progress_example.png" width="40%">
