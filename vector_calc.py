# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:54:48 2024

@author: Shen Ge
@name: Vector Calculator
@description:
    
    Plots out different vectors according to specifications.
    
@version:
    1.1
    Add transverse vectors
    
    1.0 
    Add translational vectors with distributions
"""

import os, sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__ == '__main__':    
    # Define the vector components
    vector = np.array([3, 4, 5])
    
    # Create another vector in same direction with different length (magnitude)
    mean = np.linalg.norm(vector)
    vector_unit = vector / mean
    
    try:
        n = sys.argv[1]
    except:
        # number of randomized vectors
        n = input('Enter number of randomized vectors to use: ')
    n = int(n)
    
    try:
        output = sys.argv[2]
    except:
        output = input('Enter file name of output: ')
    
    if output[-4:] != '.npy':
        print('Appending .npy extension to file')
        output += '.npy'
        
    output_folder = 'output_vectors'
    #%% Create fixed magnitude offsets (resolution error)
    threesigma = 1.5
    sigma      = threesigma/3    # this is a fixed magnitude
    
    print('Creating fixed magnitude offsets with three sigma: ', threesigma)
    
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
    threesigma_prop = 0.6
    sigma = threesigma_prop/3 # this multiplied by 100 is a percentage
    
    print('Creating proportional magnitude offsets with three sigma: ', threesigma_prop)
    
    vectors_proportional_magnitudes = np.random.normal(0, sigma, n)
    magnitude_proportional_matrix   = np.transpose(np.tile(vectors_proportional_magnitudes,(3,1)))

    # note this is NOT based on unit vector but the vector itself    
    vectors_proportionaloffset      = vector * magnitude_proportional_matrix
    
    #%% Now add transverse direction
    threesigma_transpose = 1.0
    sigma = threesigma_transpose/3
    print('Creating transverse fixed magnitude offsets with three sigma: ', threesigma_transpose)
    
    
    
    #%% Combined vector and histogram plot    
    vectors_totalerror = vectors_fixedoffset + vectors_proportionaloffset
    vectors            = vector + vectors_totalerror
    
    vectors_magnitudes = np.zeros(n)
    for i,v in enumerate(vectors):
        vectors_magnitudes[i] = np.linalg.norm(v)
    vectors_magnitudes_mean = np.mean(vectors_magnitudes)
    vectors_magnitudes_std  = np.std(vectors_magnitudes)
    
    # if only in-line, the unit vector direction should match with the original unit vector
    # the direction does not change so all unit vectors should match!
    for vi in vectors:
        vector_normalized = vi/np.linalg.norm(vi)
        print(vector_normalized)
        # assert np.array_equal(vector_normalized,vector_unit) # cannot do this since may have rounding errors
        assert np.allclose(vector_normalized,vector_unit,atol=1e-6)
    
    #%%
    # Create the histogram
    # plt.hist(vectors, bins=50, alpha=0.75, color='blue', edgecolor='black')
    plt.hist(vectors_magnitudes, bins=50, alpha=0.75)
    
    # Add labels and title
    plt.xlabel('Vector Magnitude')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Normal Distribution (3-Sigma)\nMean: {vectors_magnitudes_mean} / Std: {vectors_magnitudes_std}')
    
    # Add a vertical line for the mean
    # cannot use the original vector magnitude as mean since adding multiple distributions
    # changes what the mean of the combined distribution might be
    plt.axvline(vectors_magnitudes_mean, color='red', linestyle='dashed', linewidth=2)
    
    # Add vertical lines for 1-sigma, 2-sigma, and 3-sigma
    for i in range(1, 4):
        plt.axvline(vectors_magnitudes_mean + i*vectors_magnitudes_std, color='green', linestyle='dashed', linewidth=1)
        plt.axvline(vectors_magnitudes_mean - i*vectors_magnitudes_std, color='green', linestyle='dashed', linewidth=1)
    
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
    
    # if you show, you have to comment out show to be able to save
    # Save the plot
    # plt.savefig(output_folder + '/' + output[:-4] + '.png')
    
    #%% Save the numpy array for loading in future
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(output_folder + '/' + output,'wb') as f:
        np.save(f, vector)
        np.save(f, vectors)
        np.save(f, vectors_fixedoffset)
        np.save(f, vectors_proportionaloffset)
        