from math import ceil
from pyinputplus import inputInt

from attack_func import evaluate_card, evaluate_multipliers, attack_player
from movement_func import chunk_split_movement, evaluate_movement_chunks, evaluate_tech_list, get_tech_modifiers, get_player_passive
from passive_tech import super_hyper_passive_tech, bhop_passive_tech
from printing_func import print_hand, print_players, print_movement_table
from vector2_func import vector2_add, vector2_mult, vector2_dir

from card_class import Card
from player_class import Player
from constants_libraries import (STYLE_LIB, SUIT_LIB, MOVEMENT_LIB, TECH_SPEED_LIB, MOVEMENT_SHORTCUTS,
                                 INVERSION_BOOST_X, INVERSION_BOOST_Y, MIN_GENERATED_CARD_RANK, STACK_RANK_LIMIT,
                                 PARRY_LONGEVITY, SUIT_PENALTY, IDENTICAL_BOOST, MIN_MOVE, SPEED_IMPACT)


def attack_turn(player: Player, player_list: list[Player]):
    print(f">>> It is now {player.name}'s attack turn")
    print(f" > Pick a card to attack with")
    user_chosen_card = card_choosing(player, player.hand)

    print(f" > Pick a target for your attack")
    print_players(player_list, player)
    while True:
        target_idx: int = inputInt(prompt="Pick a target player by their index : ", min=0, max=len(player_list) - 1)
        target: Player = player_list[target_idx]
        print(f"The target you chose : {target}")
        if input(f"Input \"retry\" if you wish to pick a different target: ").lower() == "retry":
            continue
        break

    print(f" > {player.name} has decided to attack {target.name} using: {user_chosen_card}")
    attack_player(user_chosen_card, player, target)

    player.move_to_deck(user_chosen_card)
    player.hand.append(player.deck.draw_card())

    if target.health <= 0.00:
        idx = player_list.index(target)
        player_list.pop(idx)
        print(f"Player {target.name} has been reduced to 0 or less hit points by {player.name}")

def stack_attack_value(player: Player) -> bool:
    filter_hand = []
    for item in player.hand:
        if item.rank <= STACK_RANK_LIMIT:
            filter_hand.append(item)

    if len(filter_hand) == 0:
        print(f"You have no eligible cards to stack attack value (card rank must be < {STACK_RANK_LIMIT})\n"
              f"This action didn't take a turn action")
        return False

    print(f" > Pick a card to stack attack value with")
    chosen_card = card_choosing(player, filter_hand)
    player.move_to_deck(chosen_card)

    value, weakness_used, strength_used = evaluate_card(chosen_card, player)
    evaluate_multipliers(player, weakness_used, strength_used)

    matched_keys = get_player_passive(player, "SUPER")
    if not matched_keys:
        matched_keys = get_player_passive(player, "HYPER")
    if matched_keys:
        tech_bonus = super_hyper_passive_tech(player, matched_keys)
        value += tech_bonus

    player.attack_stack += value
    print(f" - Increased {player.name} attack stack by {value:,.2f}\n")

    player.hand.append(player.deck.draw_card())
    return True

def player_parry(player: Player) -> bool:
    print(f"Pick a card to be used as a parry against the next attack against you\n"
          f"The parry will expire after {PARRY_LONGEVITY} turns\n")
    if player.parry_card is not None:
        print(f" - You already have a parry card set, it will be returned to your hand if you continue")
        if input(f"Input \"return\" if you wish to go back: ").lower() == "return":
            return False

    print(f" > Pick a card to start a parry with")
    user_card = card_choosing(player, player.hand)
    player.move_to_deck(user_card)

    if player.parry_card is not None:
        player.hand.append(player.parry_card)
        print(f" - {player.name}'s parry card changed : {player.parry_card} -> {user_card}\n")
    else:
        player.hand.append(player.deck.draw_card())
        print(f" - {player.name} gained a parry card : {user_card}\n")

    player.parry_card = user_card
    player.parry_time = PARRY_LONGEVITY
    return True

