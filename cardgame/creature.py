from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
import yaml
import random

"""
Card Game

Defines the Creature, Trait and Player classes for a card game.
Creatures are loaded from YAML and can be purchased by Player.

Traits are randomly assigned when purchasing.

"""

# --- Ability enum -----------------------------------------------------------

class Ability(Enum):
    FLYING      = "Flying"
    DEFENDER    = "Defender"
    SWIFTNESS   = "Swiftness"
    INSPIRATION = "Inspiration"
    CREATION    = "Creation"
    INSIGHT     = "Insight"
    NONE        = "None"

#  this dictionary has Ability enum values as keys and integers as values
ABILITY_BONUS_HP: dict[Ability, int] = {
    Ability.DEFENDER: 5,
}

# --- Era enum -----------------------------------------------------------

class Era(Enum):
    MYTHICAL = "Mythical"
    MEDIEVAL = "Medieval"
    DEMONIC  = "Demonic"
    ANGELIC  = "Angelic"
    MODERN   = "Modern"
    FUTURE   = "Future"
    NONE     = "None"
# --- Trait dataclass --------------------------------------------------------

@dataclass
class Trait:
    name:            str
    hp_modifier:     int = 0
    attack_modifier: int = 0
    description:     str = ""

    def __str__(self) -> str:
        parts = []
        if self.hp_modifier:
            sign = "+" if self.hp_modifier > 0 else ""
            parts.append(f"HP {sign}{self.hp_modifier}")
        if self.attack_modifier:
            sign = "+" if self.attack_modifier > 0 else ""
            parts.append(f"ATK {sign}{self.attack_modifier}")
        modifiers = ", ".join(parts) if parts else "no modifiers"
        return f"{self.name} ({modifiers})"


# --- Trait loader -----------------------------------------------------------

