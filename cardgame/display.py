# -*- coding: utf-8 -*-
"""
Card Game — display.py

All Rich-powered rendering for the card game.
Import these functions in turn.py to replace plain print() calls.
"""
from __future__ import annotations
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.progress import BarColumn, Progress, TextColumn
from rich import box
from rich.rule import Rule

import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from creature import Creature, Player

# from creature import Creature, Player

console = Console()


# --- Colors -----------------------------------------------------------------

ABILITY_COLOR: dict[str, str] = {
    "Flying":    "sky_blue2",
    "Defender":  "steel_blue",
    "Swiftness": "gold1",
    "None":      "grey50",
}

TRAIT_COLOR: dict[str, str] = {
    "Enraged":        "red1",
    "Blessed":        "yellow1",
    "Cursed":         "magenta",
    "Withered":       "grey42",
    "Battle-Hardened": "orange1",
}

FLAVOR_COMMENTS = {
    "activate": [
        "The magic has concluded.",
        "All spells are done!",
    ],
    "attack": [
        "The battlefield trembles.",
        "No mercy shown.",
        "Steel meets flesh.",
        "A decisive strike!",
        "The crowd roars.",
    ],
    "destroyed": [
        "Reduced to rubble.",
        "Another falls.",
        "Gone, but not forgotten.",
        "The dust settles.",
        "Nothing remains.",
    ],
    "direct_attack": [
        "The gates are broken!",
        "No one left to defend!",
        "Chaos erupts!",
        "The enemy is exposed!",
        "A devastating blow!",
    ],
    "purchase": [
        "A new ally joins the cause.",
        "The ranks grow stronger.",
        "Coin well spent.",
        "Fortune favors the bold.",
        "A fine addition to the field.",
    ],
}


# --- Helpers ----------------------------------------------------------------

def _hp_bar(current: int, maximum: int, width: int = 16) -> Text:
    """Render a coloured HP bar as a Rich Text object."""
    ratio    = current / maximum if maximum > 0 else 0
    filled   = int(ratio * width)
    empty    = width - filled

    if ratio > 0.5:
        color = "green3"
    elif ratio > 0.25:
        color = "yellow1"
    else:
        color = "red1"

    bar = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * empty,  style="grey30")
    bar.append(f"  {current}/{maximum}", style="grey70")
    return bar


def _ability_badge(ability_name: str) -> Text:
    color = ABILITY_COLOR.get(ability_name, "grey50")
    badge = Text()
    badge.append(f" {ability_name} ", style=f"bold {color} on grey15")
    return badge


def _trait_badges(traits) -> Text:
    if not traits:
        return Text("none", style="grey50 italic")
    result = Text()
    for i, trait in enumerate(traits):
        color = TRAIT_COLOR.get(trait.name, "white")
        result.append(trait.name, style=f"bold {color}")
        if i < len(traits) - 1:
            result.append("  ")
    return result


# --- Creature card ----------------------------------------------------------

def creature_card(creature: Creature, width: int = 36) -> Panel:
    """Render a single creature as a Rich Panel card."""
    alive  = creature.is_alive
    status = "[grey50 italic]exhausted[/]" if creature.is_exhausted else "[green3]ready[/]"

    # Title with status
    title = Text()
    title.append(creature.name, style="bold white" if alive else "bold grey50 strike")
    title.append("  ")
    title.append(_ability_badge(creature.ability.value))

    # Body
    body = Text()
    body.append("  HP   ", style="grey70")
    body.append(_hp_bar(creature.current_hp, creature.max_hp))
    body.append("\n")
    body.append("  ATK  ", style="grey70")
    body.append(str(creature.attack), style="bold red1")
    body.append("\n")
    body.append("  COST ", style="grey70")
    body.append(str(creature.cost), style="bold yellow1")
    body.append("  INCOME ", style="grey70")
    body.append("+" + str(creature.income), style="bold green3")
    body.append(" gold\n")
    body.append("  ")
    body.append(_trait_badges(creature.traits))
    body.append("\n  ")
    
    if creature.is_exhausted:
        body.append("exhausted", style="grey50 italic")
    else:
        body.append("ready", style="green3")

    border_color = "grey30" if not alive else (
        "red3" if creature.is_exhausted else "cyan"
    )

    return Panel(
        body,
        title=title,
        title_align="left",
        border_style=border_color,
        width=width,
        box=box.ROUNDED,
    )


# --- Player board -----------------------------------------------------------

def render_player(player: Player) -> None:
    """Render a player's full board — health, gold, and all creatures."""
    hp_ratio = player.hp / player.max_hp if player.max_hp > 0 else 0
    hp_color = "green3" if hp_ratio > 0.5 else "yellow1" if hp_ratio > 0.25 else "red1"

    header = Text()
    header.append(f" {player.name} ", style="bold white on grey15")
    header.append("  HP: ", style="grey70")
    header.append(f"{player.hp}/{player.max_hp}", style=f"bold {hp_color}")
    header.append("  Gold: ", style="grey70")
    header.append(f"{player.gold}", style="bold yellow1")

    console.print(header)

    if player.creatures:
        cards = [creature_card(c) for c in player.creatures]
        console.print(Columns(cards, padding=(0, 1)))
    else:
        console.print("  [grey50 italic](no creatures on field)[/]")


