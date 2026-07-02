from math import ceil
from pyinputplus import inputInt
from re import sub, escape

from attack_func import evaluate_card, evaluate_multipliers, attack_player
from movement_func import chunk_split_movement, evaluate_movement_chunks, evaluate_tech_list, get_player_passive
from printing_func import print_hand, print_players, print_movement_table
from tech_func import super_hyper_passive_tech, bhop_passive_tech, active_tech
from vector2_func import vector2_mult, vector2_dir

from card_class import Card
from player_class import Player
from constants_libraries import (STYLE_LIB, SUIT_LIB, MOVEMENT_LIB, MOVEMENT_SHORTCUTS,
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

    print(f"\n > {player.name} has decided to attack {target.name} using: {user_chosen_card}")
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
    player.hand.remove(user_card)

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
        print(f"The suit you chose : {chosen_suit}")
        if input(f"Input \"retry\" if you wish to pick a different suit: ").lower() == "retry":
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
    player.hand.remove(user_card)

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
    player.hand.remove(user_card_1st)

    print(f" > Pick another card to merge")
    user_card_2nd = card_choosing(player, player.hand)
    player.hand.remove(user_card_2nd)

    if evaluate_card(user_card_1st, player)[0] > evaluate_card(user_card_2nd, player)[0]:
        player.hand.append(user_card_1st)
        player.move_to_deck(user_card_1st) 
    else:
        player.hand.append(user_card_2nd)
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
    player.hand.remove(user_card)

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
        drop_bonus = bhop_passive_tech(player, matched_keys, use="drop_half_cards")
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
        def_bonus = bhop_passive_tech(player, matched_keys, use="defend")
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
            move_seq = sub(escape(k) + r'(?!-)', v, move_seq)

        move_list = [item.strip() for item in move_seq.split(",") if item.strip()]
        if not 0 < len(move_list) <= max_moves:
            print(f"Invalid selection length, keep amount of actions under {max_moves}, try again...")
            continue
        for idx, item in enumerate(move_list):
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

    velocity_modifier = active_tech(player, velocity_modifier)

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