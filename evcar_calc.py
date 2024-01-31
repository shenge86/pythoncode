# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 23:48:21 2024

@author: Shen
@name: Electric Car vs Gas Car Cost Comparison
"""
from decimal import Decimal

def quantize(value):
    rounded_value = value.quantize(Decimal('0.01'))
    return rounded_value

if __name__ == '__main__':
    # EV CAR: Polestar 2 2024
    energy_total  = 82 # kWh
    mileage_total = 320 # miles
    
    costperkwh = input('Enter cost per kwh: ')
    
    if costperkwh in ['']:
        costperkwh =  Decimal('0.36') # dollars per kWh
    else:
        costperkwh = Decimal(costperkwh)
        
    print('Cost per energy ($/kwh): ', costperkwh)
    
    cost_total_polestar    = energy_total * costperkwh    
    costpermile_polestar   = cost_total_polestar / mileage_total # 9 cents per mile


    # Toyota Corolla
    gas_total     = Decimal('13.2') # gallons
    mileage_total = 383 # miles
    
    mpg           = mileage_total/gas_total # 29 miles per gallon
    
    costpergallon = input('Enter cost per gallon: ')
    
    if costpergallon in ['']:
        costpergallon = Decimal('2.80') # dollars per gallon
    else:
        costpergallon = Decimal(costpergallon)
    
    print('Cost per volume ($/gallon): ', costpergallon)
    
    cost_total_corolla  = gas_total * costpergallon
    costpermile_corolla = cost_total_corolla / mileage_total
    
    
    
    print('================================')    
    print('Polestar (dollars per mile): ', costpermile_polestar)
    print('Corolla  (dollars per mile): ', costpermile_corolla)
    
    
    ### COST EVERY WEEK 
    distance = 200 # miles
    print(f'COST PER WEEK IF RUNNING {distance} miles')    
    
    print('You can charge an electric vehicle for free in many places so your actual cost for EV for fuel is cheaper.')
    distance_free = 100 # use Volta charger for free
    print(f'For instance, let us assume that I charge about {distance_free} miles for free every week.')
    
    cost_polestar = quantize(costpermile_polestar * distance)
    print(f'Total cost of Polestar running {distance} miles: ${cost_polestar}')
    cost_polestar = quantize(costpermile_polestar * (distance-distance_free))
    print(f'Total cost of Polestar running {distance} miles with {distance_free} miles being free: ${cost_polestar}')
    
    cost_corolla = quantize(costpermile_corolla * distance)
    
    print(f'Total cost of Corolla running {distance} miles: ${cost_corolla}')
    
    print('Polestar is this much cheaper for same distance as Corolla: $', cost_corolla - cost_polestar)