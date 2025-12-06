# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 00:43:28 2025

@author: sheng
@name: Image Identification Test
@description:
    
    Use tensorflow / keras to identify image
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions

#%%
# Load the pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

if __name__ == '__main__':
    new_lines = []
    LOGFILE = 'images/imagecaptions2.txt'
    folder = "images"
    # ---------------------------
    # Step 1 — Load existing entries
    # ---------------------------
    logged_paths = set()
    if os.path.exists(LOGFILE):
        with open(LOGFILE, "r") as f:
            for line in f:
                if line.startswith("Opening:"):
                    # Extract the path after "Opening: "
                    path = line.split("Opening:")[1].strip()
                    logged_paths.add(path)
    
    # ---------------------------
    # Step 2 — Loop and analyze
    # ---------------------------
    for filename in os.listdir(folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder, filename)
            
            if img_path in logged_paths:
                print(f'SKIPPING! Image already analyzed: {img_path}\n')
                continue
            else:
                print('Assessing: ', img_path)
        # Path to the input image
        # img_path = 'images/palm-tree-1.jpg' # The image to classify
        new_lines.append('Opening: '+img_path+'\n')
        
        # Load the image
        img = cv2.imread(img_path)
        
        # Preprocess the image
        img = cv2.resize(img, (224, 224)) # Resize the image to match the model's input size
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0) # Add a batch dimension
        x = preprocess_input(x)
        
        # Make predictions
        preds = model.predict(x)
                
        # Decode and display predictions
        my_list = decode_predictions(preds, top=3)[0]
        newline = "\n".join(str(t) for t in my_list)
        new_lines.append(newline)
        new_lines.append('\n')
    
    #%% write to text
    if os.path.exists(LOGFILE):
        print('Log file exists. Will append.')
        with open(LOGFILE,'a') as f:
            for line in new_lines:
                f.write(line)
    else:
        with open(LOGFILE,'w') as f:
            for line in new_lines:
                f.write(line)
    
    # try:
    #     with open(LOGFILE, "r") as f:
    #         existing = set(f.readlines())
    # except FileNotFoundError:
    #     existing = set()
    
    # # do not write duplicates
    # with open(LOGFILE,'w') as f:
    #     for line in new_lines:
    #         if line not in existing:
    #             f.write(line)
