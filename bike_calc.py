# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 09:49:42 2024

@author: Shen
@name: Bike Charge Accounting
"""
from decimal import Decimal

if __name__ == '__main__':
    print('''
    Hi Shen,
    
    We've determined with the assistance of our lead bike mechanic that you need a Gen3 Suspension fork assembly 
    which thankfully we do have. New parts and all.
    
    Our mechanic will build the fork assembly and front wheel assembly for you and can even put on the brake rotor 
    as soon as the invoice is paid. All other parts (front wheel assembly red, shimano gear shifter, brake rotor 180mm, 
    and front brake caliper& hose) are available.
    
    Due to the fact that two parts need to be built and we are shipping them separately, we will have to send two
    invoices. Unfortunately, I can not offer you a discount of any kind. We apologize for the delay in the availability of parts,
    I know you waited a few months.
    
    Additionally, some of the parts are showing as out of stock because we are doing a special deal for you so I 
    will need to call you and take payment over the phone. Please note that these invoices will be deleted in 7 days, 
    if it is not paid in 7 days the invoice process will start over and the price quote on this invoice may not be valid.
    
    I would like to know what day and time would be best to call you to take payment of invoices over the phone.
    
    
    Please do not hesitate to contact me if you have any further questions.
    Look forward to hearing from you.
    
    Kind regards,
    Hodo
    
    www.ArielRider.com
    ''')


    print(''' PARTS:
          
    Suspension Fork Assembly - $295.00+shipping
    Front Wheel Assembly- $95.00+shipping
    Shimano Gear Shifter - $15.00 +shipping
    Brake Rotor 180mm - $29.90+shipping
    Brake caliper w/ brake line - $75.00 +shipping
    ''')
    
    X_class_front_wheel  = Decimal('95.00')
    Shimano_gear_shifter = Decimal('15.00')
    brake_rotor          = Decimal('29.90')
    brake_caliper_hose   = Decimal('75.00')

    invoice_d7853 = X_class_front_wheel + Shimano_gear_shifter + brake_rotor + brake_caliper_hose
    
    suspension_fork_assembly = Decimal('295.00')
    
    invoice_d7854 = suspension_fork_assembly
    
    