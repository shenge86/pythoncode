# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:54:48 2024

@author: Shen Ge
@name: Vector Calculator
@description:
    
    Plots out different vectors according to specifications.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__ == '__main__':    
    # Define the vector components
    vector = np.array([3, 4, 5])
    
    # Create another vector in same direction with different length (magnitude)
    mean = np.linalg.norm(vector)
    vector_unit = vector / mean
    
    # number of randomized vectors
    n = 1000
    
    #%% Create fixed magnitude offsets (resolution error)
    threesigma = 1.5
    sigma      = threesigma/3    # this is a fixed magnitude
    
    # uncomment following only if we are saying we care just 1 error
    # If we want to calculate it directly do this:
    # vectors_fixedoffset_magnitudes = np.random.normal(mean, sigma, 10)            
    # magnitude_matrix = np.transpose(np.tile(vectors_fixedoffset_magnitudes,(3,1)))
    # example with 10:
    # array([[6.37689186, 6.37689186, 6.37689186],
    #        [7.8216075 , 7.8216075 , 7.8216075 ],
    #        [6.78860865, 6.78860865, 6.78860865],
    #        [7.04551036, 7.04551036, 7.04551036],
    #        [7.11160532, 7.11160532, 7.11160532],
    #        [7.53646483, 7.53646483, 7.53646483],
    #        [7.91480414, 7.91480414, 7.91480414],
    #        [6.60397245, 6.60397245, 6.60397245],
    #        [7.93335531, 7.93335531, 7.93335531],
    #        [7.52989555, 7.52989555, 7.52989555]])
    
    # vectors_fixedoffset = vector_unit * magnitude_matrix 
    # example with 10:
    # array([[2.70548609, 3.60731478, 4.50914348],
    #        [3.31842702, 4.42456937, 5.53071171],
    #        [2.88016273, 3.84021697, 4.80027121],
    #        [2.98915689, 3.98554252, 4.98192815],
    #        [3.01719861, 4.02293148, 5.02866435],
    #        [3.19745123, 4.26326831, 5.32908539],
    #        [3.35796701, 4.47728934, 5.59661168],
    #        [2.80182822, 3.73577096, 4.6697137 ],
    #        [3.3658376 , 4.48778347, 5.60972934],
    #        [3.19466412, 4.25955216, 5.3244402 ]])
    
    # However, recall we care about errors and not the actual amount
    vectors_fixedoffset_magnitudes = np.random.normal(0, sigma, n)            
    magnitude_matrix               = np.transpose(np.tile(vectors_fixedoffset_magnitudes,(3,1)))
    vectors_fixedoffset            = vector_unit * magnitude_matrix 
    
    
    #%% Create proportional magnitude offsets
    sigma = 0.2 # this multiplied by 100 is a percentage
    vectors_proportional_magnitudes = np.random.normal(0, sigma, n)
    magnitude_proportional_matrix   = np.transpose(np.tile(vectors_proportional_magnitudes,(3,1)))

    # note this is NOT based on unit vector but the vector itself    
    vectors_proportionaloffset      = vector * magnitude_proportional_matrix
    
    #%% Combined vector and histogram plot    
    vectors_totalerror = vectors_fixedoffset + vectors_proportionaloffset
    vectors            = vector + vectors_totalerror
    
    # if only in-line, this should match the original unit vector
    # the direction does not change so all unit vectors should match!
    for vector in vectors:
        vector_normalized = vector/np.linalg.norm(vector)
        print(vector_normalized)
        # assert np.array_equal(vector_normalized,vector_unit) # cannot do this since may have rounding errors
        assert np.allclose(vector_normalized,vector_unit,atol=1e-6)
    
    #%%
    # Create the histogram
    # plt.hist(vectors, bins=50, alpha=0.75, color='blue', edgecolor='black')
    plt.hist(vectors, bins=50, alpha=0.75)
    
    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Normal Distribution (3-Sigma)')
    
    # Add a vertical line for the mean
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=2)
    
    # Add vertical lines for 1-sigma, 2-sigma, and 3-sigma
    for i in range(1, 4):
        plt.axvline(mean + i*sigma, color='green', linestyle='dashed', linewidth=1)
        plt.axvline(mean - i*sigma, color='green', linestyle='dashed', linewidth=1)
    
    # Show the plot
    plt.show()
    
    
    #%% Create a figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # only if just plotting 1 vector
    # # Define the origin
    # origin = np.array([0, 0, 0])
    
    # # Plot the vector
    # # normalizes it to an unit vector
    # # ax.quiver(*origin, *vector, length=1.0, normalize=True)
    # ax.quiver(*origin, *vector)
    
    # Define the origin points (optional, here they start at (0,0,0))
    origins = np.zeros_like(vectors)

    # Separate the components of the vectors
    X, Y, Z = origins[:, 0], origins[:, 1], origins[:, 2]
    U, V, W = vectors[:, 0], vectors[:, 1], vectors[:, 2]
    
    # Define colors
    colors = np.linalg.norm(vectors, axis=1)  # Color by vector magnitude
        
    # Plot the vectors
    ax.quiver(X, Y, Z, U, V, W, cmap='viridis', array=colors)
    # ax.quiver(X, Y, Z, U, V, W)
    
    # Set the limits of the plot
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    ax.set_zlim([0, 5])
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Show the plot
    plt.show()
    
    