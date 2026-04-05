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
import copy # required to not reference the same creature over and over

from creature import Creature, Player, AIPlayer, load_creatures, load_traits
import display


# --- Turn class -------------------------------------------------------------

class Turn:
    def __init__(
        self,
        player_one:    Player,
        player_two:    Player,
        shop_one:      list[Creature],
        shop_two:      list[Creature],
        gold_per_turn: int = 3,
    ):
        self.player_one    = player_one
        self.player_two    = player_two
        self.shop_one      = shop_one
        self.shop_two      = shop_two
        self.gold_per_turn = gold_per_turn
        self.turn_number   = 1

        self.active_player   = player_one
        self.opponent_player = player_two

    # --- Helpers ------------------------------------------------------------

    def _switch_active_player(self) -> None:
        self.active_player, self.opponent_player = (
            self.opponent_player,
            self.active_player,
        )

    # --- Phases -------------------------------------------------------------

    def purchase_phase(self) -> None:
        display.render_phase_header("Purchase Phase")

        self.active_player.gold += self.gold_per_turn
        display.log_gold_income(
            self.active_player.name,
            self.gold_per_turn,
            self.active_player.gold,
        )

        if self.active_player == self.player_one:
            affordable = [c for c in self.shop_one if self.active_player.can_afford(c)]
        else:
            affordable = [c for c in self.shop_two if self.active_player.can_afford(c)]

        if not affordable:
            display.log_cant_afford(
                self.active_player.name, "anything", 0, self.active_player.gold
            )
            return
        
        chosen_arr = self.active_player.choose_purchase(affordable)

        # do for each creature purchased
        for chosen in chosen_arr:
            self.active_player.gold -= chosen.cost
            self.active_player.creatures.append(copy.deepcopy(chosen))
            
            display.log_purchase(
                self.active_player.name,
                chosen.name,
                chosen.cost,
                self.active_player.gold,
            )

    def attack_phase(self) -> None:
        display.render_phase_header("Attack Phase")

        attackers = [c for c in self.active_player.alive_creatures if c.can_attack]

        if not attackers:
            display.log_no_attackers(self.active_player.name)
            return

        for attacker in attackers:
            defenders = self.opponent_player.alive_creatures

            if defenders:
                target = random.choice(defenders)
                
                # Attacker hits defender
                display.log_attack(attacker.name, target.name, attacker.attack)
                target.take_damage(attacker.attack)
                if not target.is_alive:
                    display.log_creature_destroyed(target.name)
                elif target.is_alive and attacker.ability is not attacker.ability.SWIFTNESS: # Defender counter-attacks if still alive
                    display.log_attack(target.name, attacker.name, target.attack)
                    attacker.take_damage(target.attack)
                    if not attacker.is_alive:
                        display.log_creature_destroyed(attacker.name)
            else:
                display.log_direct_attack(
                    attacker.name, self.opponent_player.name, attacker.attack
                )
                self.opponent_player.take_damage(attacker.attack)

            attacker.exhaust()

    def disposal_phase(self) -> None:
        display.render_phase_header("Disposal Phase")

        removed_any = False
        for player in (self.active_player, self.opponent_player):
            dead = [c for c in player.creatures if not c.is_alive]
            for creature in dead:
                player.creatures.remove(creature)
                display.log_creature_removed(creature.name, player.name)
                removed_any = True

        if not removed_any:
            display.console.print("  [grey50 italic]No creatures to dispose of.[/]")

    def end_phase(self) -> None:
        display.render_phase_header("End Phase")

        self.active_player.ready_all()
        display.log_readied(self.active_player.name)
        self._switch_active_player()
        self.turn_number += 1

    # --- Full turn ----------------------------------------------------------

    def play_turn(self) -> None:
        display.render_turn_header(self.turn_number, self.active_player.name)
        self.purchase_phase()
        self.attack_phase()
        self.disposal_phase()
        self.end_phase()

        display.render_board_divider()
        display.render_player(self.active_player)
        display.render_player(self.opponent_player)

    # --- Game loop ----------------------------------------------------------

    def check_winner(self) -> Player | None:
        if not self.player_one.is_alive:
            return self.player_two
        if not self.player_two.is_alive:
            return self.player_one
        return None

    def run(self, max_turns: int = 50) -> None:
        display.render_game_start(self.player_one.name, self.player_two.name)
        display.render_shop(self.shop_one, self.player_one)
        display.render_shop(self.shop_two, self.player_two)
        display.render_player(self.player_one)
        display.render_player(self.player_two)

        while self.turn_number <= max_turns:
            self.play_turn()

            winner = self.check_winner()
            if winner:
                display.render_game_over(winner.name, self.turn_number)
                display.render_player(self.player_one)
                display.render_player(self.player_two)
                return

        display.console.print(
            f"\n  [grey50]Game ended after {max_turns} turns with no winner.[/]"
        )


# --- Entry point ------------------------------------------------------------

if __name__ == "__main__":
    shop_one  = load_creatures("creatures.yaml", "traits.yaml", "Medieval")
    shop_two  = load_creatures("creatures.yaml", "traits.yaml", "Mythical")
    alice = AIPlayer(name="Alice", hp=20, gold=1000)
    bob   = Player(name="Bob",   hp=20, gold=200)

    game = Turn(
        player_one    = alice,
        player_two    = bob,
        shop_one      = shop_one,
        shop_two      = shop_two,
        gold_per_turn = 3,
    )
    game.run()