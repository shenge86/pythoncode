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

class Particle:
    """
    Represents a particle with a position and velocity in 2D space.
    """

    def __init__(self, position=(0.0, 0.0), velocity=(0.0, 0.0), radius=0.02):
        """
        Initializes a Particle object.

        Args:
            position (tuple): A tuple representing the (x, y) coordinates of the particle's position.
                              Defaults to (0.0, 0.0).
            velocity (tuple): A tuple representing the (vx, vy) components of the particle's velocity.
                              Defaults to (0.0, 0.0).
        """
        self.position = list(position)  # Store as a list to allow modification
        self.velocity = list(velocity)  # Store as a list to allow modification
        self.radius    = radius

    def update(self, delta_time, bounds):
        """
        Updates the particle's state based on its velocity and a given time step.

        Args:
            delta_time (float): The time interval over which to update the position.
        """
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        
        # Bounce on x walls
        if self.position[0] - self.radius < bounds[0] or self.position[0] + self.radius > bounds[1]:
            self.velocity[0] *= -1 # reverse velocity in x-direction
            self.position[0] = np.clip(self.position[0], bounds[0] + self.radius, bounds[1] - self.radius)
        
        # Bounce on y walls
        if self.position[1] - self.radius < bounds[2] or self.position[1] + self.radius > bounds[3]:
            self.velocity[1] *= -1
            self.position[1] = np.clip(self.position[1], bounds[2] + self.radius, bounds[3] - self.radius)

    @property
    def get_position(self):
        """
        Returns the current position of the particle.

        Returns:
            tuple: The (x, y, z) coordinates of the particle's position.
        """
        return tuple(self.position)
    
    @property
    def x(self):
        return self.get_position[0]
    
    @property
    def y(self):
        return self.get_position[1]

    @property
    def get_velocity(self):
        """
        Returns the current velocity of the particle.

        Returns:
            tuple: The (vx, vy, vz) components of the particle's velocity.
        """
        return tuple(self.velocity)

    @property
    def vx(self):
        return self.get_velocity[0]
    
    @property
    def vy(self):
        return self.get_velocity[1]

    def set_velocity(self, new_velocity):
        """
        Sets a new velocity for the particle.

        Args:
            new_velocity (tuple): A tuple representing the new (vx, vy, vz) components of the velocity.
        """
        if len(new_velocity) == len(self.velocity):
            self.velocity = list(new_velocity)
        else:
            raise ValueError("New velocity must have the same dimensions as current velocity.")

    def __str__(self):
        """
        Returns a string representation of the Particle object.
        """
        return f"Particle(position={self.position}, velocity={self.velocity})"


if __name__ == '__main__':
    global cell_size
    
    # Define the simulation parameters
    num_particles = 50  # Number of particles
    cell_size = 10.0   # Size of the square cell
    bounds = (0, cell_size, 0, cell_size) # (xmin, xmax, ymin, ymax)
    dt = 0.1         # Time step
    
    #####################################
    #### NON-CLASS VERSION (use only for simplistic non-collision or non-attraction case)
    # Initialize particle positions and velocities randomly within the cell
    # x, y positions within [0, cell_size)
    # # vx, vy velocities within [-0.5, 0.5)
    # positions = cell_size * np.random.rand(num_particles, 2)
    # velocities = (np.random.rand(num_particles, 2) - 0.5) / 5
    
    # # Function to update particle positions and handle boundary conditions
    # def update_particles():
    #     global positions, velocities
    
    #     # Update positions based on velocities
    #     positions += velocities * dt
    
    #     # Handle boundary conditions (bouncing off walls)
    #     # If a particle hits a wall, reverse its velocity component
    #     positions[positions < 0] = 0  # Restrict particles to stay within the cell
    #     positions[positions > cell_size] = cell_size
    #     velocities[positions == 0] *= -1
    #     velocities[positions == cell_size] *= -1
    
    
    # # Create the plot for visualization
    plt.close('all')
    fig, ax = plt.subplots()
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.set_aspect('equal')
    ax.set_title("Bouncing Dancers")
    
    # # Plot the particles as red dots
    # particles_plot, = ax.plot(positions[:, 0], positions[:, 1], 'ro', markersize=4)
    #####################################
    particle0 = Particle(position=(5,5), velocity=(1,1), radius=0.03)
    particle1 = Particle(position=(5,5), velocity=(1,-1), radius=0.03)
    
    particles = [particle0, particle1]
    
    particles_plot = ax.scatter([p.x for p in particles], [p.y for p in particles], s=200)
    
    # Function to animate the particle movement
    def animate(frame):
        # for non-class version
        # update_particles()
        # particles_plot.set_data(positions[:, 0], positions[:, 1]) # use for line plots
        
        # class version
        for p in particles:
            p.update(dt, bounds)
        
        particles_plot.set_offsets([(p.x, p.y) for p in particles]) # use for scatter plots
        
        return particles_plot,
    
    # Create the animation
    animation = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
    
    plt.show()
    
    # save as mp4
    FFwriter = FFMpegWriter(fps=10)
    animation.save('dancingparticles.mp4', writer = FFwriter)