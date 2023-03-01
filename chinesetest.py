'''
Chinese test
'''
words190 = {'Pronouniciation': ('Túbù lǚxíng',''),
            'Example 1': ('她自己喜欢徒步旅行和骑自行车长途旅行这样的运动方式。','Her own preferred methods of exercise are hiking and long cycle rides.'),
            'Example 2': ('他们做了一次穿越森林的十英里徒步旅行。','They went on a ten-mile hike through the forest.')}

words192 = {'Alternative': ('吸脂',''),
            'Example 1': ('我想她做过吸脂手术和双眼皮手术。','I think she has had liposuction and double eyelid surgery.')}

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
         192: ('抽脂','liposuction',words192),
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

    print('Word Test! Any time you can type in give up to get the answer.')
    print('You can also type in quit to exit the program.')
    temp = iter(words)
    word_index = next(temp,None)
    while True:
        chooseword = input(f'Please type the Chinese for {words[word_index][1]}: ')
        if chooseword in ['give up']:
            print('Answer: ')
            print('{:<5} | {:口<10} | {}'.format(word_index,words[word_index][0],words[word_index][1]))
            if len(value) > 2:
                for k,v in value[2].items():
                    print(k+': ')
                    print(v[0])
                    print(v[1])
                print('===================================================')
            word_index = next(temp,None)
            continue
        elif chooseword in ['quit','q']:
            print('Quitting.')
            break
        elif chooseword not in [words[word_index][0]]:
            print('You are incorrect! Try again.')
            continue
        else:
            print('Correct! Moving to next word.')
            word_index = next(temp,None)
            continue
