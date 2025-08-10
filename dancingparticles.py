# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 19:21:52 2025

@author: Shen Ge
@name: Dancing Particles
@description:
    
    This code is supposed to simulate ecstatic dancers starting with some random initial conditions and then bouncing around.
    Behavior of particles can be continually improved.
    
@version:
    Future:
        1. Add restitution time (max time until 2 partners separate)
    
    August 9, 2025:
        Baseline version
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

#%%
class Particle:
    """
    Represents a particle with a position and velocity in 2D space.
    """

    def __init__(self, position=(0.0, 0.0), velocity=(0.0, 0.0), radius=0.02, soi=1.0, attractor=0.5, color='red', name='Shen'):
        """
        Initializes a Particle object.

        Args:
            position (tuple): A tuple representing the (x, y) coordinates of the particle's position.
                              Defaults to (0.0, 0.0).
            
            velocity (tuple): A tuple representing the (vx, vy) components of the particle's velocity.
                              Defaults to (0.0, 0.0).
                              
            radius (float): Radius to determine when it hits something
            
            soi (float): Sphere of influence where attractor applies
            
            attractor (float): attraction coefficient where positive values indicate that the particle attracts other particles
                               negative value means this particle repulses other particles
        """
        self.position = list(position)  # Store as a list to allow modification
        self.velocity = list(velocity)  # Store as a list to allow modification
        self.radius   = radius
        self.soi      = soi
        self.attractor= attractor
        self.color    = color
        self.name     = name # the human name if one exists

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

        # if stuck in a corner make sure you increase your velocity in correct direction to get away
        # dx = bounds[0] - self.position[0]
        # dy = bounds[2] - self.position[1]
        # dist_corner_left = np.hypot(dx, dy)
        # if (dist_corner_left <= (self.radius + 0.1)) and (self.velocity[0] < 0) and (self.velocity[1] < 0):
        #     self.velocity[0] = 10
        #     self.velocity[1] = 1

        # if velocity ever becomes too low reset velocity to a random value
        if self.get_speed < 1:
            self.velocity = np.random.uniform(-1, 1, 2) 

        # for debugging only:
        # print(self.name, self.x, self.y, self.vx, self.vy)
        
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
    def get_speed(self):
        """Returns the scalar speed"""
        return np.linalg.norm(self.velocity)

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

#%% particle interactions
def handle_particle_collisions(particles):
    '''
    The most basic is to just do collisions but of course we know real humans are not like this! :) 
    '''
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = particles[i], particles[j]
            dx = p2.position[0] - p1.position[0]
            dy = p2.position[1] - p1.position[1]
            dist = np.hypot(dx, dy) #equivalent to np.sqrt(dx**2 + dy**2)
            min_dist = p1.radius + p2.radius

            if dist < min_dist:  # collision detected
                # Normalize collision vector
                nx, ny = dx / dist, dy / dist

                # Relative velocity
                dvx = p1.velocity[0] - p2.velocity[0]
                dvy = p1.velocity[1] - p2.velocity[1]

                # Velocity along normal
                vn = dvx * nx + dvy * ny
                if vn > 0:
                    continue  # already moving apart

                # Elastic collision impulse
                p1.velocity[0] -= vn * nx
                p1.velocity[1] -= vn * ny
                p2.velocity[0] += vn * nx
                p2.velocity[1] += vn * ny

                # Push particles apart so they don't stick
                overlap = min_dist - dist
                p1.position[0] -= nx * overlap / 2
                p1.position[1] -= ny * overlap / 2
                p2.position[0] += nx * overlap / 2
                p2.position[1] += ny * overlap / 2

def handle_attractor(particles):
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = particles[i], particles[j]
            dx = p2.position[0] - p1.position[0]
            dy = p2.position[1] - p1.position[1]
            dist = np.hypot(dx, dy) #equivalent to np.sqrt(dx**2 + dy**2)
            
            # examine what happens due to particle 1 sphere of influence
            # attractor > 0 means it attracts
            if dist < p1.soi:
                # original_speed = p2.get_speed # uncomment if you do not want speed to change
                
                p2.velocity[0] = -(p2.position[0] - p1.position[0]) * p1.attractor
                p2.velocity[1] = -(p2.position[1] - p1.position[1]) * p1.attractor
                
                # change this velocity dramatically if stuck in a corner scenario
                
                # bottom left corner
                dx = bounds[0] - p2.position[0] # xmin difference
                dy = bounds[2] - p2.position[1] # ymin difference
                dist_corner_botleft = np.hypot(dx, dy)
                if (dist_corner_botleft <= (p2.radius + 0.1)) and (p2.velocity[0] < 0) and (p2.velocity[1] < 0):
                    p2.velocity[0] = 10
                    p2.velocity[1] = 1
                    
                # bottom right corner
                dx = bounds[1] - p2.position[0] # xmax difference
                dy = bounds[2] - p2.position[1] # ymin difference
                dist_corner_botright = np.hypot(dx, dy)
                if (dist_corner_botright <= (p2.radius + 0.1)) and (p2.velocity[0] > 0) and (p2.velocity[1] < 0):
                    p2.velocity[0] = -1
                    p2.velocity[1] = 10
                    
                # top right corner
                dx = bounds[1] - p2.position[0] # xmax difference
                dy = bounds[3] - p2.position[1] # ymax difference
                dist_corner_topright = np.hypot(dx, dy)
                if (dist_corner_topright <= (p2.radius + 0.1)) and (p2.velocity[0] > 0) and (p2.velocity[1] > 0):
                    p2.velocity[0] = -10
                    p2.velocity[1] = -10
                
                # uncomment if you do not want speed to change
                # normalize and multiply by original speed to get reasonable speed back
                # p2_speed = p2.get_speed # new speed
                # p2.velocity[0] = p2.velocity[0]/p2_speed * original_speed
                # p2.velocity[1] = p2.velocity[1]/p2_speed * original_speed
            
            # examine what happens due to particle 2 sphere of influence
            if dist < p2.soi:                
                p1.velocity[0] = -(p1.position[0] - p2.position[0]) * p2.attractor
                p1.velocity[1] = -(p1.position[1] - p2.position[1]) * p2.attractor
            

#%%
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
    particle0 = Particle(position=(5,5), velocity=(1,1), radius=0.03, soi=5.0, attractor=-0.5, color='red', name='Shen')
    particle1 = Particle(position=(5,9), velocity=(0.01,-0.01), radius=0.03, soi=3.0, attractor=0.3, color='blue', name='Eric')
    
    particles = [particle0, particle1]
    
    particles_plot = ax.scatter([p.x for p in particles], [p.y for p in particles], s=200, c=[p.color for p in particles])
    
    # Function to animate the particle movement
    def animate(frame):
        # for non-class version
        # update_particles()
        # particles_plot.set_data(positions[:, 0], positions[:, 1]) # use for line plots
        
        # class version
        for p in particles:
            p.update(dt, bounds)
        
        # handle_particle_collisions(particles) # simple particle collisions; do not use for realism
        handle_attractor(particles)
        
        particles_plot.set_offsets([(p.x, p.y) for p in particles]) # use for scatter plots
        
        return particles_plot,
    
    # Create the animation
    animation = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
    
    plt.show()
    
    # save as mp4
    FFwriter = FFMpegWriter(fps=10)
    animation.save('dancingparticles.mp4', writer = FFwriter)