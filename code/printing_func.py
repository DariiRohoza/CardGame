from rich import box
from rich.console import Console
from rich.table import Table

from card_class import Card
from player_class import Player
from constants_libraries import SUIT_LIB, MOVEMENT_LIB, CARD_PRINT, PLAYER_PRINT, MOVEMENT_PRINT


def print_hand(player: Player | None = None, hand: list[Card] | None = None) -> bool:
    if player is None or hand is None:
        print(f"No player provided or hand is empty")
        return False

    if len(hand) == 0:
        hand = player.hand

    card_table = Table(caption=f"{player.name}'s cards", box=box.ROUNDED)
    for item in CARD_PRINT:
        card_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
    for idx, item in enumerate(hand):
        style, suit_rank = item.style, str(item.rank) + str(SUIT_LIB[item.suit])
        card_table.add_row(str(idx), style, suit_rank)

    console = Console(force_terminal=True, color_system="truecolor", width=150)
    console.print(card_table)
    return True

def print_players(player_list: list[Player], player: Player | None = None) -> bool:
    if len(player_list) == 0:
        print(f"Not enough players to print!")
        return False

    player_table = Table(caption=f"The players", box=box.ROUNDED)
    for item in PLAYER_PRINT:
        player_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
    for idx, plr in enumerate(player_list):
        name, health = plr.name, f"{plr.health:,.2f}"
        defense, attack_stack = str(plr.defending), f"{plr.attack_stack:,.2f}"
        actions, speed = str(plr.action_count), plr.speed_value()
        weakness, strength = plr.weakness, plr.strength

        if weakness == "": weakness = "None"
        if strength == "": strength = "None"
        you = "You" if player == plr else "N/A"

        player_table.add_row(str(idx), name, health, defense, attack_stack, actions,
                             f"{speed:,.2f} m/s", weakness, strength, you)

    console = Console(force_terminal=True, color_system="truecolor", width=200)
    console.print(player_table)
    return True

def print_movement_table():
    move_table = Table(caption=f"Moves", box=box.ROUNDED)
    for item in MOVEMENT_PRINT:
        move_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
    idx = 0
    for key, val in MOVEMENT_LIB.items():
        if type(val[1]) is str:
            move_possibility = val[1]
        else:
            move_possibility = ""
            for item in val[1]:
                move_possibility += item
                move_possibility += " OR " if item is not val[1][-1] else ""
        move_table.add_row(str(idx), f"{key}", f"{val[0]}", f"{move_possibility}")
        idx += 1

    console = Console(force_terminal=True, color_system="truecolor", width=150)
    console.print(move_table)