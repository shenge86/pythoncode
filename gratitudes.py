# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:24:30 2024

@author: Shen
@name: Friends and Gratitudes
@description:
    
    Gratitudes
"""
import numpy as np

class Friend:
    num_instances = 0
    def __init__(self, name, affiliation='Unknown', onlist=False, phone=0):
        type(self).num_instances += 1
        self.name  = name        
        self.affiliation = affiliation
        self.onlist = onlist
        
        self._phone = phone

    # Add a __str__ method to print info about the object
    def __str__(self):
        return f"Name: {self.name}, \
                Affiliation: {self.affiliation}, \
                Onlist: {self.onlist} \
                Phone: {self.phone} "
        
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value):
      if not isinstance(value, int) or value < 0:
          raise ValueError("Phone must be a positive integer.")
      self._phone = value

if __name__ == '__main__':
    print('Friendship list...')
    friends = []
    friends.append(Friend('Justin Yeung', 'Body and Brain', True))
    
    for friend in friends:
        print(friend)