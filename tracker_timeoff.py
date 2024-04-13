# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:50:47 2024

@author: Shen
@name: Time Off Calculator
@description: 
    Calculates how much time I have left dependent on what is being used so far
"""
from datetime import timedelta

#%%
if __name__ == '__main__':
    PTO = {'jan10': timedelta(hours=8,minutes=30),
           'jan22': timedelta(hours=4,minutes=15),
           'feb09': timedelta(hours=6,minutes=59),
           'feb26': timedelta(hours=12,minutes=21),
           'mar05': timedelta(hours=16),
           'mar08': timedelta(minutes=36),
           'mar11': timedelta(hours=4),
           'mar12': timedelta(hours=4),
           'mar20': timedelta(hours=1,minutes=42),
           'mar21': timedelta(hours=8),
           'apr02': timedelta(hours=3,minutes=30),
           'apr08': timedelta(hours=8),
           'apr10': timedelta(hours=8),
           }
    
    PTO_sum = 0 # seconds
    
    # for value in PTO.values():
    for key,value in PTO.items():
        PTO_sum += value.seconds
        if PTO_sum/3600 > 240:
            print('Warning! You have went over the 240 hours (aka 6 weeks or 30 days) allocated for paid time off!!')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        elif PTO_sum/3600 > 200:
            print('You have used 5 weeks of vacation time! Cutting it close!')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        elif PTO_sum/3600 > 160:
            print('You used up 4 weeks of vacation time.')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        elif PTO_sum/3600 > 120:
            print('You used up 3 weeks of vacation time. Halfway there!')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        elif PTO_sum/3600 > 80:
            print('You used up 2 weeks of vacation time.')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        elif PTO_sum/3600 > 40:
            print('You used up 1 week of vacation time.')
            print('Latest day: ', key)
            print('Latest hours used: ', value / timedelta(hours=1))
        
    print('Total seconds: ', PTO_sum)
    print('Total hours  : ', PTO_sum / 3600)