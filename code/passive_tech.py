from math import ceil

from movement_func import get_tech_modifiers

from player_class import Player


def super_hyper_passive_tech(player: Player, matched: list) -> float:
    tech, chain = matched[0]
    full_tech = tech + chain if chain != "" else tech
    passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

    extension = 1 if "EXTENDED" in modifiers_list else 0
    slide = 1.3 if "SLIDE" in modifiers_list else 1
    chain_mult = 1 + 1.10 * chain_len

    bonus = (1 + extension) * chain_mult * slide
    del player.passive_tech[tech]
    print(f" - {player.name}'s passive tech increased attack stack (tech: {full_tech} bonus: {bonus:,.2f})")
    return bonus

def ultra_passive_tech(player: Player, matched: list) -> float:
    tech, chain = matched[0]
    full_tech = tech + chain if chain != "" else tech
    passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

    extension = 0.25 if "EXTENDED" in modifiers_list else 0
    chain_mult = 0.50 + 0.20 * chain_len

    bonus = 1 + extension * chain_mult
    del player.passive_tech[tech]
    print(f" * Attacker passive tech increased damage (tech: {full_tech} multiplier: {bonus:,.2f})")
    return bonus

def bhop_passive_tech(player: Player, matched: list, use: str) -> int:
    if use == "":
        use_text = "dropped cards count and modified the drop cards action"
    else:
        use_text = "defense stacks gained"

    tech, chain = matched[0]
    full_tech = tech + chain if chain != "" else tech
    passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

    extension = 0.80 if "EXTENDED" in modifiers_list else 0
    high_jump = 1.35 if "HIGH-JUMP" in modifiers_list else 1
    chain_mult = 1 + 1.20 * chain_len

    bonus = ceil(chain_mult * high_jump + extension)
    if bonus >= 1:
        del player.passive_tech[tech]
        print(f" - {player.name}'s passive tech increased {use_text} (tech: {full_tech} bonus: {bonus})")
    return bonus

def fall_passive_tech(player: Player, matched: list) -> float:
    tech, chain = matched[0]
    full_tech = tech + chain if chain != "" else tech
    passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

    slow_fall = 0.03 if "SLOW-FALL" in modifiers_list else 0
    fast_fall = 0.05 if "FAST-FALL" in modifiers_list else 0
    chain_mult = 1 + 0.5 * chain_len

    bonus = 1 + (slow_fall - fast_fall) * chain_mult
    del player.passive_tech[tech]
    print(f" * Target passive tech changed damage (tech: {full_tech} multiplier: {bonus:,.2f})")
    return bonus

def bounce_passive_tech(player: Player, matched: list) -> float:
    tech, chain = matched[0]
    full_tech = tech + chain if chain != "" else tech
    passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

    extension = 1.40 if "EXTENDED" in modifiers_list else 1
    high_jump = 1.30 if "HIGH-JUMP" in modifiers_list else 1
    chain_mult = 1 + 0.20 * chain_len

    bonus = 2 * high_jump * extension * chain_mult
    del player.passive_tech[tech]
    print(f" * Attacker passive tech decreased target parry effectiveness")
    return bonus