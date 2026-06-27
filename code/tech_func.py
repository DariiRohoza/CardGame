from math import ceil

from vector2_func import vector2_add, vector2_mult, vector2_dir

from move_tech_class import MoveTech
from player_class import Player
from constants_libraries import TECH_SPEED_LIB, SPEED_IMPACT

# passive tech
def super_hyper_passive_tech(player: Player, matched: list[MoveTech]) -> float:
    tech = matched[0]

    extension = 1 if "EXTENDED" in tech.modifiers else 0
    slide = 1.3 if "SLIDE" in tech.modifiers else 1
    chain_mult = 1 + 1.10 * tech.chain_count

    bonus = (1 + extension) * chain_mult * slide
    player.passive_tech.remove(tech)
    print(f" - {player.name}'s passive tech increased attack stack (tech: {tech} bonus: {bonus:,.2f})")
    return bonus

def ultra_passive_tech(player: Player, matched: list[MoveTech]) -> float:
    tech = matched[0]

    extension = 0.25 if "EXTENDED" in tech.modifiers else 0
    chain_mult = 0.50 + 0.20 * tech.chain_count

    bonus = 1 + extension * chain_mult
    player.passive_tech.remove(tech)
    print(f" * Attacker passive tech increased damage (tech: {tech} multiplier: {bonus:,.2f})")
    return bonus

def bhop_passive_tech(player: Player, matched: list[MoveTech], use: str) -> int:
    if use == "drop_half_cards":
        use_text = "dropped cards count and modified the drop cards action"
    else:
        use_text = "defense stacks gained"

    tech = matched[0]

    extension = 0.80 if "EXTENDED" in tech.modifiers else 0
    high_jump = 1.35 if "HIGH-JUMP" in tech.modifiers else 1
    chain_mult = 1 + 1.20 * tech.chain_count

    bonus = ceil(chain_mult * high_jump + extension)
    if bonus >= 1:
        player.passive_tech.remove(tech)
        print(f" - {player.name}'s passive tech increased {use_text} (tech: {tech} bonus: {bonus})")
    return bonus

def fall_passive_tech(player: Player, matched: list) -> float:
    tech = matched[0]

    slow_fall = 0.03 if "SLOW-FALL" in tech.modifiers else 0
    fast_fall = 0.05 if "FAST-FALL" in tech.modifiers else 0
    chain_mult = 1 + 0.5 * tech.chain_count

    bonus = 1 + (slow_fall - fast_fall) * chain_mult
    player.passive_tech.remove(tech)
    print(f" * Target passive tech changed damage (tech: {tech} multiplier: {bonus:,.2f})")
    return bonus

def bounce_passive_tech(player: Player, matched: list) -> float:
    tech = matched[0]

    extension = 1.40 if "EXTENDED" in tech.modifiers else 1
    high_jump = 1.30 if "HIGH-JUMP" in tech.modifiers else 1
    chain_mult = 1 + 0.20 * tech.chain_count

    bonus = 2 * high_jump * extension * chain_mult
    player.passive_tech.remove(tech)
    print(f" * Attacker passive tech decreased target parry effectiveness")
    return bonus

# active tech
def active_tech(player: Player, velocity_modifier: float) -> float:
    if player.active_tech is None:
        return velocity_modifier
    match player.active_tech.tech:
        case "SUPER" | "HYPER":
            velocity_modifier = super_hyper_active_tech(player, velocity_modifier)
        case "ULTRA":
            ultra_active_tech(player)
        case "B-HOP":
            velocity_modifier = bhop_active_tech(player, velocity_modifier)
        case "FALL-BOOST":
            fall_active_tech(player)
        case "BOUNCE-BOOST":
            bounce_active_tech(player)

    print(f" - {player.name}'s speed has been influenced via a {player.active_tech} active tech")
    player.transfer_active_tech()
    return velocity_modifier

