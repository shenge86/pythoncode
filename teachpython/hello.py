# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:46:39 2026

@author: Shen Ge

This code demonstrates some simple functionalities of Python.

Three objectives:
    
    1. Learn the basic building structures (materials) aka variables.
    2. Learn how to manipulate the building structures aka
       conditional statements (if else), looping (while or for)
    3. Learn how to package them into sensible rooms aka
       functions or classes
    4. Learn some common libraries aka
       numpy, pandas

To do before arrival:
    
    1. Create a worksheet with basic definitions and examples.
    2. Give practice problems.
    3. Get this on your computer before arriving.
    Go to https://www.anaconda.com/download for full set
    or go here for a minimal install
    https://www.anaconda.com/docs/getting-started/miniconda/install#windows-command-prompt

"""
print("hello world")

natalia_msg = 'hello natalia'

raining = False
if raining is True:
    walk = False
else:
    walk = True
    
print('Raining: ', raining)
print('Walking: ', walk)

age = 37
age2 = 38
coffeeprice = 1.50

# TYPES
print('Types for the different variables: ')
print('natalia_msg', type(natalia_msg))
print('raining', type(raining))
print('walk', type(walk))
print('age', type(age))
print('coffeeprice', type(coffeeprice))

agestr = "37"

print(age * 2)
print(agestr * 2)

print(age + age2)

# Typecast agestr so that we can add it to int age please! hklhlhlhkhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
print(age + int(agestr)) # integer
# Typecast age into string
print(str(age) + agestr) # string

print('Shen is awesome')

# LOOPS
# Hit control + C to terminate a program
age = 0
while age < 21:
    print('Age: ', age)
    print('You are not allowed into this place.')
    age = age + 1
    
color_list = ['yellow', 'red', 'green', 'blue', 'black']
color_test = ['purple', 'cyan', 'red', 'blue', 'magenta']

# This is called a list
print(type(color_list))
print(type(color_test))

color = color_test[0]
firstletterofcolor = color[0]
print(color)
print(firstletterofcolor)

print(color_test[0])
print(color_test[1])
print(color_test[2])

index = 0
while color not in color_list:
    print('Index: ', index)
    print('Color: ', color)
    print('Your color is not in the list')
    index = index + 1
    color = color_test[index]
    
print('Your color is found!')
print('Index: ', index)
print('Color: ', color)