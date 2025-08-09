'''
Chinese Test Words

References:
    Internet
    My mom

Version History:
    v1.1 August 2025:
        - Add tkinter for popugup GUI select options
        - Gamify the heck out of it with Creature class and attack and block options.
    
    V1.0 July 2025:
        - Create initial 'game' which is flashcard scoring with points

'''
import sys
import random

import pandas as pd

import tkinter as tk

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

words195 = {'Example 1': ('这个理论太深奥了, 您能不能讲得通透一点?','The theory is too difficult to understand, can you elaborate on it?'),
            'Example 2': ('天空由通透的湛蓝色变成了暗灰色。','The sky was changing from translucent blue to thicker grey.'),
            'Example 3': ('将物件放在灯座，看看哪一件通透能力最强？','Put each object in front of the lamp . which one is the most transparent')
            }

words204 = {'Example 1': ('当主角生病时，替补终于得到了第一次大好机会。', 'When the star was taken ill the understudy finally got her first Big Break')}

words5000= {'Details': ('伦敦西区（London\'s West End）是与纽约百老汇(Broadway)齐名的世界两大戏剧中心之一，是表演艺术的国际舞台，也是英国戏剧界的代名词。','在如此有限的区域内集中如此之多的剧院，在世界上只有纽约的百老汇可与之相比，而从历史传统来讲，西区要比百老汇悠久得多。')}

#%% I/O Functions
def dict2csv(words,output='words.csv'):
    '''Convert dictionary called words to DataFrame
    and save it to csv
    '''
    df = pd.DataFrame(
        [(k, v[0], v[1]) for k, v in words.items()],
        columns=["id", "chinese", "english"]
    )
    
    # Save to CSV
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return df

def csv2dict(filename):
    '''Ingests in csv file and converts it to a dictionary
    where first row is key and 2 other columns are tuple values in a tuple
    '''
    # Read CSV file
    df = pd.read_csv(filename)
    
    # Create dictionary: first column as key, next two columns as tuple
    data_dict = dict(zip(df.iloc[:, 0], zip(df.iloc[:, 1], df.iloc[:, 2])))
    
    return data_dict

#%% WORD JUMPS
def jumpword(nextorrandom):
    if nextorrandom in ['next','n','下','1']:
        word_index = next(temp,None)
    elif nextorrandom[0:3] in ['num']:
        word_index = int(nextorrandom[3:])
    else:
        print('Random word used. 随机单词。')
        word_index, _ = random.choice(list(words.items()))
    return word_index

#%% GUI functions
def choose_option():
    global selected_value
    selected_value = choice_var.get()  # store the selected value
    root.destroy()  # close the window

#%% Information messages
message_dict = {'theintro': '''
MAGIC LANGUAGE APTITUDE TEST
In this world, language can hold all keys. As you approach the final throne, 
an ancient dragon stares back at you. The beast opens its giant maw and speaks
in a thundering voice:
    
Do you truly think you can block my flaming breath?
Very well, I can go easy on you or it can be hard.
What do you choose, mortal?
''',

'correct': 'You blocked the flaming attack with an appropriate counterspell. You still sustain a little damage.',

'incorrect': 'You mutter senseless words that did nothing to stop the flame ball from hitting your body!!',

'flee': 'You flee from the scene as if a dragon is after you. You live the rest of your life a nameless nobody. You have utterly failed.',

'dying': 'You feel that you are close to dying. You know that if you fail to block one more time you are gone!',

'death': 'You fail to utter the correct words of power and you are struck one more time. You burn up in a pile of ashes.',

'victory': 'You have succeeded where no one else has. Truly you deserve the title of Hero.'

                }

