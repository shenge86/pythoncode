'''
Chinese test
'''
words190 = {'Pronouniciation': ('Túbù lǚxíng',''),
            'Example 1': ('她自己喜欢徒步旅行和骑自行车长途旅行这样的运动方式。','Her own preferred methods of exercise are hiking and long cycle rides.'),
            'Example 2': ('他们做了一次穿越森林的十英里徒步旅行。','They went on a ten-mile hike through the forest.')}

words = {100: ('接种','vaccinate'),
         101: ('阴性','negative(medical)'),
         111: ('甲状','thyroid'),
         124: ('关节炎','arthritis'),
         186: ('短语','phrase'),
         187: ('顺时针','clockwise'),
         188: ('逆时针','counterclockwise'),
         189: ('远足','hiking'),
         190: ('徒步旅行','trekking',words190),
         191: ('贬义词','derogatory term'),
         1000: ('旧地重游','Revisit a familiar place; return to old haunts'),
         1001: ('物是人非','The scenery remains the same but the people are changed. Things are unchanged but the people are gone.'),
         1002: ('劳逸结合','Strike a proper balance between work and rest.'),
         1003: ('劳逸不均','Uneven allocation of work and rest.'),
         2000: ('赵大妈','Person who goes around and gets into other people\'s business. Loves to talk to people.')}



if __name__ == '__main__':
    print('Chinese Dictionary Tester')
    print('If you see blanks please type as follows in command line: ')
    print('chcp 936')
    for key,value in words.items():
        print('{:<5} | {:口<10} | {}'.format(key,value[0],value[1]))
        if len(value) > 2:
            for k,v in value[2].items():
                print(k+': ')
                print(v[0])
                print(v[1])
            print('===================================================')
