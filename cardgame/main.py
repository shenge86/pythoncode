# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 23:23:12 2026

@author: sheng
@name: The actual game
"""

from creature import load_creatures, Player

#%% battle exchange
def battle_exchange(attacker, defender):
    if attacker.can_attack:
        defender.take_damage(attacker.attack)
        attacker.exhaust()
        print(f"  {attacker.name} deals {attacker.attack} damage.")
        print(f"  {defender}")
        if not defender.is_alive:
            print(f"  {defender.name} has been destroyed!")
    else:
        print(f"  {attacker.name} cannot attack!")
        
    print('**********************************************************')
    
    # defender's retaliation
    if defender.can_defend:
        attacker.take_damage(defender.attack)
        defender.exhaust()
        print(f"  {defender.name} retaliates and deals {defender.attack} damage.")
        print(f"  {attacker}")
        if not attacker.is_alive:
            print(f"  {attacker.name} has been destroyed!")

def end_turn(creatures):
    print('===========EVERYONE RESTING=========')
    for creature in creatures:
        creature.ready()
        # all heal a bit
        creature.heal(1)
        print(f'{creature.name} has healed by 1')
        print(creature)

#%%
if __name__ == '__main__':
    print('Starting the game...')
    creatures_path = 'creatures.yaml'
    traits_path    = 'traits.yaml'
    creatures = load_creatures(creatures_path, traits_path)

    print("=== Creatures loaded with traits ===\n")
    for c in creatures:
        print(c)
        if c.traits:
            for t in c.traits:
                print(f"  Trait — {t}: {t.description}")
        print()
    
    #%% simulated battle
    alice = Player(name="Alice", hp=20, gold=1000)
    alice.purchase(creatures[0]) 
    
    # simulate initial battle
    # attacker, defender = creatures[0], creatures[1]
    # attacker = assets['creatures'][0]
    attacker = alice.creatures[0]
    defender = creatures[1]
    print(f"--- Combat: {attacker.name} attacks {defender.name} ---")

    battle_exchange(attacker, defender)
    end_turn(creatures)
    
    battle_exchange(attacker, defender)