#%% Gamified!
class Creature:
    def __init__(self, name, attack_power, health, block):
        """
        Initialize a Creature.

        Args:
            name (str): Name of the creature.
            attack_power (int or float): Attack strength of the creature.
            health (int or float): Current health points of the creature.
            block (float): Damage reduction percentage (0 to 1).
        """
        self.name = name
        self.attack_power = attack_power
        self.health = health
        self._block = block

    @property
    def blocked(self):
        return self._block
    
    @blocked.setter
    def blocked(self, new_value):
        if (new_value < 0) or (new_value > 1):
            raise ValueError('Damage reduction must be between 0 and 1')
        self._block = new_value
        
    def defense_up(self):
        if self.name == 'Dragon':
            print(f'{self.name} has defense of {self.blocked*100:.0f}%')
            if round(self._block,1) <= 0.5:
                print('The dragon skin hardens as its defense increases.')                
                self._block += 0.1
                print(f'{self.name} now has defense of {self.blocked*100:.0f}%')
            else:
                self._block = 0.55 # max it can ever reach

    def attack_ready(self):
        if self.name == 'Dragon':
            print('The dragon gets ready for another blast of terrible flames.')
        elif self.name == 'Hero':
            print('You steady your hands and cast another spell! You utter these words: ')
            print(random.choice(list(words.items()))[1][0]) # random word

    def attack(self, target):
        """Attack another creature, reducing their health."""
        if not isinstance(target, Creature):
            raise ValueError("Target must be a Creature instance.")
  
        # Calculate effective damage after block reduction
        damage = self.attack_power * (1 - target.blocked)
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage:.1f} damage!")
        print(f"{target.name} now has {target.health:.1f} health.")

    def is_alive(self):
        """Check if the creature is still alive."""
        return self.health > 0
    
    def is_dead(self):
        """Check if the creature is dead."""
        if self.health <= 0:
            print(f'The {self.name} is dead!')
        return self.health <= 0

    def __str__(self):
        """String representation of the creature."""
        return (f"{self.name} (Attack: {self.attack_power}, "
                f"Health: {self.health}, Block: {self.blocked*100:.0f}%)")
    
    
    
