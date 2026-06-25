from math import tanh

from movement_func import get_player_passive
from passive_tech import ultra_passive_tech, fall_passive_tech, bounce_passive_tech
from vector2_func import vector2_dir, vector2_decay

from card_class import Card
from player_class import Player

from constants_libraries import (STYLE_LIB, SUIT_LIB, ACTION_MULTIPLIER, SPEED_IMPACT,
                                 DEFENSE_STRENGTH_LIM, DEFENSE_WEAKNESS_LIM, DEFENSE_THRESHOLD, MIN_WEAKNESS_CRITICAL)


def evaluate_card(used_card: Card, player: Player, stack_apply: bool = False):
    weakness_used = False
    strength_used = False

    card_suit, card_rank, card_style = used_card.suit, used_card.rank, used_card.style
    value = float(card_rank)
    value += player.attack_stack if stack_apply else 0
    value *= STYLE_LIB[card_style]
    if player.weakness == SUIT_LIB[card_suit]:
        value *= 0.75
        print(f" * Used {player.name} weakness ({player.weakness})")
        weakness_used = True
    if player.strength == SUIT_LIB[card_suit]:
        value *= 1.50
        print(f" * Used {player.name} strength ({player.strength})")
        strength_used = True

    return value, weakness_used, strength_used

def evaluate_multipliers(player: Player, weakness_used: bool, strength_used: bool):
    if weakness_used:
        player.weakness = ""
    if strength_used:
        player.strength = ""

def attack_player(used_card: Card, attacker: Player, target: Player):
    defending_bool = False
    weakness_bool = False

    card_suit, card_rank, card_style = used_card.suit, used_card.rank, used_card.style
    damage, weakness_used, strength_used = evaluate_card(used_card, attacker, True)

    if attacker.attack_stack > 0:
        attacker.attack_stack = 0
        print(f" * Used attacker damage stack to amplify damage")

    if DEFENSE_THRESHOLD <= target.defending:
        damage = 0
        remaining_defense = 1 + (target.defending + 1) // 2
        print(f" * Nullified all damage taken at the cost of {target.defending - remaining_defense} defense stacks")
        target.defending = remaining_defense

    else:
        speed_modifier = 1 + tanh((attacker.speed_value() - target.speed_value()) / (3 * SPEED_IMPACT))
        if speed_modifier != 1:
            damage *= speed_modifier
            print(f" * Attacker and Target speeds modified damage ({speed_modifier:,.2f})")
        if attacker.speed_value() > 0 and target.speed_value() > 0:
            target_dir_x, target_dir_y = vector2_dir(target.speed)
            attacker_dir_x, attacker_dir_y = vector2_dir(attacker.speed)
            dif_dir_x = target_dir_x + attacker_dir_x
            dif_dir_y = target_dir_y + attacker_dir_y

            mult_x = 1.05 + (-0.05 * abs(dif_dir_x))
            mult_y = 1.05 + (-0.05 * abs(dif_dir_y))
            damage *= mult_x
            damage *= mult_y
            print(f" * Movement direction of both players affected damage (x: {mult_x:,.2f}, y: {mult_y:,.2f})")

        if target.parry_card is not None:
            value, weakness_used, strength_used = evaluate_card(target.parry_card, target)
            evaluate_multipliers(target, weakness_used, strength_used)

            matched_keys = get_player_passive(attacker, "BOUNCE-BOOST")
            if matched_keys:
                mult = bounce_passive_tech(attacker, matched_keys)
                value /= mult

            target.parry_time = 0
            target.parry_card = None
            damage -= value
            print(f" * Target parry card decreased attacker damage ({value:,.2f})")
            if attacker.speed_value() > 0:
                vector2_decay(attacker,
                    0.13 * speed_modifier * ACTION_MULTIPLIER,
                    0.13 * speed_modifier * ACTION_MULTIPLIER
                )
                print(f" * Target parry decreased attacker speed")

        matched_keys = get_player_passive(attacker, "ULTRA")
        if matched_keys:
            mult = ultra_passive_tech(attacker, matched_keys)
            damage *= mult

        matched_keys = get_player_passive(target, "FALL-BOOST")
        if matched_keys:
            mult = fall_passive_tech(target, matched_keys)
            damage *= mult

        if 0 < target.defending:
            damage *= 0.90 ** target.defending
            print(f" * Nullified 1 target defense stack")
            target.defending -= 1 # defense stacks get removed one by one, but they all impact damage taken
            defending_bool = True

        if target.weakness == SUIT_LIB[card_suit]:
            damage *= 1.50
            print(f" * Target weakness amplified damage ({target.weakness})")
            weakness_bool = True
        if target.strength == SUIT_LIB[card_suit]:
            damage *= 0.75
            print(f" * Target strength reduced damage ({target.strength})")

        if defending_bool and weakness_bool:
            # weak_def_crit scales effectiveness of hits targeting weakness with the amount of defense of target
            weak_def_crit = (target.defending // 3) - 1
            weak_def_crit = weak_def_crit if MIN_WEAKNESS_CRITICAL < weak_def_crit else MIN_WEAKNESS_CRITICAL
            target.defending -= weak_def_crit
            print(f" * Weakness caused target to lose {weak_def_crit} more defense stack(s)")

        if DEFENSE_WEAKNESS_LIM <= target.defending and target.weakness == SUIT_LIB[card_suit]:
            damage *= 0.66 # 2/3 : completely removing target weakness impact
            print(f" * Nullified target weakness scaling")
        if DEFENSE_STRENGTH_LIM <= target.defending and attacker.strength == SUIT_LIB[card_suit]:
            damage *= 0.83 # 5/6 : reducing 1.5x to 1.25x attacker strength impact
            print(f" * Reduced attacker strength scaling")

        vector2_decay(target,
            0.30 * speed_modifier * ACTION_MULTIPLIER,
            0.30 * speed_modifier * ACTION_MULTIPLIER
        )

    evaluate_multipliers(attacker, weakness_used, strength_used)
    if damage > 0:
        target.health -= damage
        target.weakness = SUIT_LIB[card_suit]
        target.strength = SUIT_LIB[(card_suit + 2) % len(SUIT_LIB)]
        print(f"{target.name}'s health after attacking : {target.health:,.2f}\n"
              f"{target.name} is now weak to {target.weakness} and strong with {target.strength}\n")
    else:
        print(f"{target.name}'s was unaffected by the attack\n")