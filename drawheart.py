# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 22:37:03 2025

@author: sheng
@name: Heart draw
"""

import matplotlib.pyplot as plt
import numpy as np

# Create an array of theta values from 0 to 2*pi
t = np.arange(0, 2 * np.pi, 0.1) # t = np.linspace(0, 2 * np.pi, 1000)

# Parametric equations for the x and y coordinates of the heart
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, color='red', linewidth=2)

# Remove the axis ticks and spines
plt.xticks([])
plt.yticks([])
plt.axis('off')

# Add the equation to the figure using LaTeX formatting
# We use a raw string (r"...") so that backslashes are not interpreted as escape characters.
equation = r"$x = 16\sin^3(t)$" + "\n" + r"$y = 13\cos(t) - 5\cos(2t) - 2\cos(3t) - \cos(4t)$"
plt.text(0, -20, equation, ha='center', fontsize=12, color='black')

plt.savefig('heart.png')

# Display the plot
plt.show()