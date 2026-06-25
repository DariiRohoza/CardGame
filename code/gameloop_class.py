from math import ceil
from pyfiglet import figlet_format
from pyinputplus import inputInt
from time import sleep

from attack_func import evaluate_card, evaluate_multipliers, attack_player
from movement_func import chunk_split_movement, evaluate_movement_chunks, evaluate_tech_list, get_tech_modifiers, get_player_passive
from passive_tech import super_hyper_passive_tech, bhop_passive_tech
from printing_func import print_hand, print_players, print_movement_table
from vector2_func import vector2_add, vector2_mult, vector2_dir, vector2_decay

from card_class import Card
from deck_class import Deck
from player_class import Player
from constants_libraries import (STYLE_LIB, SUIT_LIB, MOVEMENT_LIB, TECH_SPEED_LIB,
                                 MIN_GENERATED_CARD_RANK, MIN_GAME_PLAYERS, MAX_GAME_PLAYERS, PLAYER_HAND_SIZE,
                                 STACK_RANK_LIMIT, PARRY_LONGEVITY, SUIT_PENALTY, IDENTICAL_BOOST, MIN_MOVE, SPEED_IMPACT)


class GameLoop:
    def __init__(self):
        self.player_list: list[Player] = []
        self.counter: int = 0
        self.action_counter: int = 0
        self.deck: Deck = Deck()
        self.conclude_game: bool = False

    def __str__(self):
        return f"A game with {len(self.player_list)} players"

    def initialize_game(self):
        if len(self.player_list) < MIN_GAME_PLAYERS:
            print(f"Insufficient players, skipping...")
        else:
            print(f"All requirements have been fulfilled, the game is starting...")
            self.deck.fill()

            for item in self.player_list:
                for _ in range(PLAYER_HAND_SIZE):
                    item.hand.append(self.deck.draw_card())

    def add_player(self, new_player: Player):
        if len(self.deck) != 0:
            print(f"Deck has been initialized, can't add more players, skipping...")
        elif len(self.player_list) == MAX_GAME_PLAYERS:
            print(f"Player limit reached, can't add more players, skipping...")
        elif new_player.hand:
            print(f"Player hand needs to be empty to be added, skipping...")
        else:
            self.player_list.append(new_player)

    def main_loop(self):
        while not self.conclude_game:
            sleep(0.35)
            velocity_modifier = 1
            no_decay = False
            if len(self.deck) == 0:
                self.deck.fill()
                self.deck.shuffle()
                print(f"--<  Refilled Deck  >--\n")

            curr_player, curr_hand = self.fetch_curr()

            print(f">>> It is now {curr_player.name}'s turn\n\n"
                  f"Pick an options from those below by inputting the number in front of it\n"
                  f"00 : Conclude Game / Quit\n"
                  f"01 : Attack Player\n"
                  f"02 : Stack Attack Value\n"
                  f"03 : Start a Parry\n"
                  f"04 : Refurbish Card Suit\n"
                  f"05 : Increase Card Rank\n"
                  f"06 : Merge Card Rank\n"
                  f"07 : Stylize Card\n"
                  f"08 : Exchange half of your hand\n"
                  f"09 : Defend\n"
                  f"10 : Move\n"
                  f"11 : View Other Players\n"
                  f"12 : View Hand\n")

            user_choice_option = inputInt(prompt="User input: ", min=0, max=12)

            match user_choice_option:
                case 0:
                    if input(f" - Type \"quit\" to stop the program: ").lower() == "quit":
                        self.conclude_game = True

                case 1: self.attack_turn(curr_player, curr_hand)
                case 2: self.stack_attack_value(curr_player, curr_hand)
                case 3: self.player_parry(curr_player, curr_hand)
                case 4: self.refurbish_card_suit(curr_player, curr_hand)
                case 5: self.increase_card_rank(curr_player, curr_hand)
                case 6: self.merge_card_rank(curr_player, curr_hand)
                case 7: self.stylize_card(curr_player, curr_hand)
                case 8: self.drop_half_cards(curr_player, curr_hand)
                case 9: self.defend(curr_player, 2)
                case 10: velocity_modifier = self.move_player(curr_player)
                case 11: print_players(self.player_list, curr_player)
                case 12: print_hand(curr_player, curr_hand)

            if 0 <= user_choice_option <= 10:
                self.iterate_turn()

            if len(self.player_list) == 1:
                print(f" > A winner has been found!\n")
                self.conclude_game = True
                game_winner(self.player_list[0])

            if curr_player.speed_value() > 0 and self.action_counter == 0 and not no_decay:
                vector2_decay(curr_player, velocity_modifier, velocity_modifier)
                print(f">>> Applied velocity decay to {curr_player.name}\n")

            if curr_player.parry_time > 0 and self.action_counter == 0:
                curr_player.parry_time -= 1

            if curr_player.parry_time == 0 and curr_player.parry_card is not None:
                parry_card = curr_player.parry_card
                curr_player.parry_card = None
                print(f" - {curr_player.name}'s parry card expired : {parry_card}\n")

    # ── MainLoop Util / Helper Functions ──────────────────────────────
    def iterate_turn(self):
        self.action_counter += 1
        if self.action_counter >= self.player_list[self.counter].action_count:
            self.counter += 1
            self.action_counter = 0
        self.counter %= len(self.player_list)

    def fetch_curr(self):
        curr_player = self.player_list[self.counter]
        curr_hand = curr_player.hand
        return curr_player, curr_hand

    # ── MainLoop SubFunctions ──────────────────────────────
    def attack_turn(self, curr_player: Player, curr_hand: list[Card]):
        print(f">>> It is now {curr_player.name}'s attack turn")
        print(f" > Pick a card to attack with")
        user_chosen_card = card_choosing(curr_player, curr_hand)

        print(f" > Pick a target for your attack")
        print_players(self.player_list, curr_player)
        while True:
            target_idx: int = inputInt(prompt="Pick a target player by their index : ", min=0, max=len(self.player_list)-1)
            user_chosen_target: Player = self.player_list[target_idx]
            print(f"The target you chose : {user_chosen_target}")
            if input(f"Input \"retry\" if you wish to pick a different target: ").lower() == "retry":
                continue
            break

        print(f" > {curr_player.name} has decided to attack {user_chosen_target.name} using: {user_chosen_card}")
        attack_player(user_chosen_card, curr_player, user_chosen_target)

        curr_hand.remove(user_chosen_card)
        curr_hand.append(self.deck.draw_card())

        if user_chosen_target.health <= 0.00:
            self.player_list.remove(user_chosen_target)
            print(f"Player {user_chosen_target.name} has been reduced to 0 or less hit points")

    def stack_attack_value(self, curr_player: Player, curr_hand: list[Card]) -> bool:
        filter_hand = []
        for item in curr_hand:
            if item.rank <= STACK_RANK_LIMIT:
                filter_hand.append(item)

        if len(filter_hand) == 0:
            print(f"You have no eligible cards to stack attack value (card rank must be < {STACK_RANK_LIMIT})\n"
                  f"This action didn't take a turn action")
            return False

        print(f" > Pick a card to stack attack value with")
        chosen_card = card_choosing(curr_player, filter_hand)
        curr_hand.remove(chosen_card)

        value, weakness_used, strength_used = evaluate_card(chosen_card, curr_player)
        evaluate_multipliers(curr_player, weakness_used, strength_used)

        matched_keys = get_player_passive(curr_player, "SUPER")
        if not matched_keys:
            matched_keys = get_player_passive(curr_player, "HYPER")
        if matched_keys:
            tech_bonus = super_hyper_passive_tech(curr_player, matched_keys)
            value += tech_bonus

        curr_player.attack_stack += value
        print(f" - Increased {curr_player.name} attack stack by {value:,.2f}\n")

        curr_hand.append(self.deck.draw_card())
        return True

    def player_parry(self, curr_player: Player, curr_hand: list[Card]) -> bool:
        print(f"Pick a card to be used as a parry against the next attack against you\n"
              f"The parry will expire after {PARRY_LONGEVITY} turns\n")
        if curr_player.parry_card is not None:
            print(f" - You already have a parry card set, it will be returned to your hand if you continue")
            if input(f"Input \"return\" if you wish to go back: ").lower() == "return":
                return False

        print(f" > Pick a card to start a parry with")
        user_card = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card)

        if curr_player.parry_card is not None:
            curr_hand.append(curr_player.parry_card)
            print(f" - {curr_player.name}'s parry card changed : {curr_player.parry_card} -> {user_card}\n")
        else:
            curr_hand.append(self.deck.draw_card())
            print(f" - {curr_player.name} gained a parry card : {user_card}\n")

        curr_player.parry_card = user_card
        curr_player.parry_time = PARRY_LONGEVITY
        return True

    def refurbish_card_suit(self, curr_player: Player, curr_hand: list[Card]):
        print(f" > Pick a card to be refurbished")
        user_card = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card)

        print(f"> Pick a target suit\n")
        for key, value in SUIT_LIB.items():
            print(f"{key} : {value}")
        while True:
            chosen_suit: int = inputInt(
                prompt=f"Pick a target suit by its index (Current suit : {SUIT_LIB[user_card.suit]}) : ",
                min=0, max=len(SUIT_LIB)-1
            )
            if user_card.suit == chosen_suit:
                print(f"New suit cannot be the same as initial suit, pick a different suit")
                continue
            print(f"The target you chose : {chosen_suit}")
            if input(f"Input \"retry\" if you wish to pick a different target: ").lower() == "retry":
                continue
            break

        if curr_player.weakness == SUIT_LIB[chosen_suit]:
            curr_player.weakness = ""
            print(f" - Cured player weakness at no cost")

        curr_player.strength = SUIT_LIB[chosen_suit]
        print(f" - Granted player strength with the chosen suit ({curr_player.strength})")

        new_card = Card()
        new_card.add_info(chosen_suit, user_card.rank, user_card.style)

        print(f"\n--> Changed suit card: {new_card}\n")
        curr_hand.append(new_card)

    def increase_card_rank(self, curr_player: Player, curr_hand: list[Card]):
        print(f" > Pick a card to increase rank of")
        user_card = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card)

        rank_change = MIN_GENERATED_CARD_RANK
        if curr_player.strength == SUIT_LIB[user_card.suit]:
            rank_change += 5
            curr_player.strength = ""
            print(f" - Nullified player strength for a higher ranked card")

        speed_bonus = 3 * ceil(2 * curr_player.speed_value() // SPEED_IMPACT)
        if speed_bonus > 0:
            rank_change += speed_bonus
            print(f" - Player speed increased the rank increase by ({speed_bonus})")

        new_card = Card()
        new_card.add_info(user_card.suit, user_card.rank + rank_change, user_card.style)

        print(f"\n--> Increased rank card: {new_card}\n")
        curr_hand.append(new_card)
        self.defend(curr_player, 1)

    def merge_card_rank(self, curr_player: Player, curr_hand: list[Card]):
        print(f"If the cards don't have the same suit, a penalty will be applied\n"
              f"If both cards have the same rank and suit, a bonus will be applied\n\n"
              f" > Pick a card to merge")
        user_card_1st = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card_1st)

        print(f" > Pick another card to merge")
        user_card_2nd = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card_2nd)

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
            final_rank = 1

        merged_card = Card()
        merged_card.add_info(user_card_1st.suit, final_rank, merged_style)

        print(f"\n--> Merged card: {merged_card}\n")
        curr_hand.append(merged_card)
        curr_hand.append(self.deck.draw_card())

    def stylize_card(self, curr_player: Player, curr_hand: list[Card]):
        print(f" > Pick a card to increase style of")
        user_card = card_choosing(curr_player, curr_hand)
        curr_hand.remove(user_card)

        new_style = user_card.style
        for key, value in STYLE_LIB.items():
            if value > STYLE_LIB[new_style]:
                new_style = key
                break

        new_card = Card()
        new_card.add_info(user_card.suit, user_card.rank, new_style)

        print(f"\n--> Increased style card: {new_card}\n")
        curr_hand.append(new_card)

    def drop_half_cards(self, curr_player: Player, curr_hand: list[Card]) -> bool:
        cards_removed = len(curr_hand) // 2
        modified: bool = False
        matched_keys = get_player_passive(curr_player, "B-HOP")
        if matched_keys:
            drop_bonus = bhop_passive_tech(curr_player, matched_keys, "drop_half_cards")
            if drop_bonus >= 1:
                modified = True

        for i in range(cards_removed):
            print(f"Choose a card to remove ({i}/{cards_removed} removed already)")
            user_card = card_choosing(curr_player, curr_hand)
            curr_hand.remove(user_card)
            if modified:
                curr_hand.append(self.deck.draw_card())
                print(f" - New card added to hand")
                if input("To stop dropping cards type \"stop\": ").lower():
                    break

        if not modified:
            for _ in range(cards_removed):
                curr_hand.append(self.deck.draw_card())
            print(f"{cards_removed} new cards have been added to your hand\n")
        return False

    def defend(self, curr_player: Player, def_stacks: int):
        matched_keys = get_player_passive(curr_player, "B-HOP")
        if matched_keys:
            def_bonus = bhop_passive_tech(curr_player, matched_keys, "defend")
            def_stacks += def_bonus

        curr_player.defending += def_stacks
        print(f"{curr_player.name} has gained {def_stacks} stack(s) of defense\n")

    def move_player(self, curr_player: Player) -> float:
        move_list = []
        velocity_modifier = 1
        max_moves = MIN_MOVE + int(curr_player.speed_value() // SPEED_IMPACT)
        print_movement_table()
        print(f"Input a movement sequence of moves from the \"Move\" column in the table above\n"
              f"Separate each input with a \",\" with a maximum of {max_moves} choices")

        while True:
            valid_entry = True
            move_seq = input("Input: ").upper()
            if len(move_seq) <= 0:
                print("Invalid length of input, try again...")
                continue
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

        prev_vector = curr_player.print_speed(True)
        prev_speed = curr_player.speed_value()

        movement_chunks = chunk_split_movement(move_list)
        tech_list = evaluate_movement_chunks(movement_chunks, curr_player)
        if len(tech_list) > 0:
            evaluate_tech_list(tech_list, curr_player)

        active_tech = curr_player.active_tech
        if "SUPER" in curr_player.active_tech or "HYPER" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = vector2_dir(curr_player.speed)
            plr_dir_x = 1 if plr_dir_x == 0 else plr_dir_x

            x, y = TECH_SPEED_LIB[active_tech]

            extension = 1.45 if "EXTENDED" in modifiers_list else 1
            slide = 1.55 if "SLIDE" in modifiers_list else 1
            chain_mult = 1 + 1.10 * chain_len

            hyper_boost_x = x * plr_dir_x * extension * slide * chain_mult
            hyper_boost_y = y * (extension // 2.4) * chain_mult
            hyper_boost = (hyper_boost_x, hyper_boost_y)

            curr_player.speed = vector2_add(curr_player.speed, hyper_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a {active_tech.lower()} active tech")
            curr_player.transfer_active_tech()
            velocity_modifier /= slide

        elif "ULTRA" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)

            x, y = TECH_SPEED_LIB[active_tech]

            extension = 2 * 0.50 if "EXTENDED" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            ultra_mult_x = (x + extension) * chain_mult
            ultra_mult_y = y * chain_mult
            ultra_mult = (ultra_mult_x, ultra_mult_y)

            curr_player.speed = vector2_mult(curr_player.speed, ultra_mult)
            print(f" - {curr_player.name}'s speed has been influenced via an ultra active tech")
            curr_player.transfer_active_tech()

        elif "B-HOP" in active_tech and curr_player.speed_value() > 0:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = vector2_dir(curr_player.speed)

            x, y = TECH_SPEED_LIB[active_tech]

            extension = 1.2 if "EXTENDED" in modifiers_list else 1
            high_jump = 0.85 if "HIGH-JUMP" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            b_hop_boost_x = x * plr_dir_x * extension * chain_mult
            b_hop_boost_y = (y + high_jump) * extension * chain_mult
            b_hop_boost = (b_hop_boost_x, b_hop_boost_y)

            curr_player.speed = vector2_add(curr_player.speed, b_hop_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a b-hop active tech")
            curr_player.transfer_active_tech()
            velocity_modifier /= (1.25 + (extension // 3) + (high_jump // 3))

        elif "FALL-BOOST" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = vector2_dir(curr_player.speed)
            plr_dir_x *= -1 # inverting, FALL-BOOST decreases horizontal speed

            x, y = TECH_SPEED_LIB[active_tech]

            slow_fall = 0.80 if "SLOW-FALL" in modifiers_list else 1
            fast_fall = 1.50 if "FAST-FALL" in modifiers_list else 1
            chain_mult = 1 + 1.10 * chain_len

            fall_boost_x = x * plr_dir_x * chain_mult
            fall_boost_y = y * slow_fall * fast_fall * chain_mult
            fall_boost = (fall_boost_x, fall_boost_y)

            curr_player.speed = vector2_add(curr_player.speed, fall_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a fall-boost active tech")
            curr_player.transfer_active_tech()

            if slow_fall > 1:
                curr_player.defending += 1
                print(f" - {curr_player.name}'s defense stacks have been increased by 1 via slow-falling")
            elif fast_fall > 1:
                def_change = 1 if curr_player.defending >= 1 else 0
                curr_player.defending -= def_change
                print(f" - {curr_player.name}'s defense stacks have been decreased by {def_change} via fast-falling")

        elif "BOUNCE-BOOST" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = vector2_dir(curr_player.speed)
            plr_dir_x *= -1  # inverting, BOUNCE-BOOST decreases horizontal speed

            x, y = TECH_SPEED_LIB[active_tech]

            extension = 0.70 if "EXTENDED" in modifiers_list else 0
            high_jump = 0.85 if "HIGH-JUMP" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            bounce_boost_x = (x - extension) * plr_dir_x * chain_mult
            bounce_boost_y = y * (1 + extension + high_jump) * chain_mult
            bounce_boost = (bounce_boost_x, bounce_boost_y)

            curr_player.speed = vector2_add(curr_player.speed, bounce_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a bounce-boost active tech")
            curr_player.transfer_active_tech()

            if high_jump > 0:
                def_change = int(bounce_boost_y // SPEED_IMPACT)
                def_change = def_change if curr_player.defending > def_change else curr_player.defending
                curr_player.defending -= def_change
                print(f" - {curr_player.name}'s defense stacks have been decreased by {def_change} via high-jumping")

        print(f"{curr_player.name}'s speed change:\n"
              f" --> {prev_vector} --> {curr_player.print_speed(True)}\n"
              f" --> {prev_speed:,.2f} m/s --> {curr_player.speed_value():,.2f} m/s\n")
        return velocity_modifier

# ── Util / Helper Functions ──────────────────────────────
def game_winner(winner: Player):
    print(f"The player that has eliminated all the other players and won is!\n",
          figlet_format(f"{winner.name}", font="larry3d"))

def card_choosing(p: Player, hand: list[Card]) -> Card:
    print_hand(curr_player=p, curr_hand=hand)
    card_idx: int = inputInt(prompt="Pick a card by its index : ", min=0, max=len(hand)-1)
    card: Card = hand[card_idx]
    return card