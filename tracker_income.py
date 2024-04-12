# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:58:37 2024

@author: Shen
@name: Venmo payments
"""
from decimal import Decimal

#%%
if __name__ == '__main__':
    print('Calculate total income from tutoring, radio and other miscellaneous ones.')
    
    income_yasminkazzaz = {'jan08': Decimal('65.00'),
                           'jan15': Decimal('65.00'),
                           'jan22': Decimal('65.00'),
                           'feb12': Decimal('130.00'),
                           'feb19': Decimal('65.00'),
                           'feb26': Decimal('65.00'),
                           'mar05': Decimal('65.00'),
                           'mar26': Decimal('65.00'),
                           'apr02': Decimal('65.00'),
                           'apr16': Decimal('65.00'),
                           'apr23': Decimal('65.00'),
                           'apr30': Decimal('146.25'),
                           'may14': Decimal('65.00'),
                           'jun11': Decimal('65.00'),
                           'jun25': Decimal('65.00'),
                           'sep10': Decimal('65.00'),
                           'oct01': Decimal('65.00'),
                           'oct22': Decimal('65.00'),
                           'nov05': Decimal('65.00'),
                           'nov12': Decimal('65.00'),
                           'dec03': Decimal('65.00'),
                           'dec10': Decimal('65.00'),
                           'dec17': Decimal('65.00'),
                           }
    
    income_elizabethlane = {'feb18': Decimal('130.00'),
                            'mar21': Decimal('81.25'),
                            'may13': Decimal('97.50'),
                            }
    
    income_tarawray = {'jun10': Decimal('65.00'),
                       }
    
    income_cathyhughes = {'sep10': Decimal('70.00'),
                          'sep17': Decimal('70.00'),
                          'sep24': Decimal('70.00'),
                          'oct01': Decimal('70.00'),
                          'oct09': Decimal('70.00'),
                          }
    
    # zelle
    income_rebeccawagley = {'mar09': Decimal('65.00')}
    
    # zelle
    income_courtneymunoz = {'oct19': Decimal('70.00')}
    
    # patreon (will have to fill out W9 if >$600 in income)
    income_sg2onspace = {'jan': Decimal('2.60'),
                         'feb': Decimal('5.20'),
                         'mar': Decimal('5.20'),
                         'apr': Decimal('5.20'),
                         'may': Decimal('5.20'),
                         'jun': Decimal('5.20'),
                         'jul': Decimal('5.20'),
                         'aug': Decimal('5.20'),
                         'sep': Decimal('5.20'),
                         'oct': Decimal('5.20'),
                         'nov': Decimal('5.20'),
                         'dec': Decimal('7.80'),
                         }
    
    income_misc = {'apr03': Decimal('25.00'),
                   }
    
    income_yasminkazzaz_total = sum(income_yasminkazzaz.values())
    income_elizabethlane_total= sum(income_elizabethlane.values())
    income_tarawray_total     = sum(income_tarawray.values())
    income_cathyhughes_total  = sum(income_cathyhughes.values())
    income_rebeccawagley_total= sum(income_rebeccawagley.values())
    income_courtneymunoz_total= sum(income_courtneymunoz.values())
    income_sg2onspace_total   = sum(income_sg2onspace.values())
    income_misc_total         = sum(income_misc.values())
    
    # print('Yasmin Kazzaz income ($): ', income_yasminkazzaz_total)
    # print('Elizabeth Lane income($): ', income_elizabethlane_total)
    # print('Miscellaneous income ($): ', income_misc_total)
    
    #%%
    variables = locals()
    word_to_find = '_total'
    matching_variables = [var_name for var_name in variables if var_name.endswith(word_to_find)]
    
    # total = income_yasminkazzaz_total + income_elizabethlane_total + income_tarawray_total + income_cathyhughes_total + income_misc_total
    
    total = 0
    for x in matching_variables:
        print(f'{x}: {globals()[x]}')
        total += globals()[x]
    
    print('Total ($): ', total)
    
    #%% Investments
    rothira_contributions = {'2014': Decimal('5000.00'),
                             '2018': Decimal('2000.00'),
                             '2019': Decimal('6000.00'),
                             '2020': Decimal('6000.00'),
                             '2021': Decimal('6000.00'),
                             '2022': Decimal('6000.00'),
                             '2023': Decimal('6500.00')
                             }
    
    rothira_contributions_sum = sum(rothira_contributions.values())
    print("Roth IRA ($): ", rothira_contributions_sum)