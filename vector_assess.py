# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:43:14 2024

@author: Shen
@name: Vector Analyze
@description:
    
    Assesses the vector distribution already generated.
"""
import os, sys

import numpy as np


if __name__ == '__main__':
    try:
        output = sys.argv[1]
    except:
        output = input('Enter numpy file to ingest: ')
        
    if output[-4:] != '.npy':
        print('Appending .npy extension to file')
        output += '.npy'
        
    with open('output_vectors/'+output,'rb') as f:
        vector  = np.load(f)
        vectors = np.load(f)
        vectors_fixedoffset = np.load(f)
        vectors_proportionaloffset = np.load(f)
        
    for (v, vf, vp) in zip(vectors, vectors_fixedoffset, vectors_proportionaloffset):
        v_test = vector + vf + vp
        print('vector (nominal) + fixed offset + proportional offset: ', v_test)
        print('dispersed vector: ', v)
        print('Difference between the two: ', v_test - v)
        assert np.allclose(v_test*2,v,atol=1e-6)