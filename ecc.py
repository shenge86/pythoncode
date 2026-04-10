# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:38:08 2026

@author: sheng
@name: Expected Casualty Calculator
"""
from enum import Enum
import numpy as np

class FailureMode(Enum):
    THRUST_FAILURE = 'Thrust_Failure'
    EXPLOSION      = 'Explosion'
    GNC_FAILURE    = 'GNC_Failure'
    


if __name__ == '__main__':
    print('Run basic assessment....')
    print('''Two strategies: 
          1. Reduce probability and area of impact.
          2. Reduce density of impact based on trajectory flies over.
          ''')
    
    time_of_flight = [0, 100, 200] # seconds
    
    # read in an ephemeris (trajectory kernel)
    
    
    #%% Failure modes
    # this is the probability of actual failure regardless of trajectory
    print('''
          Probability of failure will depend on a thorough analysis of all potential failure origins
          and each of their respective failure probabilities. Assuming also no redundancies to handle 
          failures
          
          Note also probability of failure can depend on what flight phase the vehicle is
          Explosion soon after launch probability?
          No guidance and control after all prop used up?
          ''')
          
    p_failure = 0.0001
    
    #%% Casualty area
    print('''
        Casualty area dependent on human
        exposure to debris and the debris size, weight, velocity
        components, ballistic coefficients (weight/maximum crosssectional 
                                            area of a piece of debris), kinetic energy,
        impact, bounce, slide and fragmentation characteristics
        of that debris, as well as any explosive properties the
        debris might have.
        
        If the failure is an explosion
        soon after launch the amount of impacting debris may be
        at a maximum because the bulk of the propellant has not
        been burned and early boost stages, if any, have not been
        safely jettisoned. This may be contrasted with an out of
        control ballistic reentry of a single stage vehicle with
        no propellant or hazardous material on board. The latter
        scenario would involve minimal debris generation. 
          ''')
    
    # determine a function to calculate the area based on what time of flight this is    
    
    #%%
    P = np.array([1, 1, 1]) * p_failure # probability (must be between 0 and 1)
    A = np.array([100, 200, 300])   # casualty area in square meters
    D = np.array([47, 1500, 5])  # population density of the area at risk for ith event
    
    Ec = 0
    for prob, area, density in zip(P, A, D):
        Ec += prob * area * density
        
    print(Ec)
    
    Ec_limit = 0.00003 # accepted casualty ratees
    if Ec > Ec_limit:
        print(f'Warning! This trajectory goes over accepted casualty rate of {Ec_limit}')
        
    #%% Monte Carlo study for dispersed trajectories 
    # Impact probability geographic region
    print('''
          Probability of a particular impact within a region comes from Monte Carlo studies.
          Run a bunch of cases (>1000) around a nominal trajectory from its initial condition
          with dispersed conditions 
          
          Ideally run it through a 6 DOF simulator but without it can do a simpler analysis
          with a constant cross-track angle and assuming a constant descent rate.
          ''')
    
    print('Need a probability map and a population density map overlaid for the same regions.')
    
    # these are probabilities that a trajectory ends up in that area
    p_1sigma = 0.6827
    p_2sigma = 0.2718 # between +/-1 and +/-2 sigma
    p_3sigma = 0.0428 # between +/-2 and +/-3 sigma
    