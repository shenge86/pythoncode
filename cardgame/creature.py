from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
import yaml


# --- Ability enum -----------------------------------------------------------

class Ability(Enum):
    FLYING    = "Flying"
    DEFENDER  = "Defender"
    SWIFTNESS = "Swiftness"
    NONE      = "None"

#  this dictionary has Ability enum values as keys and integers as values
ABILITY_BONUS_HP: dict[Ability, int] = {
    Ability.DEFENDER: 5,
}


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


# --- Creature dataclass -----------------------------------------------------

@dataclass
class Creature:
    name:        str
    max_hp:      int
    attack:      int
    cost:        int
    ability:     Ability = Ability.NONE
    description: str     = ""
    traits:      list[Trait] = field(default_factory=list)

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


def load_creatures(
    creatures_path: str | Path,
    traits_path:    str | Path,
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
            description: "..."
            traits:
              - Enraged
              - Blessed
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

        creature = Creature(
            name        = entry["name"],
            max_hp      = entry["hp"],
            attack      = entry["attack"],
            ability     = _parse_ability(entry.get("ability")),
            cost        = entry["cost"],
            description = entry.get("description", ""),
            traits      = traits,
        )
        creatures.append(creature)

    return creatures

#%% money exchange
def purchase(creature, assets):
    print('Gold before purchase: ', assets['gold'])
    if assets['gold'] >= creature.cost:
        assets['gold'] -= creature.cost
        assets['creatures'].append(creature)
        print(f'You have bought 1 {creature.name}')
        print('Gold remaining: ', assets['gold'])
    else:
        print('You do not have enough money to purhcase this!')
    
    return assets

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
if __name__ == "__main__":
    creatures = load_creatures("creatures.yaml", "traits.yaml")

    print("=== Creatures loaded with traits ===\n")
    for c in creatures:
        print(c)
        if c.traits:
            for t in c.traits:
                print(f"  Trait — {t}: {t.description}")
        print()
    
    #%% simulated battle
    # purchase one
    assets = {'gold': 1000,
              'creatures': [],
              }
              
    assets = purchase(creatures[0], assets)
    
    
    # simulate initial battle
    # attacker, defender = creatures[0], creatures[1]
    attacker = assets['creatures'][0]
    defender = creatures[1]
    print(f"--- Combat: {attacker.name} attacks {defender.name} ---")

    battle_exchange(attacker, defender)
    end_turn(creatures)
    
    battle_exchange(attacker, defender)