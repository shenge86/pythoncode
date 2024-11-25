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

    @property
    def onlist_bool(self):
        return "True" if self.onlist else "False"

def return_bool(value):
    return "True" if value else "False"

if __name__ == '__main__':
    print('Friendship list...')
    friends = []
    friends.append(Friend('Justin Yeung', 'UT Health MPH Student', True))
    friends.append(Friend('Ben ?', 'Nurse', True))
    friends.append(Friend('John Graves', 'Intuitive Machines', True))
    friends.append(Friend('Evan Zeigmann', 'St. Thomas counselor student', True))
    friends.append(Friend('Megan Finkel', 'Indiana University Russian Slavic Studies PhD student', True))
    friends.append(Friend('Lindsay Nichols', '?', True))
    friends.append(Friend('Gina Lowry', 'Former teacher; now seeking assistant principal position', True))
    friends.append(Friend('Alicia Baker', 'Jacobs / NASA', True))
    friends.append(Friend('Jim Boyd', 'Intuitive Machines', True))
    friends.append(Friend('Sam Welsh', 'Intuitive Machines', True))
    friends.append(Friend('Michelle Free', '?', True))
    friends.append(Friend('Jim Temple', 'Retired', True))
    friends.append(Friend('Shen Ge', 'Intuitive Machines', True, 8328082371))
    friends.append(Friend('Melissa Hong Ge', '?', True))
    friends.append(Friend('Yongfu Ge', '?'))
    
    print(f"{'Name':<20} {'Affiliation':<60} {'Onlist':10} {'Phone':<9}")
    for friend in friends:
        boolvalue = return_bool(friend.onlist)
        print(f"{friend.name:<20} {friend.affiliation:<60} {friend.onlist_bool:10} {friend.phone:<9}")
        # print(friend)