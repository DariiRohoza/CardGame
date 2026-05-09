from pyfiglet import figlet_format
from card_class import Card
from deck_class import Deck
from player_class import Player
from constants_libraries import (suit_lib, style_lib, MIN_GENERATED_CARD_RANK,
                                 MIN_GAME_PLAYERS, MAX_GAME_PLAYERS, PLAYER_HAND_SIZE,
                                 DEFENSE_THRESHOLD, SUIT_PENALTY, IDENTICAL_BOOST)

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
        # Checking Conditions
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
            user_choice_option = 0
            if len(self.deck) == 0:
                self.deck.fill()
                self.deck.shuffle()
                print(f"--<  Refilled Deck  >--\n")

            curr_player, curr_hand = self.fetch_curr()

            print(f">>> It is now {curr_player.name}'s turn\n\n"
                  f"Pick an options from those below by inputting the number in front of it\n"
                  f"00 : Conclude Game / Quit\n"
                  f"01 : Attack Player\n"
                  f"02 : View Other Players\n"
                  f"03 : View Hand\n"
                  f"04 : Refurbish Card Suit\n"
                  f"05 : Increase Card Rank\n"
                  f"06 : Merge Card Rank\n"
                  f"07 : Stylize Card\n"
                  f"08 : Exchange half of your hand\n"
                  f"09 : Defend\n")

            while True:
                try:
                    user_choice_option = int(input(f"Input your choice: "))
                except ValueError:
                    print(f"The input is of invalid value, try again...")
                    continue
                break

            match user_choice_option:
                case 0: self.conclude_game = True
                case 1: self.attack_turn(curr_player, curr_hand)
                case 2: print_players(self.player_list, curr_player)
                case 3: print_hand(curr_hand)
                case 4: self.refurbish_card_suit(curr_hand, curr_player)
                case 5: self.increase_card_rank(curr_hand, curr_player)
                case 6: self.merge_card_rank(curr_hand)
                case 7: self.stylize_card(curr_hand)
                case 8: self.drop_half_cards(curr_hand)
                case 9: self.defend(curr_player, 2)

                case _:
                    print(f"Invalid input, try again...\n")

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
        print_hand(curr_hand)
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
            print(f"{curr_player.name} has decided to attack {user_chosen_target.name} using:", user_chosen_card)

            attack_player(curr_player, user_chosen_target, user_chosen_card)

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

    def refurbish_card_suit(self, curr_hand: list[Card], curr_player: Player):
        print(f"Pick a card to be refurbished from your hand by inputting the number in front of it")
        print_hand(curr_hand)
        user_card = card_choosing(curr_hand)
        curr_hand.remove(user_card)

        print(f"Please select a target suit from the following options by inputting the number in front of it")
        for key, value in suit_lib.items():
            if key != user_card.card_value[0]:
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
            if user_choice_suit not in suit_lib.keys():
                print(f"The input is out of range, try again...")
                continue
            if user_choice_suit == user_card.card_value[0]:
                print(f"The target suit has to be different from the starting suit, try again...")
                continue
            break

        if curr_player.weakness == suit_lib[user_choice_suit]:
            print(f" * Cured player weakness at no cost")
            curr_player.weakness = ""

        print(f"\n--> Granted player strength with the chosen suit ({suit_lib[user_choice_suit]})")
        curr_player.strength = suit_lib[user_choice_suit]

        new_card = Card()
        new_card.add_info(user_choice_suit, user_card.card_value[1], user_card.style)

        print(f"\n--> Changed suit card: {new_card}\n")
        curr_hand.append(new_card)
        self.iterate_turn()

    def increase_card_rank(self, curr_hand: list[Card], curr_player: Player):
        print(f"Pick a card to increase rank of from your hand by inputting the number in front of it")
        print_hand(curr_hand)
        user_card = card_choosing(curr_hand)
        curr_hand.remove(user_card)

        strength_bonus = MIN_GENERATED_CARD_RANK

        if curr_player.strength == suit_lib[user_card.card_value[0]]:
            strength_bonus += 5
            print(f" * Nullified player strength for a higher ranked card")
            curr_player.strength = ""

        new_card = Card()
        new_card.add_info(user_card.card_value[0], user_card.card_value[1] + strength_bonus, user_card.style)

        print(f"\n--> Increased rank card: {new_card}\n")
        curr_hand.append(new_card)
        self.defend(curr_player, 1) # also handles the iterate_turn()

    def merge_card_rank(self, curr_hand: list[Card]):
        print(f"The first card you pick is going to be the target while the second is the one going to be merged\n"
              f"--> If the 2 cards selected have different suits, the result will have a penalty of 3 subtracted\n\n"
              f"Pick a target card from your hand by inputting the number in front of it")
        print_hand(curr_hand)
        user_card_1st = card_choosing(curr_hand)
        curr_hand.remove(user_card_1st)

        print(f"Pick the card that is to be merged to your first pick by inputting the number in front of it")
        print_hand(curr_hand)
        user_card_2nd = card_choosing(curr_hand)
        curr_hand.remove(user_card_2nd)

        if style_lib[user_card_1st.style] > style_lib[user_card_2nd.style]:
            merged_style = user_card_1st.style
        else:
            merged_style = user_card_2nd.style

        change = 0

        if user_card_1st.card_value[0] != user_card_2nd.card_value[0]:
            change += SUIT_PENALTY
        if user_card_2nd.card_value == user_card_1st.card_value:
            change += IDENTICAL_BOOST

        merged_card = Card()
        merged_card.add_info(user_card_1st.card_value[0],
                             user_card_1st.card_value[1] + user_card_2nd.card_value[1] + change,
                             merged_style)

        print(f"\n--> Merged card: {merged_card}\n")
        curr_hand.append(merged_card)
        curr_hand.append(self.deck.draw_card())
        self.iterate_turn()

    def stylize_card(self, curr_hand: list[Card]):
        print(f"Pick a card to increase style of from your hand by inputting the number in front of it")
        print_hand(curr_hand)
        user_card = card_choosing(curr_hand)
        curr_hand.remove(user_card)

        new_style = user_card.style
        for key, value in style_lib.items():
            if value > style_lib[new_style]:
                new_style = key
                break

        new_card = Card()
        new_card.add_info(user_card.card_value[0], user_card.card_value[1], new_style)

        print(f"\n--> Increased style card: {new_card}\n")
        curr_hand.append(new_card)
        self.iterate_turn()

    def defend(self, curr_player, def_stacks: int):
        curr_player.defending += def_stacks
        print(f"{curr_player.name} has gained {def_stacks} stack(s) of defense\n")
        self.iterate_turn()

    def drop_half_cards(self, curr_hand: list[Card]):
        cards_removed = len(curr_hand) // 2
        for i in range(cards_removed):
            print(f"Choose a card to remove ({i}/{cards_removed} removed already)")
            print_hand(curr_hand)
            user_card = card_choosing(curr_hand)
            curr_hand.remove(user_card)

        for _ in range(cards_removed):
            curr_hand.append(self.deck.draw_card())
        print(f"{cards_removed} new cards have been added to your hand\n")
        self.iterate_turn()

