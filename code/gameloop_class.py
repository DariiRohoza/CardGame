from rich import box
from rich.console import Console
from rich.table import Table

from math import tanh, cosh

from pyfiglet import figlet_format

from card_class import Card
from deck_class import Deck
from player_class import Player
from constants_libraries import (STYLE_LIB, SUIT_LIB, MOVEMENT_LIB, MOVEMENT_TECH_LIB,
                                 MAX_ACTIVE_TECH_LEN, CARD_PRINT, PLAYER_PRINT, MOVEMENT_PRINT,
                                 MIN_GENERATED_CARD_RANK, MIN_GAME_PLAYERS, MAX_GAME_PLAYERS, PLAYER_HAND_SIZE,
                                 STACK_RANK_LIMIT, SUIT_PENALTY, IDENTICAL_BOOST,
                                 MIN_MOVE, SPEED_IMPACT, VELOCITY_DECAY_X, VELOCITY_DECAY_Y,
                                 DEFENSE_STRENGTH_LIM, DEFENSE_WEAKNESS_LIM, DEFENSE_THRESHOLD, MIN_WEAKNESS_CRITICAL)

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
        # Checking conditions
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
            velocity_modifier = 1
            no_decay = False
            if len(self.deck) == 0:
                self.deck.fill()
                self.deck.shuffle()
                print(f"--<  Refilled Deck  >--\n")

            curr_player, curr_hand = self.fetch_curr()

            print(f">>> It is now {curr_player.name}'s turn\n\n"
                  f"Pick an options from those below by inputting the number in front of it\n"
                  f"01 : Attack Player\n"
                  f"11 : Stack Attack Value\n"
                  f"02 : View Other Players\n"
                  f"03 : View Hand\n"
                  f"04 : Refurbish Card Suit\n"
                  f"05 : Increase Card Rank\n"
                  f"06 : Merge Card Rank\n"
                  f"07 : Stylize Card\n"
                  f"08 : Exchange half of your hand\n"
                  f"09 : Defend\n"
                  f"10 : Move\n"
                  f"quit : Conclude Game / Quit\n")

            user_choice_option = input(f"Input your choice: ").strip().lstrip("0")

            match user_choice_option:
                case "1": self.attack_turn(curr_player, curr_hand)
                case "11": self.stack_attack_value(curr_player, curr_hand)
                case "2": print_players(self.player_list, curr_player)
                case "3": print_hand(curr_player, curr_hand)
                case "4": self.refurbish_card_suit(curr_player, curr_hand)
                case "5": self.increase_card_rank(curr_player, curr_hand)
                case "6": self.merge_card_rank(curr_player, curr_hand)
                case "7": self.stylize_card(curr_player, curr_hand)
                case "8": self.drop_half_cards(curr_player, curr_hand)
                case "9": self.defend(curr_player, 2)
                case "10": velocity_modifier = self.move_player(curr_player)

                case "quit" | "QUIT":
                    self.conclude_game = True
                case _:
                    print(f"Invalid input, try again...\n")
                    no_decay = True

            if curr_player.speed_value() > 0 and self.action_counter == 0 and not no_decay:
                apply_velocity_decay(curr_player, velocity_modifier, velocity_modifier)
                print(f">>> Applied velocity decay to {curr_player.name}\n")

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
        user_chosen_target = None

        print(f">>> It is now {curr_player.name}'s attack turn")
        print(f"Pick a card from your hand by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_chosen_card = card_choosing(curr_hand)

        print(f"Please select a player to attack from the following options by inputting the number in front of them")
        print_players(self.player_list, curr_player)

        while True:
            try:
                user_choice_player = int(input(f"Input your number of choice: "))
                if user_choice_player < 0:
                    print(f"Please use positive numbers!")
                    continue
            except ValueError:
                print(f"The input is of invalid type, skipping...")
                continue
            try:
                user_chosen_target = self.player_list[user_choice_player]
            except IndexError:
                print(f"The input is out of range, skipping...")
                continue
            print(f"The target you chose : {user_chosen_target}")
            user_in = input(f"Input \"retry\" if you wish to pick a different target: ")
            if user_in.lower() == "retry":
                continue
            break

        if user_chosen_target is not None and user_chosen_card is not None:
            print(f"{curr_player.name} has decided to attack {user_chosen_target.name} using: {user_chosen_card}")

            attack_player(user_chosen_card, curr_player, user_chosen_target)

            curr_hand.remove(user_chosen_card)
            curr_hand.append(self.deck.draw_card())

            if user_chosen_target.health <= 0.00:
                self.player_list.remove(user_chosen_target)
                print(f"Player {user_chosen_target.name} has been reduced to 0 or less hit points")

            if len(self.player_list) == 1:
                print(f"A winner has been found!\n")
                self.conclude_game = True
                game_winner(self.player_list[0])

        self.iterate_turn()

    def stack_attack_value(self, curr_player: Player, curr_hand: list[Card]) -> bool:
        tech_bonus = 0
        filter_hand = []
        for item in curr_hand:
            if item.rank <= STACK_RANK_LIMIT:
                filter_hand.append(item)

        if len(filter_hand) == 0:
            print(f"You have no eligible cards to stack attack value (card rank must be < {STACK_RANK_LIMIT})\n"
                  f"This action didn't take a turn action")
            return False

        print(f"Choose a card from the eligible below to stack their attack value by inputting the number in front of it")
        print_hand(curr_player, filter_hand)
        chosen_card = card_choosing(filter_hand)
        curr_hand.remove(chosen_card)
        value, weakness_used, strength_used = evaluate_card(chosen_card, curr_player)
        evaluate_multipliers(curr_player, weakness_used, strength_used)

        matched_keys = get_player_passive(curr_player, "SUPER")
        if not matched_keys:
            matched_keys = get_player_passive(curr_player, "HYPER")

        if matched_keys:
            tech, chain = matched_keys[0]
            full_tech = tech + " \\ " + chain if chain != "" else tech
            passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

            extension = 1 if "EXTENDED" in modifiers_list else 0
            slide = 1.3 if "SLIDE" in modifiers_list else 1
            chain_mult = 1 + 1.10 * chain_len

            tech_bonus = (1 + extension) * chain_mult * slide
            print(f" - {curr_player.name}'s passive tech increased attack stack"
                  f"(tech: {full_tech} bonus: {tech_bonus:,.2f})")
            del curr_player.passive_tech[tech]

        curr_player.attack_stack += value + tech_bonus
        print(f" - Increased {curr_player.name} attack stack by {value} (total change: {value + tech_bonus:,.2f})\n")

        curr_hand.append(self.deck.draw_card())
        self.iterate_turn()
        return True

    def refurbish_card_suit(self, curr_player: Player, curr_hand: list[Card]):
        print(f"Pick a card to be refurbished from your hand by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_card = card_choosing(curr_hand)
        curr_hand.remove(user_card)

        print(f"Please select a target suit from the following options by inputting the number in front of it")
        for key, value in SUIT_LIB.items():
            if key != user_card.suit:
                print(f"{key} : {value}")
            else:
                print(f"{key} : {value} > CURRENT SUIT")

        user_choice_suit = 0
        while True:
            try:
                user_choice_suit = int(input(f"Input your choice: "))
            except ValueError:
                print(f"The input is of invalid type, try again...")
                continue
            if user_choice_suit not in SUIT_LIB.keys():
                print(f"The input is out of range, try again...")
                continue
            elif user_choice_suit == user_card.suit:
                print(f"The target suit has to be different from the starting suit, try again...")
                continue
            break

        if curr_player.weakness == SUIT_LIB[user_choice_suit]:
            curr_player.weakness = ""
            print(f" - Cured player weakness at no cost")

        curr_player.strength = SUIT_LIB[user_choice_suit]
        print(f" - Granted player strength with the chosen suit ({curr_player.strength})")

        new_card = Card()
        new_card.add_info(user_choice_suit, user_card.rank, user_card.style)

        print(f"\n--> Changed suit card: {new_card}\n")
        curr_hand.append(new_card)
        self.iterate_turn()

    def increase_card_rank(self, curr_player: Player, curr_hand: list[Card]):
        print(f"Pick a card to increase rank of from your hand by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_card = card_choosing(curr_hand)
        curr_hand.remove(user_card)

        rank_change = MIN_GENERATED_CARD_RANK
        if curr_player.strength == SUIT_LIB[user_card.suit]:
            rank_change += 5
            curr_player.strength = ""
            print(f" - Nullified player strength for a higher ranked card")

        speed_bonus = int(2 * curr_player.speed_value() // SPEED_IMPACT)
        if speed_bonus > 0:
            rank_change += speed_bonus
            print(f" - Player speed increased the rank increase by ({speed_bonus})")

        new_card = Card()
        new_card.add_info(user_card.suit, user_card.rank + rank_change, user_card.style)

        print(f"\n--> Increased rank card: {new_card}\n")
        curr_hand.append(new_card)
        self.defend(curr_player, 1) # also handles the iterate_turn()

    def merge_card_rank(self, curr_player: Player, curr_hand: list[Card]):
        print(f"The first card you pick is going to be the target while the second is the one going to be merged\n"
              f"--> If the 2 cards selected have different suits, the result will have a penalty of 3 subtracted\n\n"
              f"Pick a target card from your hand by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_card_1st = card_choosing(curr_hand)
        curr_hand.remove(user_card_1st)

        print(f"Pick the card that is to be merged to your first pick by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_card_2nd = card_choosing(curr_hand)
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

        merged_card = Card()
        merged_card.add_info(user_card_1st.suit, user_card_1st.rank + user_card_2nd.rank + rank_change, merged_style)

        print(f"\n--> Merged card: {merged_card}\n")
        curr_hand.append(merged_card)
        curr_hand.append(self.deck.draw_card())
        self.iterate_turn()

    def stylize_card(self, curr_player: Player, curr_hand: list[Card]):
        print(f"Pick a card to increase style of from your hand by inputting the number in front of it")
        print_hand(curr_player, curr_hand)
        user_card = card_choosing(curr_hand)
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
        self.iterate_turn()

    def drop_half_cards(self, curr_player: Player, curr_hand: list[Card]):
        cards_removed = len(curr_hand) // 2
        for i in range(cards_removed):
            print(f"Choose a card to remove ({i}/{cards_removed} removed already)")
            print_hand(curr_player, curr_hand)
            user_card = card_choosing(curr_hand)
            curr_hand.remove(user_card)

        for _ in range(cards_removed):
            curr_hand.append(self.deck.draw_card())
        print(f"{cards_removed} new cards have been added to your hand\n")
        self.iterate_turn()

    def defend(self, curr_player: Player, def_stacks: int):
        curr_player.defending += def_stacks
        print(f"{curr_player.name} has gained {def_stacks} stack(s) of defense\n")
        self.iterate_turn()

    def move_player(self, curr_player: Player) -> float:
        print_movement_table()
        move_list = []
        velocity_modifier = 1
        max_moves = MIN_MOVE + int(curr_player.speed_value() // SPEED_IMPACT)
        print(f"Input a movement sequence from the \"Move\" column in the table above\n"
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
            for item in move_list:
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
            plr_dir_x, plr_dir_y = get_vector_direction(curr_player.speed)
            plr_dir_x = 1 if plr_dir_x == 0 else plr_dir_x

            horizontal = 26 if active_tech == "HYPER" else 15
            vertical = 3 if active_tech == "HYPER" else 9

            extension = 1.2 if "EXTENDED" in modifiers_list else 1
            slide = 1.3 if "SLIDE" in modifiers_list else 1
            chain_mult = 1 + 1.10 * chain_len

            hyper_boost_x = (plr_dir_x * horizontal * extension * slide) * chain_mult
            hyper_boost_y = vertical * chain_mult

            hyper_boost = (hyper_boost_x, hyper_boost_y)

            curr_player.speed = add_velocity(curr_player.speed, hyper_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a {active_tech.lower()} active tech")
            curr_player.transfer_active_tech()
            velocity_modifier /= slide

        elif "ULTRA" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)

            extension = 0.50 if "EXTENDED" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            ultra_mult_x = (1.50 + extension) * chain_mult
            ultra_mult_y = 1.30 * chain_mult
            ultra_mult = (ultra_mult_x, ultra_mult_y)

            curr_player.speed = multiply_velocity(curr_player.speed, ultra_mult)
            print(f" - {curr_player.name}'s speed has been influenced via an ultra active tech")
            curr_player.transfer_active_tech()

        elif "B-HOP" in active_tech and curr_player.speed_value() > 0:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = get_vector_direction(curr_player.speed)

            extension = 0.45 if "EXTENDED" in modifiers_list else 0
            high_jump = 0.75 if "HIGH-JUMP" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            b_hop_boost_x = (plr_dir_x * (12 + extension)) * chain_mult
            b_hop_boost_y = (3.5 + high_jump + extension) * chain_mult
            b_hop_boost = (b_hop_boost_x, b_hop_boost_y)

            curr_player.speed = add_velocity(curr_player.speed, b_hop_boost)
            print(f" - {curr_player.name}'s speed has been influenced via a b-hop active tech")
            curr_player.transfer_active_tech()
            velocity_modifier /= (1.25 + extension // 3 + high_jump // 4)

        elif "FALL-BOOST" in active_tech:
            active_tech, modifiers_list, chain_len = get_tech_modifiers(active_tech)
            plr_dir_x, plr_dir_y = get_vector_direction(curr_player.speed)
            plr_dir_x *= -1 # inverting, FALL-BOOST decreases horizontal speed

            slow_fall = 0.70 if "SLOW-FALL" in modifiers_list else 1
            fast_fall = 1.40 if "FAST-FALL" in modifiers_list else 1
            chain_mult = 1 + 1.10 * chain_len

            fall_boost_x = plr_dir_x * 3.5 * chain_mult
            fall_boost_y = (-30 * slow_fall * fast_fall) * chain_mult
            fall_boost = (fall_boost_x, fall_boost_y)

            curr_player.speed = add_velocity(curr_player.speed, fall_boost)
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
            plr_dir_x, plr_dir_y = get_vector_direction(curr_player.speed)
            plr_dir_x *= -1  # inverting, BOUNCE-BOOST decreases horizontal speed

            extension = 0.70 if "EXTENDED" in modifiers_list else 0
            high_jump = 0.80 if "HIGH-JUMP" in modifiers_list else 0
            chain_mult = 1 + 1.10 * chain_len

            bounce_boost_x = plr_dir_x * (3.5 - extension) * chain_mult
            bounce_boost_y = 25 * (1 + extension + high_jump) * chain_mult
            bounce_boost = (bounce_boost_x, bounce_boost_y)

            curr_player.speed = add_velocity(curr_player.speed, bounce_boost)
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
        self.iterate_turn()
        return velocity_modifier

# ── Table Printing Functions ──────────────────────────────
def print_hand(curr_player: Player | None = None, curr_hand: list[Card] | None = None) -> bool:
    if curr_player is None or curr_hand is None:
        print(f"No player provided or hand is empty")
        return False

    card_table = Table(caption=f"{curr_player.name}'s cards", box=box.ROUNDED)
    for item in CARD_PRINT:
        card_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
    for idx, item in enumerate(curr_hand):
        style, suit_rank = item.style, str(item.rank) + str(SUIT_LIB[item.suit])
        card_table.add_row(str(idx), style, suit_rank)

    console = Console(force_terminal=True, color_system="truecolor", width=150)
    console.print(card_table)
    return True

def print_players(player_list: list[Player], curr_player: Player | None = None) -> bool:
    if len(player_list) == 0:
        print(f"Not enough players to print!")
        return False

    player_table = Table(caption=f"The players", box=box.ROUNDED)
    active_tech_len = max(len(plr.active_tech) for plr in player_list) + 2
    cut_movement_tech = False
    for item in PLAYER_PRINT:
        if item[0] != "Move Tech":
            player_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
            continue
        if active_tech_len <= MAX_ACTIVE_TECH_LEN:
            player_table.add_column(item[0], min_width=active_tech_len, justify="center", no_wrap=True)
            continue
        player_table.add_column(item[0], min_width=item[1], justify="center", no_wrap=True)
        cut_movement_tech = True
    for idx, plr in enumerate(player_list):
        name, health = plr.name, f"{plr.health:,.2f}"
        defense, attack_stack = str(plr.defending), f"{plr.attack_stack:,.2f}"
        actions, speed, active_tech = str(plr.action_count), plr.speed_value(), plr.active_tech
        weakness, strength = plr.weakness, plr.strength

        if active_tech == "": active_tech = "None"
        if weakness == "": weakness = "None"
        if strength == "": strength = "None"
        if cut_movement_tech and len(active_tech) > MAX_ACTIVE_TECH_LEN:
            active_tech = active_tech[:MAX_ACTIVE_TECH_LEN - 3] + "..."
        you = "You" if curr_player == plr else "N/A"

        player_table.add_row(str(idx), name, health, defense, attack_stack, actions,
                             f"{speed:,.2f} m/s", active_tech, weakness, strength, you)

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

# ── Attacking Functions ──────────────────────────────
def evaluate_card(used_card: Card, curr_player: Player, stack_apply: bool = False):
    weakness_used = False
    strength_used = False

    card_suit, card_rank, card_style = used_card.suit, used_card.rank, used_card.style
    value = float(card_rank)
    value += curr_player.attack_stack if stack_apply else 0
    value *= STYLE_LIB[card_style]
    if curr_player.weakness == SUIT_LIB[card_suit]:
        value *= 0.75
        print(f" * Used {curr_player.name} weakness ({curr_player.weakness})")
        weakness_used = True
    if curr_player.strength == SUIT_LIB[card_suit]:
        value *= 1.50
        print(f" * Used {curr_player.name} strength ({curr_player.strength})")
        strength_used = True

    return value, weakness_used, strength_used

def evaluate_multipliers(curr_player: Player, weakness_used: bool, strength_used: bool):
    if weakness_used:
        curr_player.weakness = ""
    if strength_used:
        curr_player.strength = ""

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
            target_dir_x, target_dir_y = get_vector_direction(target.speed)
            attacker_dir_x, attacker_dir_y = get_vector_direction(attacker.speed)
            dif_dir_x = target_dir_x + attacker_dir_x
            dif_dir_y = target_dir_y + attacker_dir_y

            mult_x = 1.05 + (-0.05 * abs(dif_dir_x))
            mult_y = 1.05 + (-0.05 * abs(dif_dir_y))
            damage *= mult_x
            damage *= mult_y
            print(f" * Movement direction of both players affected damage (x: {mult_x:,.2f}, y: {mult_y:,.2f})")

        matched_keys = get_player_passive(attacker, "ULTRA")
        if matched_keys:
            tech, chain = matched_keys[0]
            full_tech = tech + " \\ " + chain if chain != "" else tech
            passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

            extension = 0.25 if "EXTENDED" in modifiers_list else 0
            chain_mult = 0.50 + 0.20 * chain_len

            mult = 1 + extension * chain_mult
            damage *= mult
            print(f" * Attacker passive tech increased damage (tech: {full_tech} multiplier: {mult:,.2f})")
            del attacker.passive_tech[tech]

        matched_keys = get_player_passive(target, "FALL-BOOST")
        if matched_keys:
            tech, chain = matched_keys[0]
            full_tech = tech + " \\ " + chain if chain != "" else tech
            passive_tech, modifiers_list, chain_len = get_tech_modifiers(full_tech)

            slow_fall = 0.03 if "SLOW-FALL" in modifiers_list else 0
            fast_fall = 0.05 if "FAST-FALL" in modifiers_list else 0
            chain_mult = 1 + 0.5 * chain_len

            mult = 1 + (slow_fall - fast_fall) * chain_mult
            damage *= mult

            print(f" * Target passive tech changed damage (tech: {full_tech} multiplier: {mult:,.2f})")
            del target.passive_tech[tech]

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

        apply_velocity_decay(target, 0.2, 0.2)

    evaluate_multipliers(attacker, weakness_used, strength_used)
    if damage > 0:
        target.health -= damage
        target.weakness = SUIT_LIB[card_suit]
        target.strength = SUIT_LIB[(card_suit + 2) % len(SUIT_LIB)]
        print(f"{target.name}'s health after attacking : {target.health:,.2f}\n"
              f"{target.name} is now weak to {target.weakness} and strong with {target.strength}\n")
    else:
        print(f"{target.name}'s was unaffected by the attack\n")

# ── Movement Functions ──────────────────────────────
def chunk_split_movement(movement: list[str]) -> list[tuple]:
    max_tech_len = max(len(key) for key in MOVEMENT_TECH_LIB.keys())
    movement_chunks = []
    i = 0
    while i < len(movement):
        matched = False
        for length in range(min(max_tech_len, len(movement) - i), 0, - 1):
            part = tuple(movement[i: i + length])
            if part in MOVEMENT_TECH_LIB.keys():
                movement_chunks.append(part)
                i += length
                matched = True
                break
        if not matched:
            movement_chunks.append(tuple(movement[i: i + 1]))
            i += 1
    return movement_chunks

def evaluate_movement_chunks(movement_chunks: list[tuple], player: Player) -> list[str]:
    tech_list = []
    for chunk in movement_chunks:
        if chunk in MOVEMENT_TECH_LIB.keys():
            tech_list.append(MOVEMENT_TECH_LIB[chunk])
        for move in chunk:
            move_vector = MOVEMENT_LIB[move][0]

            mv_dir_x, mv_dir_y = get_vector_direction(move_vector)
            plr_dir_x, plr_dir_y = get_vector_direction(player.speed)
            dif_dir_x = mv_dir_x + plr_dir_x
            dif_dir_y = mv_dir_y + plr_dir_y

            mult_x = (29 / 120) * dif_dir_x ** 3 - (1 / 2) * dif_dir_x ** 2 - (29 / 120) * dif_dir_x + (3 / 2)
            mult_y = (29 / 120) * dif_dir_y ** 3 - (1 / 2) * dif_dir_y ** 2 - (29 / 120) * dif_dir_y + (3 / 2)
            move_vector = multiply_velocity(move_vector, (mult_x, mult_y))

            player.speed = add_velocity(player.speed, move_vector)
    return tech_list

def evaluate_tech_list(tech_list: list[str], player: Player):
    for i in range(len(tech_list)):
        if tech_list[i] == player.active_tech:
            player.active_tech += " \\ CHAIN"
            print(f" <*> CHAIN modifier added to {player.name}'s active tech ({player.active_tech})")
            continue
        player.transfer_active_tech(tech_list[i])

def get_tech_modifiers(active_tech: str):
    active_tech, modifiers_list, chain_len = active_tech, [], 0
    if " \\ " in active_tech:
        active_tech, chain = active_tech.split(" \\ ", maxsplit=1)
        chain_len = len(chain.split(" \\ "))
    if " : " in active_tech:
        active_tech, modifiers = active_tech.split(" : ", maxsplit=1)
        modifiers_list = modifiers.split(" | ")
    return active_tech, modifiers_list, chain_len

def get_player_passive(player: Player, string: str) -> list[tuple]:
    matched_keys = [(key, value) for key, value in player.passive_tech.items() if string in key]
    return matched_keys

# ── Vector Functions ──────────────────────────────
def get_vector_direction(vector): # returns a pair of values, can only be 0, 1 or -1
    vector_x, vector_y = vector
    dir_x = (vector_x > 0) - (vector_x < 0)
    dir_y = (vector_y > 0) - (vector_y < 0)
    return dir_x, dir_y

def add_velocity(vector1: tuple, vector2: tuple):
    speed_x = vector1[0] + vector2[0]
    speed_y = vector1[1] + vector2[1]
    vector1 = (speed_x, speed_y)
    return vector1

def multiply_velocity(vector1: tuple, vector2: tuple):
    speed_x = vector1[0] * vector2[0]
    speed_y = vector1[1] * vector2[1]
    vector1 = (speed_x, speed_y)
    return vector1

def apply_velocity_decay(player: Player, vel_dx: float | int = 1, vel_dy: float | int = 1):
    vel_mult_x = sech((player.speed_value() * vel_dx) / (VELOCITY_DECAY_X * SPEED_IMPACT))
    vel_mult_y = sech((player.speed_value() * vel_dy) / (VELOCITY_DECAY_Y * SPEED_IMPACT))
    vel_mult = (vel_mult_x, vel_mult_y)
    player.speed = multiply_velocity(player.speed, vel_mult)

# ── Util / Helper Functions ──────────────────────────────
def game_winner(winner: Player):
    print(f"The player that has eliminated all the other players and won is!\n",
          figlet_format(f"{winner.name}", font="larry3d"))

def sech(x):
    return 1 / cosh(x)

def card_choosing(curr_hand: list[Card]) -> Card:
    user_chosen_card = curr_hand[0]
    while True:
        try:
            user_choice_card = int(input(f"Input your number of choice: "))
            if user_choice_card < 0:
                print(f"Please use positive numbers!")
                continue
        except ValueError:
            print(f"The input is of invalid type, skipping...")
            continue
        if user_choice_card >= len(curr_hand):
            print(f"The input is out of range, try again...")
            continue
        user_chosen_card = curr_hand[user_choice_card]
        print(f"The card you chose : {user_chosen_card}")
        if input(f"Input \"retry\" if you wish to pick a different card: ").lower() == "retry":
            continue
        break
    return user_chosen_card