#%%
if __name__ == '__main__':
    # instantiate dictionary of words from csv file
    words      = csv2dict('words.csv')
    keys_words = list(words.keys())
    
    if '-dict' in sys.argv:
        print('Using as dictionary instead of tester...')
        
        # get all chinese words in dictionary
        chinesewords = []
        for r in words.values():
            chinesewords.append(r[0])
        
        while True:
            chooseword = input('Enter chinese character or enter Q to quit: ')
            if chooseword in chinesewords:
                matching_key = next((key for key, value in words.items() if value[0] == chooseword), None)
                value = words[matching_key]
                print(value[1])
                if len(value) > 2:
                    sentence_dict = words[matching_key][2]
                    for k,v in value[2].items():
                        print(k+': ')
                        print(v[0])
                        print(v[1])
                    print('===================================================')
                else:
                    print('No example sentence exists for this word.')
                
            elif chooseword in ['quit','Q','q']:
                print('Quitting! 退出！')
                break
            else:
                print('Word not in the dictionary. Try again!')
                continue
            
    else: # default option        
        print(message_dict['theintro'])
        
        # instantiate player
        player = Creature("Hero", 100, 100, 0.0) # block attribute changes so set to 0 here for now
        
        # instantiate dragon
        dragon = Creature("Dragon", 50, 250, 0.5) # 50% block        
        
        ##############################
        # GUI poup
        root = tk.Tk()
        root.title("Difficulty Choose")
        
        # Explanation label
        tk.Label(root, text=message_dict['theintro'], font=("Arial", 12)).pack(pady=(10, 5))
        
        # Tkinter variable for selection
        choice_var = tk.StringVar(value="Easy")  # default value
        
        # Radio buttons
        tk.Radiobutton(root, text="Easy", variable=choice_var, value="Easy").pack(anchor="w")
        tk.Radiobutton(root, text="Hard", variable=choice_var, value="Hard").pack(anchor="w")        
        
        # Select button
        tk.Button(root, text="Select", command=choose_option).pack(pady=10)
        
        # Run GUI
        root.mainloop()
        
        # Use the selected value after window closes
        print("Selected:", selected_value)
        ##############################
        # play_mode = input('You reply as such: ')
        play_mode = selected_value
        
        if play_mode.lower() in ['hard', 'h', 'reward']:
            play_mode = 'hard'
        elif play_mode.lower() in ['easy', 'e']:
            play_mode = 'easy'
        
        print(f'You have chosen the {play_mode} mode.')
        
        if play_mode == 'hard':
            print('You will never get this treasure. Get ready to face your end!!!')
            tk.messagebox.showwarning('Dragon roars', 'You will never get this treasure. Get ready to face your end!!!')
        else:
            print('Since you just want to practice and not take what is not yours, I will give you the chance to escape whenever you want.')
    
        temp = iter(words)
        word_index = next(temp,None)
    
        while True:
            print('Hitpoints: ', player.health)
            if player.is_dead() and play_mode == 'hard':
                print(message_dict['death'])
                tk.messagebox.showwarning("You have died!!!", message_dict['death'])
                break
            elif player.health < 5 and play_mode == 'hard':
                print(message_dict['dying'])
                tk.messagebox.showwarning("You are close to dying...", message_dict['dying'])
            elif dragon.is_dead() and play_mode == 'hard':
                print(message_dict['victory'])
                tk.messagebox.showwarning("You won!!!", message_dict['victory'])
                break
                
            dragon.attack_ready()
            question_word = f'You can block by uttering the magical equivalent of these words:\n{words[word_index][1]}'
            print(question_word)
            
            #%%
            list_choices = ['a', 'b', 'c', 'd']
            random.shuffle(list_choices) # shuffles them
            # create dictionary of choices
            target_value = words[word_index][0]
            dict_choices = {list_choices[0]: target_value,
                            list_choices[1]: words[random.choice(keys_words)][0],
                            list_choices[2]: words[random.choice(keys_words)][0],
                            list_choices[3]: words[random.choice(keys_words)][0],
                            }
            # list_choices = list(dict_choices.items())
            # random.shuffle(list_choices)
            # dict_choices = dict(list_choices)
            
            correct_choice = next((key for key, value in dict_choices.items() if value == target_value), None)


           #%%
            print('''
     ===============================================================                
     How do you choose to reply?
            ''')
            
            for key in sorted(dict_choices.keys()):
                print(f"\t\t{key}: {dict_choices[key]}")
            print('''
    ===============================================================
            ''')
            
            ##############################
            # GUI poup
            root = tk.Tk()
            root.title("What is the right word to utter here to block the attack?")
            
            # Explanation label
            tk.Label(root, text=f'Health: {player.health}', font=("Arial", 12)).pack(pady=(10, 5))
            tk.Label(root, text=question_word, font=("Arial", 12)).pack(pady=(10, 5))
            
            # Tkinter variable for selection
            choice_var = tk.StringVar(value="a")  # default value
            
            # Radio buttons
            for key in sorted(dict_choices.keys()):
                tk.Radiobutton(root, text=f"{key}: {dict_choices[key]}", variable=choice_var, value=f"{key}").pack(anchor="w")
            tk.Radiobutton(root, text="You choose to give up and abandon your quest to forever live in ignomy.", variable=choice_var, value="q").pack(anchor="w")
            
            # Select button
            tk.Button(root, text="Select", command=choose_option).pack(pady=10)
            
            # Run GUI
            root.mainloop()
            
            # Use the selected value after window closes
            print("Selected:", selected_value)
            ##############################    
            
            # chooseword = input('Enter the choice among these: ')
            chooseword = selected_value
            
            
            #%%            
            if chooseword in ['quit','q']:                
                print(message_dict['flee'])
                tk.messagebox.showinfo("Flee!!!", message_dict['flee'])
                # print('Quitting! 退出！')
                break            
            elif chooseword.lower() in correct_choice:
                # print('Correct! Moving to next word. 正确！继续下个词。')
                print(message_dict['correct'])
                player.blocked = 0.9
                dragon.attack(player)      
                word_index = jumpword('next')
                
                # player gets to attack
                player.attack_ready()                
                dragon.defense_up() # dragon defense hardens
                player.attack(dragon)
                
                continue
            else:
                # print('You are incorrect! Try again. 错误！请再次试试。')
                print(message_dict['incorrect'])
                player.blocked = 0
                dragon.attack(player)
                continue