# ── Util / Helper Functions ──────────────────────────────
def print_hand(curr_hand: list[Card] = None):
    if curr_hand is None:
        print(f"Hand is empty")
    else:
        for i in range(len(curr_hand)):
            print(f"{i} : {curr_hand[i]}")

def print_players(player_list: list[Player], curr_player: Player = None):
    if len(player_list) == 0:
        print(f"Not enough players to print!")
    else:
        for i in range(len(player_list)):
            print(f"{i} : {player_list[i]}")
            if player_list[i] == curr_player:
                print(f" ^ Yourself!")

def game_winner(winner: Player):
    print(f"The player that has eliminated all the other players and won is!\n",
          figlet_format(f"{winner.name}", font="larry3d"))

def attack_player(attacker: Player, target: Player, used_card: Card):
    card_style, card_value = used_card.style, used_card.card_value
    damage = card_value[1] * style_lib[card_style]

    if target.defending >= DEFENSE_THRESHOLD:
        damage = 0
        remaining_defense = (target.defending + 1 // 2) + 1
        print(f" * Nullified all damage taken at the cost of {target.defending - remaining_defense} defense stacks")
        target.defending = remaining_defense

    else:
        if target.defending > 0:
            damage *= 0.85 ** target.defending
            print(f" * Nullified 1 target defense stack")
            target.defending -= 1 # defense stacks get removed one by one, but they all impact damage taken

        if target.weakness == suit_lib[card_value[0]]:
            damage *= 1.5
            print(f" * Target weakness amplified damage ({target.weakness})")
            target.defending -= 1
            print(f"* Weakness caused target to lose another defense stack")
        if target.strength == suit_lib[card_value[0]]:
            damage *= 0.75
            print(f" * Target strength reduced damage ({target.strength})")

        if attacker.weakness == suit_lib[card_value[0]]:
            damage *= 0.75
            print(f" * Nullified attacker weakness ({attacker.weakness})")
            attacker.weakness = ""
        if attacker.strength == suit_lib[card_value[0]]:
            damage *= 1.5
            print(f" * Nullified attacker strength ({attacker.strength})")
            attacker.strength = ""

    target.health -= damage

    if damage > 0:
        target.weakness = suit_lib[card_value[0]]
        target.strength = suit_lib[(card_value[0] + 2) % len(suit_lib)]
        print(f"{target.name}'s health after attacking : {target.health:,.2f}\n"
              f"{target.name} is now weak to {target.weakness} and strong with {target.strength}\n")
    else:
        print(f"{target.name}'s was unaffected by the attack\n")

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
        user_in = input(f"Input \"retry\" if you wish to pick a different card: ")
        if user_in.lower() == "retry":
            continue
        break
    return user_chosen_card