# --- Shop -------------------------------------------------------------------

def render_shop(shop: list[Creature], player: Player) -> None:
    """Render the available shop creatures as a table."""
    table = Table(
        title=f"[bold yellow1]⚔  Shop[/] for {player.name}",
        box=box.SIMPLE_HEAVY,
        border_style="yellow4",
        header_style="bold yellow1",
        show_lines=True,
    )
    table.add_column("#",       style="grey50",  width=3)
    table.add_column("Name",    style="bold white")
    table.add_column("Ability", style="cyan")
    table.add_column("HP",      style="green3",  width=5)
    table.add_column("ATK",     style="red1",    width=5)
    table.add_column("Traits",  style="magenta")
    table.add_column("Cost",    style="yellow1", width=6)
    table.add_column("+Gold",   style="green3")
    table.add_column("Era",     style="white")

    for i, c in enumerate(shop):
        traits = ", ".join(t.name for t in c.traits) or "—"
        table.add_row(
            str(i + 1),
            c.name,
            c.ability.value,
            str(c.max_hp),
            str(c.attack),
            traits,
            f"{c.cost}g",
            str(c.income),
            c.era.value,
        )

    console.print(table)


# --- Combat events ----------------------------------------------------------

def log_purchase(player_name: str, creature_name: str, cost: int, gold_left: int) -> None:
    console.print(
        f"  [yellow1]💰[/] [bold]{player_name}[/] purchased "
        f"[bold cyan]{creature_name}[/] for [yellow1]{cost}g[/] "
        f"([grey70]{gold_left}g remaining[/])"
    )

def log_cant_afford(player_name: str, creature_name: str, cost: int, gold: int) -> None:
    console.print(
        f"  [red1]✗[/] [bold]{player_name}[/] can't afford "
        f"[bold cyan]{creature_name}[/] "
        f"([yellow1]{cost}g[/] needed, have [yellow1]{gold}g[/])"
    )

def log_defender(creature_name: str) -> None:
    console.print(
        f"  [yellow1]🌊[/] A formidable presence here!"
        f"[bold cyan]{creature_name}[/] is blocking the way!"
    )

def log_cast(creature_name: str, spell_name: str) -> None:
    console.print(
        f" [yellow1]🪄[/] Magic swirls in the air..."
        f"[bold cyan]{creature_name}[/] casts [purple]{spell_name}[/]"
        )
    
def log_effect(creature_name: str, effect: str) -> None:
    console.print(
        f" [yellow1]🪄[/] "
        f"[bold cyan]{creature_name}[/] [purple]{effect}[/]"
        )

def log_attack(attacker: str, target: str, damage: int) -> None:
    console.print(
        f"  [red1]⚔[/]  [bold]{attacker}[/] attacks "
        f"[bold]{target}[/] for [bold red1]{damage}[/] damage"
    )

def log_direct_attack(attacker: str, player_name: str, damage: int) -> None:
    console.print(
        f"  [bold red1]💥[/] [bold]{attacker}[/] strikes "
        f"[bold]{player_name}[/] directly for [bold red1]{damage}[/] damage!"
    )

def log_creature_destroyed(name: str) -> None:
    console.print(f"  [grey50]💀 {name} has been destroyed![/]")

def log_no_attackers(player_name: str) -> None:
    console.print(f"  [grey50]{player_name} has no creatures that can attack.[/]")

def log_creature_removed(creature_name: str, player_name: str) -> None:
    console.print(f"  [grey50]🗑  {creature_name} removed from {player_name}'s field.[/]")

def log_gold_income(player_name: str, amount: int, total: int) -> None:
    console.print(
        f"  [yellow1]+{amount}g[/] → [bold]{player_name}[/] "
        f"([yellow1]{total}g[/] total)"
    )

def log_readied(player_name: str) -> None:
    console.print(f"  [green3]↺[/]  {player_name}'s creatures are readied.")

def log_flavor(event: str) -> None:
    """Print a randomly chosen flavor comment for a given event type."""
    options = FLAVOR_COMMENTS.get(event, [])
    if not options:
        return
    text = random.choice(options)
    console.print(f"    [italic grey50]{text}[/]")

# --- Turn / game headers ----------------------------------------------------

def render_turn_header(turn_number: int, player_name: str) -> None:
    console.print()
    console.rule(
        f"[bold white]TURN {turn_number}[/]  [cyan]{player_name}[/]",
        style="cyan",
    )

def render_phase_header(phase: str) -> None:
    console.print(f"\n  [bold grey70]── {phase.upper()} ──[/]")

def render_board_divider() -> None:
    console.rule(style="grey30")

def render_game_start(p1: str, p2: str) -> None:
    console.print()
    console.rule("[bold yellow1]⚔  GAME START  ⚔[/]", style="yellow1")
    console.print(f"\n  [bold cyan]{p1}[/] [grey50]vs[/] [bold cyan]{p2}[/]\n")

def render_game_over(winner: str, turn: int) -> None:
    console.print()
    console.rule("[bold red1]GAME OVER[/]", style="red1")
    console.print(
        f"\n  [bold yellow1]🏆  {winner}[/] wins on turn [bold]{turn}[/]!\n"
    )
