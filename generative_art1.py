# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 00:09:40 2025

@author: sge
@name: Random line generator
@description:
    
    Inspired by this article 
    https://towardsdatascience.com/how-i-created-generative-art-with-python-that-10000-dall-e-credits-could-not-buy-fcf804b61437/
    
    Similar style to artist
    Roman Haubenstock-Ramati
"""

import torch
from PIL import Image, ImageDraw

if __name__ == '__main__':
    # Setting the size of the canvas
    canvas_size = 1000
    
    # Number of lines
    num_lines = 10
    
    # Create distributions for start and end y-coordinates and x-coordinate
    y_start_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
    y_end_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
    x_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
    
    # Sample from the distributions for each line
    y_start_points = y_start_distribution.sample((num_lines,))
    y_end_points = y_end_distribution.sample((num_lines,))
    x_points = x_distribution.sample((num_lines,))
    
    # Create a white canvas
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw the lines
    for i in range(num_lines):
        draw.line([(x_points[i], y_start_points[i]), (x_points[i], y_end_points[i])], fill='black')
    
    for i in range(5):
        # Creating normal distributions to sample from
        start_y_dist = torch.distributions.Normal(canvas_size * 0.5, canvas_size * 0.2)
        start_y = int(start_y_dist.sample())
     
        height_dist = torch.distributions.Normal(canvas_size * 0.2, canvas_size * 0.05)
        height = int(height_dist.sample())
        end_y = start_y + height
     
        start_x = int(x_distribution.sample())
        width_dist = torch.distributions.Normal(height * 0.5, height * 0.1)
        width = int(width_dist.sample())
        end_x = start_x + width
     
        # print(start_x)
        # print(start_y)
        # print(end_x)
        # print(end_y)
        # Drawing the rectangle
        draw.rectangle([(start_x, start_y), (end_x, end_y)], outline='black')
    
    # Display the image
    image.show()