'''
Chinese test
'''

words = {100: ('接种','vaccinate'),
         101: ('阴性','negative(medical)'),
         111: ('甲状','thyroid'),
         124: ('关节炎','arthritis'),
         186: ('短语','phrase')}

if __name__ == '__main__':
    for key,value in words.items():
        print('{} | {:口<10} | {}'.format(key,value[0],value[1]))
