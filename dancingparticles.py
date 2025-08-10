# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 19:21:52 2025

@author: Shen Ge
@name: Dancing Particles
@description:
    
    This code is supposed to simulate ecstatic dancers starting with some random initial conditions and then bouncing around.
    Behavior of particles can be continually improved.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

# Define the simulation parameters
num_particles = 50  # Number of particles
cell_size = 10.0   # Size of the square cell
dt = 0.1         # Time step

# Initialize particle positions and velocities randomly within the cell
# x, y positions within [0, cell_size)
# vx, vy velocities within [-0.5, 0.5)
positions = cell_size * np.random.rand(num_particles, 2)
velocities = (np.random.rand(num_particles, 2) - 0.5) / 5

# Function to update particle positions and handle boundary conditions
def update_particles():
    global positions, velocities

    # Update positions based on velocities
    positions += velocities * dt

    # Handle boundary conditions (bouncing off walls)
    # If a particle hits a wall, reverse its velocity component
    positions[positions < 0] = 0  # Restrict particles to stay within the cell
    positions[positions > cell_size] = cell_size
    velocities[positions == 0] *= -1
    velocities[positions == cell_size] *= -1


# Create the plot for visualization
fig, ax = plt.subplots()
ax.set_xlim(0, cell_size)
ax.set_ylim(0, cell_size)

# Plot the particles as red dots
particles_plot, = ax.plot(positions[:, 0], positions[:, 1], 'ro', markersize=4)

# Function to animate the particle movement
def animate(frame):
    update_particles()
    particles_plot.set_data(positions[:, 0], positions[:, 1])
    return particles_plot,

# Create the animation
animation = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)

plt.show()

# save as mp4
FFwriter = FFMpegWriter(fps=10)
animation.save('dancingparticles.mp4', writer = FFwriter)