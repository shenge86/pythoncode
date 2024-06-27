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

#%%
if __name__ == '__main__':
    
    # Define the vector components
    vector = np.array([3, 4, 5])
    
    # Create a figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Define the origin
    origin = np.array([0, 0, 0])
    
    # Plot the vector
    # normalizes it to an unit vector
    # ax.quiver(*origin, *vector, length=1.0, normalize=True)
    ax.quiver(*origin, *vector)
    
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
