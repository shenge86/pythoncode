'''
Chinese test
'''

words = {100: ('接种','vaccinate'),
         101: ('阴性','negative(medical)'),
         111: ('甲状','thyroid'),
         124: ('关节炎','arthritis'),
         186: ('短语','phrase'),
         187: ('顺时针','clockwise'),
         188: ('逆时针','counterclockwise')}

if __name__ == '__main__':
    print('Chinese Dictionary Tester')
    print('If you see blanks please type as follows in command line: ')
    print('chcp 936')
    for key,value in words.items():
        print('{} | {:口<10} | {}'.format(key,value[0],value[1]))
