'''
Chinese test
'''
import random

words14 = {'Pronouniciation': ('Nàmèn',''),
           'Example 1': ('她开始纳闷他在搞什么鬼。','She began to wonder what he was playing at.'),
           'Example 2': ('我时常纳闷她为什么要那样对待我。','I often wonder about why she treated me like that.'),
           'Example 3': ('我纳闷为什么火鸡总是和感恩节连在一起呢?','I wonder why turkey seems to belong to Thanksgiving?')}

words122 = {'Example 1': ('咱们叫份外卖吧。','Let us get a takeout.'),
            'Example 2': ('我可以像纽约其他的康复病人一样叫外卖!','I can order delivery just like anyone else convalescing in New York!')}

words190 = {'Pronouniciation': ('Túbù lǚxíng',''),
            'Example 1': ('她自己喜欢徒步旅行和骑自行车长途旅行这样的运动方式。','Her own preferred methods of exercise are hiking and long cycle rides.'),
            'Example 2': ('他们做了一次穿越森林的十英里徒步旅行。','They went on a ten-mile hike through the forest.')}

words192 = {'Alternative': ('吸脂',''),
            'Example 1': ('我想她做过吸脂手术和双眼皮手术。','I think she has had liposuction and double eyelid surgery.')}

words195 = {'Example 1': ('The theory is too difficult to understand, can you elaborate on it?','这个理论太深奥了, 您能不能讲得通透一点?'),
            'Example 2': ('The sky was changing from translucent blue to thicker grey.','天空由通透的湛蓝色变成了暗灰色。')}

words5000= {'Details': ('伦敦西区（London\'s West End）是与纽约百老汇(Broadway)齐名的世界两大戏剧中心之一，是表演艺术的国际舞台，也是英国戏剧界的代名词。','在如此有限的区域内集中如此之多的剧院，在世界上只有纽约的百老汇可与之相比，而从历史传统来讲，西区要比百老汇悠久得多。')}

words = { 14: ('纳闷','wondered (in a perplexed way)',words14),
         100: ('接种','vaccinate'),
         101: ('阴性','negative(medical)'),
         102: ('义母','stepmother'),
         103: ('遗产','inheritance'),
         104: ('刻毒','spiteful'),
         105: ('百老汇','Broadway'),
         106: ('大厦','big building'),
         111: ('甲状','thyroid'),
         115: ('床单','bedsheet'),
         122: ('外卖','takeout',words122),
         124: ('关节炎','arthritis'),
         186: ('短语','phrase'),
         187: ('顺时针','clockwise'),
         188: ('逆时针','counterclockwise'),
         189: ('远足','hiking'),
         190: ('徒步旅行','trekking',words190),
         191: ('贬义词','derogatory term'),
         192: ('抽脂','liposuction',words192),
         193: ('地标','landmark'),
         194: ('壁画','mural'),
         195: ('通透','transparent'),
         1000: ('旧地重游','Revisit a familiar place; return to old haunts'),
         1001: ('物是人非','The scenery remains the same but the people are changed. Things are unchanged but the people are gone.'),
         1002: ('劳逸结合','Strike a proper balance between work and rest.'),
         1003: ('劳逸不均','Uneven allocation of work and rest.'),
         1004: ('损人利己','to harm others to benefit oneself; benefit oneself at the expense of others'),
         1005: ('损人不利己','to harm others without benefiting oneself'),
         1006: ('吃力不讨好','work hard but get little result; do a hard but thankless job'),
         1007: ('家喻户晓','known to every household; widely known'),
         1008: ('说一不二','stand by one\'s word'),
         2000: ('赵大妈','Person who goes around and gets into other people\'s business. Loves to talk to people.'),
         5000: ('伦敦西区','London West End',words5000)}



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

    print('Word Test! Any time you can type in give up, gu, or next to get the answer.')
    print('You can also type in quit to exit the program.')
    print('词汇考研！任何时候可以输入give up 或 gu 或 next 得到答案。')
    print('你也可以输入quit退出程序。')
    temp = iter(words)
    word_index = next(temp,None)
    while True:
        chooseword = input(f'Please type the Chinese for: {words[word_index][1]}: ')
        if chooseword in ['give up','gu','next']:
            print('Answer (答案): ')
            value = words[word_index]
            print('{:<5} | {:口<10} | {}'.format(word_index,value[0],value[1]))
            if len(value) > 2:
                for k,v in value[2].items():
                    print(k+': ')
                    print(v[0])
                    print(v[1])
                print('===================================================')

            nextorrandom = input('Next word or random 顺序下个或者随机? Type in next (下) or random (随): ')
            if nextorrandom in ['next','n','下','1']:
                word_index = next(temp,None)
            else:
                print('Random word used. 随机单词。')
                word_index, _ = random.choice(list(words.items()))
            continue
        elif chooseword in ['quit','q']:
            print('Quitting! 退出！')
            break
        elif chooseword not in [words[word_index][0]]:
            print('You are incorrect! Try again. 错误！请再次试试。')
            continue
        else:
            print('Correct! Moving to next word. 正确！继续下个词。')
            nextorrandom = input('Next word or random 顺序下个或者随机? Type in next (下) or random (随): ')
            if nextorrandom in ['next','n','下','1']:
                word_index = next(temp,None)
            else:
                print('Random word used. 随机单词。')
                word_index, _ = random.choice(list(words.items()))
            continue
