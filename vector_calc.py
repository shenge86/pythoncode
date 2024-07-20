# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:54:48 2024

@author: Shen Ge
@name: Vector Calculator
@description:
    
    Plots out different vectors according to specifications.
    Vector is summation of lateral (along the nominal vector direction) and transverse direction (perpendicular to nominal vector).
    
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

class Circle:
    num_instances = 0
    def __init__(self, center, radius, a, b, num_interpol=50):
        type(self).num_instances += 1
        self.center       = center
        self.radius       = radius
        self.a            = a # vector that defines one axes in 3D space which circle lies on
        self.b            = b # vector that defines another axes in 3D space which circle lies on
        self.num_interpol = num_interpol
        
        # create the circle coordinates
        self.x_theta, self.y_theta, self.z_theta = self.create_coordinates()
        self.coordinates = np.column_stack((self.x_theta, self.y_theta, self.z_theta))
        self.coordinates_magnitudes = np.linalg.norm(self.coordinates, axis=1)
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self,value):
        if not isinstance(value, int | float) or value <= 0:
            raise ValueError("positive number expected")
        self._radius = value

    def create_coordinates(self):
        c1, c2, c3 = self.center
        a1, a2, a3 = self.a
        b1, b2, b3 = self.b
        x_theta = np.zeros(self.num_interpol)
        y_theta = np.zeros(self.num_interpol)
        z_theta = np.zeros(self.num_interpol)
        
        for i,theta in enumerate(np.linspace(0,2*np.pi,self.num_interpol)):
            x_theta[i] = c1 + self.radius*np.cos(theta)*a1 + self.radius*np.sin(theta)*b1
            y_theta[i] = c2 + self.radius*np.cos(theta)*a2 + self.radius*np.sin(theta)*b2
            z_theta[i] = c3 + self.radius*np.cos(theta)*a3 + self.radius*np.sin(theta)*b3
        
        return x_theta, y_theta, z_theta

    def confirm_coordinates(self, magnitudetocheck):        
        deltas = self.coordinates_magnitudes - magnitudetocheck
        print('Difference between this magnitude and the magnitude to check: ', deltas)
        for delta in deltas:
            assert(np.allclose(delta, 0))
            
        return None

if __name__ == '__main__':    
    # Define the vector components
    # vector = np.array([3, 4, 5])
    vector = np.array([10, 0, 0])
    
    # Create another vector in same direction with different length (magnitude)
    mean = np.linalg.norm(vector)
    vector_unit = vector / mean
    
    # number of randomized vectors
    if '-n' in sys.argv:
        n = sys.argv[sys.argv.index('-n') + 1]
    else:
        n = input('Enter number of randomized vectors to use: ')
    n = int(n)
    
    if '-o' in sys.argv:
        output = sys.argv[sys.argv.index('-o') + 1]
    else:
        output = input('Enter file name of output: ')
    
    if output[-4:] != '.npy':
        print('Appending .npy extension to file')
        output += '.npy'
        
    if '-display' in sys.argv:
        display = True
    else:
        display = False
        
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
    if display:
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
    
    #%% Now add transverse direction
    ################################
    threesigma_transpose = 9.0
    sigma = threesigma_transpose/3
    print('Creating transverse fixed magnitude offsets with three sigma: ', threesigma_transpose)
    
    ## create 2 axes on a plane perpendicular to unit vector (nominal)
    u1,u2,u3 = vector_unit
    
    if u3 != 0:
        # solution when solving dot product a dot u = 0 and assuming a1 = a2 = 1
        a1, a2   = 1,1
        a3       = -(u1+u2)/u3
    else:
        # this will mean z-axis of original vector is 0. It is flat on x-y plane
        # set a vector to be just the z-axis
        a1, a2 = 0, 0
        a3 = 1
    
    # normalize a and apply cross product to get both axes of this plane which circle lies
    a      = np.array([a1,a2,a3])
    a_unit = a / np.linalg.norm(a)
    b      = np.cross(a_unit, vector_unit)
    b1, b2, b3 = b
    
    ## generate randomized magnitude based on 3 sigma distribution
    # absolute value is needed since otherwise might be negative
    rs = np.abs(np.random.normal(0, sigma, n))
    
    #%%
    circles = [] # empty list to be populated with circle objects
    for (vector_lateral, r) in zip(vectors, rs):    
        print('Initial vector along nominal vector direction (before adding transverse component: ', vector_lateral)            
        print('Radius: ', r)
        
        circle0 = Circle(vector_lateral,r,a,b)
        x_theta, y_theta, z_theta = circle0.create_coordinates()
        
        # need to add unit test here to calculate distance to the end vector
        # see if it adds up to a constant value
        print('Test to see distance to end vector add up the same value.')
        # check magnitudes
        vector_lateral_magnitude = np.linalg.norm(vector_lateral)
        magnitudetocheck = np.sqrt(vector_lateral_magnitude**2 + r**2)
        
        circle0.confirm_coordinates(magnitudetocheck)
        
        circles.append(circle0)

    #%% add the tranverse part to the lateral part
    
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
    
    # Plot circle of points (only for tests!!)
    for circle in circles:
        ax.scatter(circle.x_theta,circle.y_theta,circle.z_theta,c='r',marker='o')
    
    # Set the limits of the plot. Plus 1 to make sure not zero
    ax.set_xlim([0, max(vectors[:,0])+1])
    ax.set_ylim([0, max(vectors[:,1])+1])
    ax.set_zlim([0, max(vectors[:,2])+1])
    
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
        