def refurbish_card_suit(player: Player):
    print(f" > Pick a card to be refurbished")
    user_card = card_choosing(player, player.hand)
    player.move_to_deck(user_card)

    print(f"> Pick a target suit")
    for key, value in SUIT_LIB.items():
        print(f"{key} : {value}")
    while True:
        chosen_suit: int = inputInt(
            prompt=f"Pick a target suit by its index (Current suit : {SUIT_LIB[user_card.suit]}) : ",
            min=0, max=len(SUIT_LIB) - 1
        )
        if user_card.suit == chosen_suit:
            print(f"New suit cannot be the same as initial suit, pick a different suit")
            continue
        print(f"The target you chose : {chosen_suit}")
        if input(f"Input \"retry\" if you wish to pick a different target: ").lower() == "retry":
            continue
        break

    if player.weakness == SUIT_LIB[chosen_suit]:
        player.weakness = ""
        print(f" - Cured player weakness at no cost")

    player.strength = SUIT_LIB[chosen_suit]
    print(f" - Granted player strength with the chosen suit ({player.strength})")

    new_card = Card()
    new_card.add_info(chosen_suit, user_card.rank, user_card.style)

    print(f"\n--> Changed suit card: {new_card}\n")
    player.hand.append(new_card)

def increase_card_rank(player: Player):
    print(f" > Pick a card to increase rank of")
    user_card = card_choosing(player, player.hand)
    player.move_to_deck(user_card)

    rank_change = MIN_GENERATED_CARD_RANK
    if player.strength == SUIT_LIB[user_card.suit]:
        rank_change += 5
        player.strength = ""
        print(f" - Nullified player strength for a higher ranked card")

    speed_bonus = 3 * ceil(2 * player.speed_value() // SPEED_IMPACT)
    if speed_bonus > 0:
        rank_change += speed_bonus
        print(f" - Player speed increased the rank increase by ({speed_bonus})")

    new_card = Card()
    new_card.add_info(user_card.suit, user_card.rank + rank_change, user_card.style)

    print(f"\n--> Increased rank card: {new_card}\n")
    player.hand.append(new_card)
    defend(player, 1)

def merge_card_rank(player: Player):
    print(f"If the cards don't have the same suit, a penalty will be applied\n"
          f"If both cards have the same rank and suit, a bonus will be applied\n\n"
          f" > Pick a card to merge")
    user_card_1st = card_choosing(player, player.hand)
    player.move_to_deck(user_card_1st)

    print(f" > Pick another card to merge")
    user_card_2nd = card_choosing(player, player.hand)
    player.move_to_deck(user_card_2nd)

    rank_change = 0
    if user_card_1st.suit != user_card_2nd.suit:
        rank_change += SUIT_PENALTY
        print(f" - Applied suit penalty to the result ({SUIT_PENALTY})")
    elif user_card_2nd.suit == user_card_1st.suit and user_card_2nd.rank == user_card_1st.rank:
        rank_change += IDENTICAL_BOOST
        print(f" - Applied identicality boost to the result ({IDENTICAL_BOOST})")

    if STYLE_LIB[user_card_1st.style] > STYLE_LIB[user_card_2nd.style]:
        merged_style = user_card_1st.style
    else:
        merged_style = user_card_2nd.style

    final_rank = user_card_1st.rank + user_card_2nd.rank + rank_change
    if final_rank <= 0:
        final_rank = MIN_GENERATED_CARD_RANK

    merged_card = Card()
    merged_card.add_info(user_card_1st.suit, final_rank, merged_style)

    print(f"\n--> Merged card: {merged_card}\n")
    player.hand.append(merged_card)
    player.hand.append(player.deck.draw_card())

def stylize_card(player: Player):
    print(f" > Pick a card to increase style of")
    user_card = card_choosing(player, player.hand)
    player.move_to_deck(user_card)

    new_style = user_card.style
    for key, value in STYLE_LIB.items():
        if value > STYLE_LIB[new_style]:
            new_style = key
            break

    new_card = Card()
    new_card.add_info(user_card.suit, user_card.rank, new_style)

    print(f"\n--> Increased style card: {new_card}\n")
    player.hand.append(new_card)

def drop_half_cards(player: Player) -> bool:
    cards_removed = len(player.hand) // 2
    modified: bool = False
    matched_keys = get_player_passive(player, "B-HOP")
    if matched_keys:
        drop_bonus = bhop_passive_tech(player, matched_keys, "drop_half_cards")
        if drop_bonus >= 1:
            modified = True

    for i in range(cards_removed):
        print(f"Choose a card to remove ({i}/{cards_removed} removed already)")
        user_card = card_choosing(player, player.hand)
        player.move_to_deck(user_card)
        if modified:
            player.hand.append(player.deck.draw_card())
            print(f" - New card added to hand")
            if input("To stop dropping cards type \"stop\": ").lower():
                break

    if not modified:
        for _ in range(cards_removed):
            player.hand.append(player.deck.draw_card())
        print(f"{cards_removed} new cards have been added to your hand\n")
    return False

def defend(player: Player, def_stacks: int):
    matched_keys = get_player_passive(player, "B-HOP")
    if matched_keys:
        def_bonus = bhop_passive_tech(player, matched_keys, "defend")
        def_stacks += def_bonus

    player.defending += def_stacks
    print(f"{player.name} has gained {def_stacks} stack(s) of defense\n")

def move_player(player: Player) -> float:
    move_list = []
    velocity_modifier = 1
    max_moves = MIN_MOVE + int(player.speed_value() // SPEED_IMPACT)
    print_movement_table()
    print(f"Input a movement sequence of moves from the \"Move\" column in the table above\n"
          f"Separate each input with a \",\" with a maximum of {max_moves} choices")

    while True:
        valid_entry = True
        move_seq = input("Input: ").upper()
        if len(move_seq) <= 0:
            print("Invalid length of input, try again...")
            continue
        for k, v in MOVEMENT_SHORTCUTS.items():
            move_seq = move_seq.replace(k, v)

        move_list = move_seq.split(",")
        if not 0 < len(move_list) <= max_moves:
            print(f"Invalid selection length, keep amount of actions under {max_moves}, try again...")
            continue
        for idx, item in enumerate(move_list):
            item = item.strip()
            move_list[idx] = item
            if item not in MOVEMENT_LIB.keys():
                print(f"Problematic item: {item}, Invalid structure, example: STALL,DASH-DOWN-LEFT,JUMP,...")
                valid_entry = False

        if not valid_entry:
            continue
        break

    prev_vector = player.print_speed(units=True)
    prev_speed = player.speed_value()
    prev_dir = vector2_dir(vector=player.speed)

    movement_chunks = chunk_split_movement(move_list)
    tech_list = evaluate_movement_chunks(movement_chunks, player)
    if len(tech_list) > 0:
        evaluate_tech_list(tech_list, player)

    active_tech = player.active_tech
    if "SUPER" in player.active_tech or "HYPER" in active_tech:
        active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
        plr_dir_x, plr_dir_y = vector2_dir(player.speed)
        plr_dir_x = 1 if plr_dir_x == 0 else plr_dir_x

        x, y = TECH_SPEED_LIB[active_tech]

        extension = 1.45 if "EXTENDED" in modifiers_list else 1
        slide = 1.55 if "SLIDE" in modifiers_list else 1
        chain_mult = 1 + 1.10 * chain_len

        hyper_boost_x = x * plr_dir_x * extension * slide * chain_mult
        hyper_boost_y = y * (extension // 2.4) * chain_mult
        hyper_boost = (hyper_boost_x, hyper_boost_y)

        player.speed = vector2_add(player.speed, hyper_boost)
        print(f" - {player.name}'s speed has been influenced via a {active_tech.lower()} active tech")
        player.transfer_active_tech()
        velocity_modifier /= slide

    elif "ULTRA" in active_tech:
        active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)

        x, y = TECH_SPEED_LIB[active_tech]

        extension = 2 * 0.50 if "EXTENDED" in modifiers_list else 0
        chain_mult = 1 + 1.10 * chain_len

        ultra_mult_x = (x + extension) * chain_mult
        ultra_mult_y = y * chain_mult
        ultra_mult = (ultra_mult_x, ultra_mult_y)

        player.speed = vector2_mult(player.speed, ultra_mult)
        print(f" - {player.name}'s speed has been influenced via an ultra active tech")
        player.transfer_active_tech()

    elif "B-HOP" in active_tech and player.speed_value() > 0:
        active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
        plr_dir_x, plr_dir_y = vector2_dir(player.speed)

        x, y = TECH_SPEED_LIB[active_tech]

        extension = 1.2 if "EXTENDED" in modifiers_list else 1
        high_jump = 0.85 if "HIGH-JUMP" in modifiers_list else 0
        chain_mult = 1 + 1.10 * chain_len

        b_hop_boost_x = x * plr_dir_x * extension * chain_mult
        b_hop_boost_y = (y + high_jump) * extension * chain_mult
        b_hop_boost = (b_hop_boost_x, b_hop_boost_y)

        player.speed = vector2_add(player.speed, b_hop_boost)
        print(f" - {player.name}'s speed has been influenced via a b-hop active tech")
        player.transfer_active_tech()
        velocity_modifier /= (1.25 + (extension // 3) + (high_jump // 3))

    elif "FALL-BOOST" in active_tech:
        active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
        plr_dir_x, plr_dir_y = vector2_dir(player.speed)
        plr_dir_x *= -1  # inverting, FALL-BOOST decreases horizontal speed

        x, y = TECH_SPEED_LIB[active_tech]

        slow_fall = 0.80 if "SLOW-FALL" in modifiers_list else 1
        fast_fall = 1.50 if "FAST-FALL" in modifiers_list else 1
        chain_mult = 1 + 1.10 * chain_len

        fall_boost_x = x * plr_dir_x * chain_mult
        fall_boost_y = y * slow_fall * fast_fall * chain_mult
        fall_boost = (fall_boost_x, fall_boost_y)

        player.speed = vector2_add(player.speed, fall_boost)
        print(f" - {player.name}'s speed has been influenced via a fall-boost active tech")
        player.transfer_active_tech()

        if slow_fall > 1:
            player.defending += 1
            print(f" - {player.name}'s defense stacks have been increased by 1 via slow-falling")
        elif fast_fall > 1:
            def_change = 1 if player.defending >= 1 else 0
            player.defending -= def_change
            print(f" - {player.name}'s defense stacks have been decreased by {def_change} via fast-falling")

    elif "BOUNCE-BOOST" in active_tech:
        active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
        plr_dir_x, plr_dir_y = vector2_dir(player.speed)
        plr_dir_x *= -1  # inverting, BOUNCE-BOOST decreases horizontal speed

        x, y = TECH_SPEED_LIB[active_tech]

        extension = 0.70 if "EXTENDED" in modifiers_list else 0
        high_jump = 0.85 if "HIGH-JUMP" in modifiers_list else 0
        chain_mult = 1 + 1.10 * chain_len

        bounce_boost_x = (x - extension) * plr_dir_x * chain_mult
        bounce_boost_y = y * (1 + extension + high_jump) * chain_mult
        bounce_boost = (bounce_boost_x, bounce_boost_y)

        player.speed = vector2_add(player.speed, bounce_boost)
        print(f" - {player.name}'s speed has been influenced via a bounce-boost active tech")
        player.transfer_active_tech()

        if high_jump > 0:
            def_change = int(bounce_boost_y // SPEED_IMPACT)
            def_change = def_change if player.defending > def_change else player.defending
            player.defending -= def_change
            print(f" - {player.name}'s defense stacks have been decreased by {def_change} via high-jumping")

    curr_dir = vector2_dir(vector=player.speed)
    if prev_dir[0] != curr_dir[0] and prev_dir[0] != 0 and curr_dir[0] != 0:
        dir_changed: int = 0
    elif prev_dir[1] != curr_dir[1] and prev_dir[1] != 0 and curr_dir[1] != 0:
        dir_changed: int = 1
    else:
        dir_changed: int = -1

    if prev_speed < player.speed_value() and dir_changed in [0, 1]:
        dv = INVERSION_BOOST_X if dir_changed == 0 else INVERSION_BOOST_Y
        player.speed = vector2_mult(player.speed, dv)
        print(f" - {player.name} performed and INVERSION BOOST, multipliers (x: {dv[0]}, y: {dv[1]})")

    print(f"{player.name}'s speed change:\n"
          f" --> {prev_vector} --> {player.print_speed(units=True)}\n"
          f" --> {prev_speed:,.2f} m/s --> {player.speed_value():,.2f} m/s\n")
    return velocity_modifier

def card_choosing(p: Player, hand: list[Card]) -> Card:
    print_hand(player=p, hand=hand)
    card_idx: int = inputInt(prompt="Pick a card by its index : ", min=0, max=len(hand)-1)
    card: Card = hand[card_idx]
    return card