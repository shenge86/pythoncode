'''
Chinese test
'''
import random

words7  = {'Prounciation: ': ('jiāolǜ',''),
           'Example 1': ('短短几分钟我们就忘记了焦虑与苦恼。','For a few brief minutes we forgot the anxiety and anguish.'),
           'Example 2': ('当意外事件干扰了你的生活时，你会感到焦虑吗？','Do you feel anxious when unforeseen incidents intrude on your day?'),
           'Example 3': ('镇静剂有助于缓解焦虑所带来的不安症状。','Tranquillizers help alleviate the distressing symptoms of anxiety.'),
           'Example 4': ('焦虑是现代人的自然状态。','Anxiety is modern man\'s natural state.'),
           'Example 5': ('近来公众对这个问题的焦虑心情现在也许正在缓和下来。','The recent public anxiety about this issue may now be abating.')}

words8  = {'Example 1': ('拥挤的人群和喧闹的噪音可能会让游客有些茫然不知所措。','Sightseers may be a little overwhelmed by the crowds and noise.'),
           'Example 2': ('他边说话边茫然地打量着房间，心不在焉的样子。','He looked vaguely around the room as he spoke, his mind elsewhere.'),
           'Example 3': ('我茫然地走了35分钟。',' For 35 minutes I was walking around in a daze.'),
           'Example 4': ('她沉默了一会儿，嘴唇紧闭，眼神茫然。','She was silent for a moment, lips tight shut, eyes distant.'),
           'Example 5': ('阿博特一脸茫然。“我没听明白，先生。”','Abbot looked blank. \"I don\'t quite follow, sir.\" '),
           'Example 6': ('他突然改变话题，使她茫然不知所措。','His abrupt change of subject left her floundering helplessly.')}

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
            'Example 2': ('The sky was changing from translucent blue to thicker grey.','天空由通透的湛蓝色变成了暗灰色。'),
            'Example 3': ('Put each object in front of the lamp . which one is the most transparent', '将物件放在灯座，看看哪一件通透能力最强？')
            }

words204 = {'Example 1': ('当主角生病时，替补终于得到了第一次大好机会。')}

words5000= {'Details': ('伦敦西区（London\'s West End）是与纽约百老汇(Broadway)齐名的世界两大戏剧中心之一，是表演艺术的国际舞台，也是英国戏剧界的代名词。','在如此有限的区域内集中如此之多的剧院，在世界上只有纽约的百老汇可与之相比，而从历史传统来讲，西区要比百老汇悠久得多。')}

words = { 1: ('上司','superior'),
          2: ('顾虑','concern; misgivings'),
          3: ('罕见','rare; seldomly seen'),
          4: ('惯用语','idiom'),
          5: ('奋勇','courageously'),
          6: ('夹板','splint'),
          7: ('焦虑','anxiety',words7),
          8: ('茫然','at a loss',words8),
          9: ('自白','confession'),
         10: ('真挚','sincere (zhēnzhì)'),
         11: ('坠落','fall;drop'),
         12: ('陈词','statement'),
         13: ('地平线','horizon'),
         14: ('纳闷','wondered (in a perplexed way)',words14),
         15: ('人道主义','humanism'),
         16: ('膈应','【方言】指讨厌、令人不舒服，但未达到要呕吐的程度。更多的指的是心理上的不舒服。'),
         17: ('腻歪','【北方方言】1.因次数过多或时间过长而感觉厌烦 2.厌恶 3.无聊 4.一些情侣之间比较亲昵的事，说一些亲昵的话'),
         18: ('预算','budget'),
         100: ('接种','vaccinate'),
         101: ('阴性','negative(medical)'),
         102: ('义母','stepmother'),
         103: ('遗产','inheritance'),
         104: ('刻毒','spiteful; malicious'),
         105: ('百老汇','Broadway'),
         106: ('大厦','big building'),
         111: ('甲状','thyroid'),
         115: ('床单','bedsheet'),
         122: ('外卖','takeout',words122),
         124: ('关节炎','arthritis'),
         134: ('预示','foreshadow'),
         135: ('务必','must; be sure to'),
         147: ('分别','1.part; leave each other 2.distinguish;differentiate'),
         161: ('将就','make do with; put up with'),
         166: ('造诣','academic or artistic attainments'),
         173: ('介入','intervene; interpose; get involved'),
         174: ('历历在目','visible before the eyes; come clearly into view'),
         175: ('一笑置之','dismiss with a laugh; chuckle over at something'),
         186: ('短语','phrase'),
         187: ('顺时针','clockwise'),
         188: ('逆时针','counterclockwise'),
         189: ('远足','hiking'),
         190: ('徒步旅行','trekking',words190),
         191: ('贬义词','derogatory term'),
         192: ('抽脂','liposuction',words192),
         193: ('地标','landmark'),
         194: ('壁画','mural'),
         195: ('通透','penetrating',words195),
         196: ('弹幕','danmaku; bullet curtain (subtitle system in online video platforms where comments shoot across the screen)'),
         197: ('大方','generous'),
         198: ('吝啬','stingy;miserly'),
         199: ('吝啬鬼','stingy person'),
         200: ('谋生','means of living'),
         201: ('小龙虾','crawfish'),
         202: ('试镜','audition'),
         203: ('回拨','callback'),
         204: ('替补','substitute'),
         205: ('替角','understudy'),
         206: ('剧作家','playwright'),
         1000: ('旧地重游','Revisit a familiar place; return to old haunts'),
         1001: ('物是人非','The scenery remains the same but the people are changed. Things are unchanged but the people are gone.'),
         1002: ('劳逸结合','Strike a proper balance between work and rest.'),
         1003: ('劳逸不均','Uneven allocation of work and rest.'),
         1004: ('损人利己','to harm others to benefit oneself; benefit oneself at the expense of others'),
         1005: ('损人不利己','to harm others without benefiting oneself'),
         1006: ('吃力不讨好','work hard but get little result; do a hard but thankless job'),
         1007: ('家喻户晓','known to every household; widely known'),
         1008: ('说一不二','stand by one\'s word'),
         1009: ('开源节流','increase income and reduce expenditure; tap new supply and reduce consumption'),
         1010: ('志同道合','cherish same ideals and follow same path; have a common goal'),
         1011: ('言多必失','he who talks much is prone to error'),
         1012: ('下不为例','not to be taaken as a precedent; not to be repeated'),
         1013: ('麻木不仁','apathetic; insensitive; unfeeling'),
         1014: ('急中生智','think of brilliant plan in emergency'),
         1015: ('靠山吃山，靠水吃水','make use of local resources'),
         1016: ('一个天南，一个地北','to live miles apart'),
         1017: ('今朝有酒今朝醉','live in the moment'),
         2000: ('赵大妈','Person who goes around and gets into other people\'s business. Loves to talk to people.'),
         2001: ('一蟹不如一蟹','one crab is no better than the other; worse and worse candidates'),
         2002: ('大姑娘坐花轿——头一回','big girl rides flower carriage--first time; a special first time occurence'),
         5000: ('伦敦西区','London West End',words5000),
         5001: ('恐怖小店','Little Shop of Horrors'),
         }



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

    nextorrandom = input('Next word or random 顺序下个或者随机? Type in next (下) or random (随): ')

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
            if nextorrandom in ['next','n','下','1']:
                word_index = next(temp,None)
            else:
                print('Random word used. 随机单词。')
                word_index, _ = random.choice(list(words.items()))
            continue