def load_traits(path: str | Path) -> dict[str, Trait]:
    """
    Load traits from a YAML file and return them as a dict keyed by name
    for easy lookup when building creatures.

    Expected YAML structure:
        traits:
          - name: Cursed
            hp_modifier: -5
            attack_modifier: -2
            description: "..."
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    traits: dict[str, Trait] = {}

    for entry in data.get("traits", []):
        trait = Trait(
            name            = entry["name"],
            hp_modifier     = entry.get("hp_modifier", 0),
            attack_modifier = entry.get("attack_modifier", 0),
            description     = entry.get("description", ""),
        )
        traits[trait.name] = trait

    return traits


def append_random_trait(creature: Creature, available_traits: dict[str, Trait]) -> bool:
    """
    Append a random trait to a creature if it doesn't already have it.
    Returns True if a trait was added, False if all traits are already owned.
    """
    owned_names = {t.name for t in creature.traits}
    candidates  = [t for t in available_traits.values() if t.name not in owned_names]

    if not candidates:
        print(f"  {creature.name} already has all available traits!")
        return False

    trait = random.choice(candidates)
    creature.traits.append(trait)
    creature.max_hp     += trait.hp_modifier
    creature.current_hp += trait.hp_modifier
    creature.attack     += trait.attack_modifier

    print(f"  {creature.name} gained the trait: {trait}")
    return True

# --- Creature dataclass -----------------------------------------------------

@dataclass
class Creature:
    name:        str
    max_hp:      int
    attack:      int
    cost:        int
    income:      int = 0 # by default, a creature produces no gold for you
    ability:     Ability = Ability.NONE
    description: str     = ""
    traits:      list[Trait] = field(default_factory=list)
    era:         Era = Era.NONE

    # Runtime state
    current_hp:   int  = field(init=False)
    is_exhausted: bool = field(init=False, default=False)

    def __post_init__(self):
        # Special dataclass method that is called automatically immediately after __init__ finishes
        # Apply ability passive bonus first
        bonus = ABILITY_BONUS_HP.get(self.ability, 0)
        self.max_hp += bonus

        # Then stack all trait modifiers on top
        for trait in self.traits:
            self.max_hp += trait.hp_modifier
            self.attack += trait.attack_modifier

        # Clamp to sensible minimums so traits can't produce broken values
        self.max_hp = max(1, self.max_hp)
        self.attack = max(0, self.attack)

        self.current_hp = self.max_hp

    # --- Properties ---------------------------------------------------------

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    @property
    def can_attack(self) -> bool:
        return self.is_alive and not self.is_exhausted and self.ability is not Ability.DEFENDER

    @property
    def can_defend(self) -> bool:
        return self.is_alive and not self.is_exhausted

    # --- Combat helpers -----------------------------------------------------

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def exhaust(self) -> None:
        self.is_exhausted = True

    def ready(self) -> None:
        self.is_exhausted = False

    # --- Magic helpers -----------------------------------------------------
    def cast(self, creatures: list[Creature]) -> Creature | None:
        if self.ability is Ability.INSPIRATION:
            print(self.name + " casts Inspiration!")
            creature = random.choice(creatures) # pick random creature to inspire
            choice   = random.random()
            quantity = int(random.random()*4) + 1 # add 1 to ensure it is not 0 ever
            
            if choice <= 0.2:
                creature.attack += quantity
                print(creature.name + " has attack increase by " + str(quantity))
            elif choice <= 0.5:
                creature.max_hp     += 2
                creature.current_hp += 2
                print(creature.name + " has health increase by 2")
            elif choice >= 0.5:
                creature.attack += 1
                print(creature.name + " has attack increase by 1")
            
            return creature
        else:
            return None


    # --- Display ------------------------------------------------------------

    def __str__(self) -> str:
        status = "exhausted" if self.is_exhausted else "ready"
        trait_names = ", ".join(t.name for t in self.traits) if self.traits else "none"
        return (
            f"{self.name} [{self.ability.value}] "
            f"HP: {self.current_hp}/{self.max_hp}  ATK: {self.attack}  "
            f"Traits: {trait_names}  ({status})"
        )

# --- Creature loader --------------------------------------------------------

def _parse_ability(raw: Optional[str]) -> Ability:
    if not raw:
        return Ability.NONE
    try:
        return Ability(raw)
    except ValueError:
        print(f"Warning: unknown ability '{raw}', defaulting to NONE.")
        return Ability.NONE

def _parse_era(raw: Optional[str]) -> Era:
    if not raw:
        return Era.NONE
    try:
        return Era(raw)
    except ValueError:
        print(f"Warning: unknown era '{raw}', defaulting to NONE.")
        return Ability.NONE

def get_creatures_by_ability(creatures: list[Creature], ability: Ability) -> list[Creature]:
    return [c for c in creatures if c.ability is ability]

def has_ability(creatures: list[Creature], ability: Ability) -> bool:
    return any(c.ability is ability for c in creatures)

def load_creatures(
    creatures_path: str | Path,
    traits_path:    str | Path,
    era_allowed:    str | Era = Era.NONE,
) -> list[Creature]:
    """
    Load creatures from a YAML file, applying any traits listed on each
    creature entry by looking them up from the traits YAML.

    Expected creature YAML structure:
        creatures:
          - name: Dragon
            hp: 20
            attack: 8
            ability: Flying
            cost: 1000
            description: "..."
            traits:
              - Enraged
            era: mythical
    """
    # Load the trait definitions first so we can look them up by name
    known_traits = load_traits(traits_path)

    with open(creatures_path, "r") as f:
        data = yaml.safe_load(f)

    creatures: list[Creature] = []

    for entry in data.get("creatures", []):
        # Resolve trait names from the creature entry into Trait objects
        trait_names  = entry.get("traits", [])
        traits: list[Trait] = []

        for name in trait_names:
            if name in known_traits:
                traits.append(known_traits[name])
            else:
                print(f"Warning: unknown trait '{name}' on {entry['name']}, skipping.")

        # also add in one random trait
        # owned_names = {t.name for t in traits}
        # candidates  = [t for t in known_traits.values() if t.name not in owned_names]
        
        # if not candidates:
        #     pass # already have every trait
        # else: 
        #     trait = random.choice(candidates)
        #     traits.append(trait)

        creature = Creature(
            name        = entry["name"],
            max_hp      = entry["hp"],
            attack      = entry["attack"],
            ability     = _parse_ability(entry.get("ability")),
            cost        = entry["cost"],
            income      = entry["income"],
            description = entry.get("description", ""),
            traits      = traits,
            era         = _parse_era(entry.get("era"))
        )
        
        # Only append if matches the Era of creature
        if creature.era == _parse_era(era_allowed):
            creatures.append(creature)
        else:
            pass
            # print(f'Ignoring {creature.name} since not a {era_allowed}')

    return creatures

# --- Player class -----------------------------------------------------------
 
class Player:
    def __init__(self, name: str, hp: int = 20, gold: int = 1000, income: int = 0):
        self.name       = name
        self.hp         = hp
        self.max_hp     = hp
        self.gold       = gold
        self.income     = income
        self.creatures: list[Creature] = []
 
    # --- Properties ---------------------------------------------------------
 
    @property
    def is_alive(self) -> bool:
        return self.hp > 0
 
    @property
    def alive_creatures(self) -> list[Creature]:
        return [c for c in self.creatures if c.is_alive]
 
    # --- Health -------------------------------------------------------------
 
    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        print(f"  {self.name} takes {amount} damage! HP: {self.hp}/{self.max_hp}")
 
    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"  {self.name} heals {amount}. HP: {self.hp}/{self.max_hp}")
 
    # --- Shop ---------------------------------------------------------------
 
    def can_afford(self, creature: Creature) -> bool:
        return self.gold >= creature.cost
 
    def choose_purchase(self, affordable: list[Creature]) -> bool:
        """Most basic purchasing logic for an AI"""
        chosen = max(affordable, key=lambda c: c.cost)
        # self.gold -= chosen.cost # do not uncomment if in turns.py
        return [chosen]
 
    def purchase(self, creature: Creature, verbosity: bool=False) -> bool:
        """
        Attempt to purchase a creature. Returns True if successful,
        False if the player can't afford it.
        """
        if not self.can_afford(creature):
            if verbosity:
                print(
                    f"  {self.name} can't afford {creature.name}! "
                    f"(costs {creature.cost}, have {self.gold} gold)"
                )
            return False
 
        self.gold -= creature.cost
        self.creatures.append(creature)
        if verbosity:
            print(
                f"  {self.name} purchased {creature.name} for {creature.cost} gold. "
                f"({self.gold} gold remaining)"
            )
        return True
 
    def sell(self, creature: Creature) -> bool:
        """
        Sell a creature back for half its cost (rounded down).
        Returns True if successful, False if creature isn't owned.
        """
        if creature not in self.creatures:
            print(f"  {self.name} doesn't own {creature.name}!")
            return False
 
        refund = creature.cost // 2
        self.creatures.remove(creature)
        self.gold += refund
        print(
            f"  {self.name} sold {creature.name} for {refund} gold. "
            f"({self.gold} gold remaining)"
        )
        return True
 
    def update_income(self):
        """Updates the income for the player"""
        self.income = 0 # reset to 0
        for creature in self.creatures:
            self.income += creature.income

    # --- Turn management ----------------------------------------------------
 
    def ready_all(self) -> None:
        """Refresh all creatures at the start of a new turn."""
        for creature in self.alive_creatures:
            creature.ready()
 
    # --- Display ------------------------------------------------------------
 
    def __str__(self) -> str:
        lines = [
            f"Player: {self.name}  HP: {self.hp}/{self.max_hp}  Gold: {self.gold}",
            f"  Creatures ({len(self.alive_creatures)} alive):",
        ]
        if self.creatures:
            for c in self.creatures:
                status = "💀" if not c.is_alive else ""
                lines.append(f"    {status} {c}")
        else:
            lines.append("    (none)")
        return "\n".join(lines)

#%%
class HumanPlayer(Player):
    def choose_purchase(self, affordable: list[Creature]) -> bool:
        gold = self.gold
        # show options
        print('Choose a number or q to quit: ')
        
        chosen_str = ''
        chosen_arr = []
        
        while chosen_str not in ['q', 'quit']:
            if len(affordable) > 0:
                for i, creature in enumerate(affordable):
                    print(f'[{i}] {creature.name}  | {creature.cost} gold')
            
                chosen_str = input('Enter a number to choose: ')
                chosen = affordable[int(chosen_str)]
                gold -= chosen.cost
                chosen_arr.append(chosen)
                
                # print(chosen_arr)
                
                # update options (reduce it further)
                affordable = [c for c in affordable if (gold >= c.cost)]
            else:
                chosen_str = 'q'
                print('You have no more gold to purchase anyone!')
        
        return chosen_arr
        
        

class AIPlayer(Player):
    def choose_purchase(self, affordable: list[Creature]) -> bool:
        gold = self.gold # temporary variable for calculating when to stop
        chosen_cheapest  = min(affordable, key=lambda c: c.cost)
        print('Cheapest creature: ', chosen_cheapest)
        
        chosen_expensive = max(affordable, key=lambda c: c.cost)
        print('Expensivest creature: ', chosen_expensive)
        chosen_arr = []
        while gold >= chosen_expensive.cost:
            chosen = max(affordable, key=lambda c: c.cost)
            chosen_arr.append(chosen)
            gold -= chosen.cost
            # self.gold -= chosen.cost # do not put here if in turns.py
            
        # now buy the cheapest ones
        while gold >= chosen_cheapest.cost:
            chosen = min(affordable, key=lambda c: c.cost)
            chosen_arr.append(chosen)
            gold -= chosen.cost
        
        return chosen_arr
        
#%%
if __name__ == "__main__":
    import display
    
    creatures_path = 'creatures.yaml'
    traits_path    = 'traits.yaml'
    era_allowed    = 'Modern'
    creatures = load_creatures(creatures_path, traits_path, era_allowed)

    print("=== Creatures loaded with traits ===\n")
    for c in creatures:
        print(c)
        if c.traits:
            for t in c.traits:
                print(f"  Trait — {t}: {t.description}")
        print("Era: ", c.era.value)
        print()
    
    #%% simulated battle
    alice = Player(name="Alice", hp=20, gold=1000)
    alice.purchase(creatures[0])
    alice.update_income()
    
    alice.purchase(creatures[1])
    alice.update_income()
    
    print('Income every turn: ', alice.income)
    
    #%% get defenders
    defenders = [c for c in creatures if c.ability is Ability.DEFENDER]
    print(defenders)
    
    #%% magic casts
    chosen = creatures[2]
    alice.purchase(chosen)
    alice.update_income()
    
    display.log_purchase(
        alice.name,
        chosen.name,
        chosen.cost,
        alice.gold,
    )
    
    chosen.cast(alice.creatures)
    
    display.render_player(alice)