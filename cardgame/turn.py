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

from creature import Creature, Player, AIPlayer, HumanPlayer, load_creatures, load_traits
from creature import Ability, get_creatures_by_ability, has_ability
import display

# --- Helper classes for shops -----------------------------------------------

def buff_random_shop_creature(shop: list[Creature], hp_bonus: int = 5, attack_bonus: int = 2) -> Creature | None:
    """
    Randomly select a creature in the shop and permanently buff its stats.
    Returns the buffed creature, or None if the shop is empty.
    """
    if not shop:
        return None

    chosen = random.choice(shop)
    chosen.max_hp      += hp_bonus
    chosen.current_hp  += hp_bonus
    chosen.attack      += attack_bonus

    console.print(
        f"  [bold yellow1]⚡ {chosen.name}[/] has been empowered! "
        f"[green3]+{hp_bonus} HP[/]  [red1]+{attack_bonus} ATK[/]"
    )
    return chosen

def merge_random_creature(shop_one: list[Creature], shop_two: list[Creature]) -> Creature | None:
    """
    Pick a random creature from shop_two and add a copy of it to shop_one.
    Returns the added creature, or None if shop_two is empty.
    """
    if not shop_two:
        console.print("  [grey50 italic]Second shop is empty, nothing to merge.[/]")
        return None

    chosen = copy.deepcopy(random.choice(shop_two))
    shop_one.append(chosen)

    console.print(
        f"  [bold cyan]✦ {chosen.name}[/] has arrived in the shop! "
        f"[grey50]HP: {chosen.max_hp}  ATK: {chosen.attack}  Cost: {chosen.cost}g[/]"
    )
    return chosen

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
        self.active_shop     = shop_one
        self.opponent_shop   = shop_two

    # --- Helpers ------------------------------------------------------------

    def _switch_active_player(self) -> None:
        self.active_player, self.opponent_player = (
            self.opponent_player,
            self.active_player,
        )

    def _switch_active_shop(self) -> None:
        self.active_shop, self.opponent_shop = (
            self.opponent_shop,
            self.active_shop,
        )

    # --- Phases -------------------------------------------------------------

    def purchase_phase(self) -> None:
        display.render_phase_header("Purchase Phase")

        # Update income and add gold
        self.active_player.update_income()
        self.active_player.gold += self.active_player.income
        
        # self.active_player.gold += self.gold_per_turn
        display.log_gold_income(
            self.active_player.name,
            self.active_player.income,
            # self.gold_per_turn,
            self.active_player.gold,
        )

        # if self.active_player == self.player_one:
        #     affordable = [c for c in self.shop_one if self.active_player.can_afford(c)]
        # else:
        #     affordable = [c for c in self.shop_two if self.active_player.can_afford(c)]

        affordable = [c for c in self.active_shop if self.active_player.can_afford(c)]

        if not affordable:
            display.log_cant_afford(
                self.active_player.name, "anything", 0, self.active_player.gold
            )
            return
        
        chosen_arr = self.active_player.choose_purchase(affordable)

        # do for each creature purchased
        for chosen in chosen_arr:
            self.active_player.gold -= chosen.cost #! This can also be in the Player class but then cannot connect to display
            self.active_player.creatures.append(copy.deepcopy(chosen))
            
            display.log_purchase(
                self.active_player.name,
                chosen.name,
                chosen.cost,
                self.active_player.gold,
            )
            
            display.log_flavor('purchase')

    def attack_phase(self) -> None:
        display.render_phase_header("Attack Phase")

        attackers = [c for c in self.active_player.alive_creatures if c.can_attack]
        
        #### activate special creature abilities
        # inspirers add stats to one random creature you have
        inspirers = get_creatures_by_ability(attackers, Ability.INSPIRATION)
        for inspirer in inspirers:
            display.log_cast(inspirer.name, Ability.INSPIRATION.value)
            inspirer.cast(self.active_player.alive_creatures)
            # attacker = random.choice(attackers) # pick random attacker to inspire
            # attacker.attack += 10
            # display.log_effect(attacker.name, "feels stronger! Attack +10")
        
        # insight checks and if you have at least one, allows you to make creatures in the shop stronger
        insight = has_ability(attackers, Ability.INSIGHT)
        if insight:
            insighters = get_creatures_by_ability(attackers, Ability.INSIGHT)
            display.log_cast(insighters[0].name, Ability.INSIGHT.value)
            buff_random_shop_creature(self.active_shop, hp_bonus=1, attack_bonus=1)
        
        # creation adds random creature from opponent shop or bonus shop into this one
        creation = has_ability(attackers, Ability.CREATION)
        if creation:
            creators = get_creatures_by_ability(attackers, Ability.CREATION)
            display.log_cast(creators[0].name, Ability.CREATION.value)
            merge_random_creature(self.active_shop, self.opponent_shop)
        ###########

        if not attackers:
            display.log_no_attackers(self.active_player.name)
            return

        for attacker in attackers:
            defenders = self.opponent_player.alive_creatures

            if defenders:
                # Defenders always defend first before anyone else
                defenders_walls = get_creatures_by_ability(defenders, Ability.DEFENDER)
                
                if len(defenders_walls) == 0:
                    # if no creatures with DEFENDER ability, choose a random creature
                    target = random.choice(defenders)
                else:
                    target = defenders_walls[0]
                    display.log_defender(target.name)
                
                # Attacker hits defender
                display.log_attack(attacker.name, target.name, attacker.attack)
                display.log_flavor('attack')
                
                target.take_damage(attacker.attack)
                if not target.is_alive:
                    display.log_creature_destroyed(target.name)
                    display.log_flavor('destroyed')
                elif target.is_alive and attacker.ability is not attacker.ability.SWIFTNESS: # Defender counter-attacks if still alive
                    display.log_attack(target.name, attacker.name, target.attack)
                    display.log_flavor('attack')
                    attacker.take_damage(target.attack)
                    if not attacker.is_alive:
                        display.log_creature_destroyed(attacker.name)
                        display.log_flavor('destroyed')
            else:
                display.log_direct_attack(
                    attacker.name, self.opponent_player.name, attacker.attack
                )
                display.log_flavor('direct_attack')
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
        self._switch_active_shop()
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
    known_traits = "traits.yaml"
    shop_medieval  = load_creatures("creatures.yaml", known_traits, "Medieval")
    shop_mythical  = load_creatures("creatures.yaml", known_traits, "Mythical")
    shop_modern    = load_creatures('creatures.yaml', known_traits, "Modern")
    
    alice = AIPlayer(name="Princess Alice", hp=10, gold=300)
    bob   = Player(name="Ancient Ent",   hp=200, gold=170)
    shen  = HumanPlayer(name="Shen", hp=20, gold=200)

    game = Turn(
        player_one    = shen,
        player_two    = alice,
        shop_one      = shop_modern,
        shop_two      = shop_medieval,
        gold_per_turn = 3,
    )
    game.run()