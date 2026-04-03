# -*- coding: utf-8 -*-
"""
Card Game — turn.py

Manages the turn structure for a two-player card game.
Each turn cycles through four phases:
  1. Purchase  — the active player buys a creature from the shop
  2. Attack    — the active player's creatures attack the opponent
  3. Disposal  — dead creatures are removed from the field
  4. End       — the turn passes to the other player
"""

from __future__ import annotations
import random
from creature import Creature, Player, load_creatures, load_traits


# --- Turn class -------------------------------------------------------------

class Turn:
    def __init__(
        self,
        player_one:     Player,
        player_two:     Player,
        shop:           list[Creature],
        gold_per_turn:  int = 3,
    ):
        self.player_one    = player_one
        self.player_two    = player_two
        self.shop          = shop
        self.gold_per_turn = gold_per_turn
        self.turn_number   = 1

        # player_one always goes first
        self.active_player   = player_one
        self.opponent_player = player_two

    # --- Phase helpers ------------------------------------------------------

    def _divider(self, title: str) -> None:
        print(f"\n  --- {title} ---")

    def _switch_active_player(self) -> None:
        self.active_player, self.opponent_player = (
            self.opponent_player,
            self.active_player,
        )

    # --- Phases -------------------------------------------------------------

    def purchase_phase(self) -> None:
        """
        Active player receives gold and may purchase one creature
        from the shop they can afford.
        """
        self._divider("Purchase Phase")

        self.active_player.gold += self.gold_per_turn
        print(f"  {self.active_player.name} receives {self.gold_per_turn} gold "
              f"(total: {self.active_player.gold})")

        affordable = [c for c in self.shop if self.active_player.can_afford(c)]

        if not affordable:
            print(f"  {self.active_player.name} can't afford anything in the shop.")
            return

        # Simple AI: buy the most expensive affordable creature
        chosen = max(affordable, key=lambda c: c.cost)
        self.active_player.purchase(chosen)

    def attack_phase(self) -> None:
        """
        Each ready creature of the active player attacks.
        If the opponent has alive creatures, they absorb the attack.
        Otherwise the damage goes directly to the opponent player's HP.
        """
        self._divider("Attack Phase")

        attackers = [c for c in self.active_player.alive_creatures if c.can_attack]

        if not attackers:
            print(f"  {self.active_player.name} has no creatures that can attack.")
            return

        for attacker in attackers:
            defenders = self.opponent_player.alive_creatures

            if defenders:
                # Attack a random defending creature
                target = random.choice(defenders)
                print(f"  {attacker.name} attacks {target.name} "
                      f"for {attacker.attack} damage.")
                target.take_damage(attacker.attack)

                if not target.is_alive:
                    print(f"  {target.name} has been destroyed!")
            else:
                # No creatures to block — hit the player directly
                print(f"  {attacker.name} attacks {self.opponent_player.name} "
                      f"directly for {attacker.attack} damage!")
                self.opponent_player.take_damage(attacker.attack)

            attacker.exhaust()

    def disposal_phase(self) -> None:
        """
        Remove any destroyed creatures from both players' rosters.
        """
        self._divider("Disposal Phase")

        for player in (self.active_player, self.opponent_player):
            dead = [c for c in player.creatures if not c.is_alive]
            for creature in dead:
                player.creatures.remove(creature)
                print(f"  {creature.name} is removed from {player.name}'s field.")

        if not any(
            not c.is_alive
            for p in (self.active_player, self.opponent_player)
            for c in p.creatures
        ):
            print("  No creatures to dispose of.")

    def end_phase(self) -> None:
        """
        Ready all creatures and pass the turn to the other player.
        """
        self._divider("End Phase")

        self.active_player.ready_all()
        print(f"  {self.active_player.name} readies all creatures.")
        self._switch_active_player()
        self.turn_number += 1

    # --- Full turn ----------------------------------------------------------

    def play_turn(self) -> None:
        """Run all four phases for the current active player."""
        print(f"\n{'='*50}")
        print(f"  TURN {self.turn_number} — {self.active_player.name}'s turn")
        print(f"{'='*50}")

        self.purchase_phase()
        self.attack_phase()
        self.disposal_phase()
        self.end_phase()

    # --- Game loop ----------------------------------------------------------

    def check_winner(self) -> Player | None:
        """Return the winning player if one side has lost, otherwise None."""
        if not self.player_one.is_alive:
            return self.player_two
        if not self.player_two.is_alive:
            return self.player_one
        return None

    def print_board(self) -> None:
        print(f"\n{self.active_player}")
        print(f"{self.opponent_player}")

    def run(self, max_turns: int = 50) -> None:
        """
        Run turns until one player's HP hits 0 or max_turns is reached.
        max_turns acts as a safety limit to prevent infinite games.
        """
        print("\n=== GAME START ===")
        self.print_board()

        while self.turn_number <= max_turns:
            self.play_turn()

            winner = self.check_winner()
            if winner:
                print(f"\n{'='*50}")
                print(f"  GAME OVER — {winner.name} wins on turn {self.turn_number}!")
                print(f"{'='*50}")
                self.print_board()
                return

        print(f"\n  Game ended after {max_turns} turns with no winner.")


# --- Entry point ------------------------------------------------------------

if __name__ == "__main__":
    # Load shared shop inventory
    traits = load_traits("traits.yaml")
    shop   = load_creatures("creatures.yaml", "traits.yaml")

    # Create two players
    alice = Player(name="Alice", hp=20, gold=2000)
    bob   = Player(name="Bob",   hp=20, gold=0)

    #%% Set up and run the game
    # this is an automated game between 2 computer opponents
    game = Turn(
        player_one    = alice,
        player_two    = bob,
        shop          = shop,
        gold_per_turn = 3,
    )
    game.run()