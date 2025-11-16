# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 19:45:04 2025

@author: sheng
@name: Image Caption Test 
@description:
    
    Uses pytorch and transformers (hugging face) to identify an image and print caption
"""

import os, sys

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

LOGFILE = 'images/imagecaptions.txt'

#%% image analyzer
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


#%% file manager
class Tee:
    def __init__(self, filename):
        self.file = open(filename, "a") # append instead of overwrite
        self.console = sys.stdout

    def write(self, msg):
        self.console.write(msg)
        self.file.write(msg)

    def flush(self):
        self.console.flush()
        self.file.flush()

if __name__ == '__main__':
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
    
    
    # sys.stdout = open('images/imagecaptions.txt', 'w')
    sys.stdout = Tee(LOGFILE)
    folder = "images"
    # img = Image.open("images/sailor.jpg").convert("RGB")
    
    for filename in os.listdir(folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder, filename)
            
            if img_path in logged_paths:
                sys.__stdout__.write(f'Image already analyzed: {img_path}\n') # do this to only print on console
                continue
           
            print('Opening: ', img_path)
            img = Image.open(img_path)
            
            inputs = processor(img, return_tensors="pt")
            out = model.generate(**inputs)
            print(processor.decode(out[0], skip_special_tokens=True))
            
    # Restore stdout if needed
    # sys.stdout.close()
    sys.stdout = sys.__stdout__
    print('DONE')