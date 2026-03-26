# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 22:12:57 2026

@author: sheng
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
import yaml


# --- Ability enum -----------------------------------------------------------

class Ability(Enum):
    FLYING    = "Flying"     # Can only be blocked by other Flying creatures
    DEFENDER  = "Defender"   # Cannot attack; gains +5 max HP
    SWIFTNESS = "Swiftness"  # Attacks before normal creatures in combat
    NONE      = "None"


ABILITY_BONUS_HP: dict[Ability, int] = {
    Ability.DEFENDER: 5,   # Defenders are tankier
}


# --- Creature dataclass -----------------------------------------------------

@dataclass
class Creature:
    name:        str
    max_hp:      int
    attack:      int
    ability:     Ability        = Ability.NONE
    description: str            = ""

    # Runtime state — not part of the card definition
    current_hp:   int           = field(init=False)
    is_exhausted: bool          = field(init=False, default=False)  # "tapped" in MTG terms

    def __post_init__(self):
        # Apply any passive HP bonuses from the creature's ability
        bonus = ABILITY_BONUS_HP.get(self.ability, 0)
        self.max_hp     += bonus
        self.current_hp  = self.max_hp

    # --- Properties ---------------------------------------------------------

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    @property
    def can_attack(self) -> bool:
        return self.is_alive and not self.is_exhausted and self.ability is not Ability.DEFENDER

    # --- Combat helpers -----------------------------------------------------

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def exhaust(self) -> None:
        """Mark the creature as having acted this turn."""
        self.is_exhausted = True

    def ready(self) -> None:
        """Refresh at the start of a new turn."""
        self.is_exhausted = False

    # --- Display ------------------------------------------------------------

    def __str__(self) -> str:
        status = "exhausted" if self.is_exhausted else "ready"
        return (
            f"{self.name} [{self.ability.value}] "
            f"HP: {self.current_hp}/{self.max_hp}  ATK: {self.attack}  ({status})"
        )


# --- YAML loader ------------------------------------------------------------

def _parse_ability(raw: Optional[str]) -> Ability:
    """Convert a YAML string to an Ability enum, defaulting to NONE."""
    if not raw:
        return Ability.NONE
    try:
        return Ability(raw)
    except ValueError:
        print(f"Warning: unknown ability '{raw}', defaulting to NONE.")
        return Ability.NONE


def load_creatures(path: str | Path) -> list[Creature]:
    """
    Load every creature defined in a YAML file and return a list of
    freshly constructed Creature instances.

    Expected YAML structure:
        creatures:
          - name: Dragon
            hp: 20
            attack: 8
            ability: Flying
            description: "..."
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    creatures: list[Creature] = []

    for entry in data.get("creatures", []):
        creature = Creature(
            name        = entry["name"],
            max_hp      = entry["hp"],
            attack      = entry["attack"],
            ability     = _parse_ability(entry.get("ability")),
            description = entry.get("description", ""),
        )
        creatures.append(creature)

    return creatures


# --- Demo -------------------------------------------------------------------

if __name__ == "__main__":
    creatures = load_creatures("creatures.yaml")

    print("=== Creatures loaded from YAML ===\n")
    for c in creatures:
        print(c)
        print(f"  \"{c.description}\"\n")

    # Simulate a quick combat exchange between the first two creatures
    attacker, defender = creatures[0], creatures[1]
    print(f"--- Combat: {attacker.name} attacks {defender.name} ---")

    if attacker.can_attack:
        defender.take_damage(attacker.attack)
        attacker.exhaust()
        print(f"  {attacker.name} deals {attacker.attack} damage.")
        print(f"  {defender}")
        if not defender.is_alive:
            print(f"  {defender.name} has been destroyed!")
    else:
        print(f"  {attacker.name} cannot attack!")