def super_hyper_active_tech(player: Player, velocity_modifier: float) -> float:
    plr_dir_x, plr_dir_y = vector2_dir(player.speed)
    plr_dir_x = 1 if plr_dir_x == 0 else plr_dir_x

    tech = player.active_tech
    x, y = TECH_SPEED_LIB[tech.tech]

    extension = 1.45 if "EXTENDED" in tech.modifiers else 1
    slide = 1.55 if "SLIDE" in tech.modifiers else 1
    chain_mult = 1 + 1.10 * tech.chain_count

    hyper_boost_x = x * plr_dir_x * extension * slide * chain_mult
    hyper_boost_y = y * (1 / slide) * chain_mult
    hyper_boost = (hyper_boost_x, hyper_boost_y)

    player.speed = vector2_add(player.speed, hyper_boost)
    velocity_modifier /= slide
    return velocity_modifier

def ultra_active_tech(player: Player):
    tech = player.active_tech
    x, y = TECH_SPEED_LIB[tech.tech]

    extension = 2 * 0.50 if "EXTENDED" in tech.modifiers else 0
    chain_mult = 1 + 1.10 * tech.chain_count

    ultra_mult_x = (x + extension) * chain_mult
    ultra_mult_y = y * chain_mult
    ultra_mult = (ultra_mult_x, ultra_mult_y)

    player.speed = vector2_mult(player.speed, ultra_mult)

def bhop_active_tech(player: Player, velocity_modifier: float) -> float:
    plr_dir_x, plr_dir_y = vector2_dir(player.speed)

    tech = player.active_tech
    x, y = TECH_SPEED_LIB[tech.tech]

    extension = 1.2 if "EXTENDED" in tech.modifiers else 1
    high_jump = 0.85 if "HIGH-JUMP" in tech.modifiers else 0
    chain_mult = 1 + 1.10 * tech.chain_count

    b_hop_boost_x = x * plr_dir_x * extension * chain_mult
    b_hop_boost_y = (y + high_jump) * extension * chain_mult
    b_hop_boost = (b_hop_boost_x, b_hop_boost_y)

    player.speed = vector2_add(player.speed, b_hop_boost)
    velocity_modifier /= (1.25 + (extension // 3) + (high_jump // 3))
    return velocity_modifier

def fall_active_tech(player: Player):
    plr_dir_x, plr_dir_y = vector2_dir(player.speed)
    plr_dir_x *= -1  # inverting, FALL-BOOST decreases horizontal speed

    tech = player.active_tech
    x, y = TECH_SPEED_LIB[tech.tech]

    slow_fall = 0.80 if "SLOW-FALL" in tech.modifiers else 1
    fast_fall = 1.50 if "FAST-FALL" in tech.modifiers else 1
    chain_mult = 1 + 1.10 * tech.chain_count

    fall_boost_x = x * plr_dir_x * chain_mult
    fall_boost_y = y * slow_fall * fast_fall * chain_mult
    fall_boost = (fall_boost_x, fall_boost_y)

    player.speed = vector2_add(player.speed, fall_boost)

    if slow_fall > 1:
        player.defending += 1
        print(f" - {player.name}'s defense stacks have been increased by 1 via slow-falling")
    elif fast_fall > 1:
        def_change = 1 if player.defending >= 1 else 0
        player.defending -= def_change
        print(f" - {player.name}'s defense stacks have been decreased by {def_change} via fast-falling")

def bounce_active_tech(player: Player):
    plr_dir_x, plr_dir_y = vector2_dir(player.speed)
    plr_dir_x *= -1  # inverting, BOUNCE-BOOST decreases horizontal speed

    tech = player.active_tech
    x, y = TECH_SPEED_LIB[tech.tech]

    extension = 0.70 if "EXTENDED" in tech.modifiers else 0
    high_jump = 0.85 if "HIGH-JUMP" in tech.modifiers else 0
    chain_mult = 1 + 1.10 * tech.chain_count

    bounce_boost_x = (x - extension) * plr_dir_x * chain_mult
    bounce_boost_y = y * (1 + extension + high_jump) * chain_mult
    bounce_boost = (bounce_boost_x, bounce_boost_y)

    player.speed = vector2_add(player.speed, bounce_boost)

    if high_jump > 0:
        def_change = int(bounce_boost_y // SPEED_IMPACT)
        def_change = def_change if player.defending > def_change else player.defending
        player.defending -= def_change
        print(f" - {player.name}'s defense stacks have been decreased by {def_change} via high-jumping")