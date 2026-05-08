from random import shuffle, randint, choices
from pyfiglet import figlet_format

# GLOBAL VARIABLES
style_lib = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
style_lib_weights = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]
suit_lib = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

# balanced default : hp = 100, actions = 1 || Multiply actions by n and multiply health by n ** 2
MIN_GENERATED_CARD_RANK = 1
MAX_GENERATED_CARD_RANK = 15

MAX_DECK_SIZE = 52

START_PLAYER_HEALTH = 100.0 * (2 ** 2)
ACTION_AMOUNT = 1 * 2

MIN_GAME_PLAYERS = 2
MAX_GAME_PLAYERS = 10
PLAYER_HAND_SIZE = 7

DEFENSE_THRESHOLD = 10

# CLASSES
# ── Card ──────────────────────────────
class Card:
    def __init__(self):
        self.card_value: tuple[int, int] = (0,0) # suit 1st, rank 2nd
        self.style: str = ""

    def __str__(self):
        if self.card_value is None or self.style is None:
            return (f"Value(s) missing, can't print properly, skipping..."
                    f"--> Value: {self.card_value}, Style: {self.style}")
        return f"{self.style} {str(self.card_value[1]) + suit_lib[self.card_value[0]]} card!"

    def add_info(self, suit: int, rank: int, style: str):
        global suit_lib, style_lib, MIN_GENERATED_CARD_RANK

        # Validating {Suit} and {Rank}
        if type(suit) is not int or type(rank) is not int:
            raise TypeError(f"Suit ({suit}) or rank {rank}: Invalid type")
        elif suit not in suit_lib.keys() or rank < MIN_GENERATED_CARD_RANK:
            raise ValueError(f"Suit ({suit}) or rank {rank}: Invalid value")
        elif self.card_value != (0,0):
            raise ValueError(f"A value is already assigned, skipping...")
        else:
            self.card_value = (suit, rank)

        # Validating {Style}
        if type(style) is not str:
            raise TypeError(f"Style {style}: Invalid type")
        elif style not in style_lib:
            raise ValueError(f"Style {style}: Invalid value")
        elif self.style != "":
            raise ValueError(f"A value is already assigned, skipping...")
        else:
            self.style = style

# ── Deck ──────────────────────────────
class Deck:
    def __init__(self):
        self.cards: list[Card] = []

    def __len__(self):
        return len(self.cards)

    def print_deck(self):
        for item in self.cards:
            print(item)

    def draw_card(self) -> Card:
        if len(self) == 0:
            print(f"The deck is empty, calling fill to complete the new deck before drawing a card")
            self.fill()
        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)

    # fill the deck to the brim with random cards
    def fill(self):
        global MAX_DECK_SIZE
        cards_to_add = MAX_DECK_SIZE - len(self.cards)
        for _ in range(cards_to_add):
            self.cards.append(generate_card())

# ── Player ──────────────────────────────
class Player:
    def __init__(self):
        global START_PLAYER_HEALTH, ACTION_AMOUNT
        self.name: str = "PLACEHOLDER"
        self.hand: list[Card] = []
        self.health: float = START_PLAYER_HEALTH
        self.action_count: int = ACTION_AMOUNT
        self.defending: int = 0

        # only values from {suit_lib} and an empty string {""}
        self.weakness: str = ""
        self.strength: str = ""

    def __str__(self):
        if self.health <= 0.00:
            return f"A dead player"
        return (f"A player at {self.health:,.2f}hp; {self.action_count} speed; {self.defending} defense stacks; "
                f"hand hidden; --> Weakness: {self.weakness}; Strength: {self.strength}")

    def rename(self, name: str=None):
        if name is not None:
            self.name = name
            return name
        while True:
            new_name = input(f"Please enter a new name for the player: ")
            if len(new_name) == 0:
                continue
            break
        self.name = new_name
        return new_name

# ── GameLoop ──────────────────────────────
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
        global MIN_GAME_PLAYERS, PLAYER_HAND_SIZE
        if len(self.player_list) < MIN_GAME_PLAYERS:
            print(f"Insufficient players, skipping...")
        else:
            print(f"All requirements have been fulfilled, the game is starting...")
            self.deck.fill()

            for item in self.player_list:
                for _ in range(PLAYER_HAND_SIZE):
                    item.hand.append(self.deck.draw_card())

    def add_player(self, new_player: Player):
        global MAX_GAME_PLAYERS
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
            if len(self.deck) == 0:
                self.deck.fill()
                self.deck.shuffle()
                print(f"--<  Refilled Deck  >--\n")

            curr_player, curr_hand = self.fetch_curr()

            print(f">>> It is now {curr_player.name}'s turn\n")
            print(f"Pick an options from those below by inputting the number in front of it\n"
                  f"00 : Conclude Game / Quit\n"
                  f"01 : Exchange half of your hand\n"
                  f"02 : View Other Players\n"
                  f"03 : View Hand\n"
                  f"04 : Attack Player\n"
                  f"05 : Refurbish Card Suit\n"
                  f"06 : Increase Card Rank\n"
                  f"07 : Merge Card Rank\n"
                  f"08 : Stylize Card\n"
                  f"09 : Defend\n")

            try:
                user_choice_option = int(input(f"Input your choice: "))
            except ValueError:
                print(f"The input is of invalid value, try again...")
                continue

            match user_choice_option:
                case 0: self.conclude_game = True
                case 1: self.drop_half_cards(curr_hand)
                case 2: print_players(self.player_list, curr_player)
                case 3: print_hand(curr_hand)
                case 4: self.attack_turn(curr_player, curr_hand)
                case 5: self.refurbish_card_suit(curr_hand, curr_player)
                case 6: self.increase_card_rank(curr_hand, curr_player)
                case 7: self.merge_card_rank(curr_hand)
                case 8: self.stylize_card(curr_hand)
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
        global suit_lib
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
        global suit_lib, MIN_GENERATED_CARD_RANK
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
        global style_lib
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

        suit_penalty = 0
        identical_boost = 0

        if user_card_1st.card_value[0] != user_card_2nd.card_value[0]:
            suit_penalty = -3
        if user_card_2nd.card_value == user_card_1st.card_value:
            identical_boost = 3

        merged_card = Card()
        merged_card.add_info(user_card_1st.card_value[0],
                             user_card_1st.card_value[1] + user_card_2nd.card_value[1] + suit_penalty + identical_boost,
                             merged_style)

        print(f"\n--> Merged card: {merged_card}\n")
        curr_hand.append(merged_card)
        curr_hand.append(self.deck.draw_card())
        self.iterate_turn()

    def stylize_card(self, curr_hand: list[Card]):
        global style_lib
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

        for i in range(cards_removed):
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

def generate_card() -> Card:
    global suit_lib, style_lib, MAX_GENERATED_CARD_RANK
    card = Card()
    suit_choice = randint(0, len(suit_lib)-1)
    rank_choice = randint(1, MAX_GENERATED_CARD_RANK)
    style_choice = choices(list(style_lib.keys()), weights=style_lib_weights, k=1)[0]
    card.add_info(suit_choice, rank_choice, style_choice)
    return card

def attack_player(attacker: Player, target: Player, used_card: Card):
    global suit_lib, style_lib, DEFENSE_THRESHOLD
    card_style, card_value = used_card.style, used_card.card_value
    damage = card_value[1] * style_lib[card_style]

    if target.defending >= DEFENSE_THRESHOLD:
        damage = 0
        remaining_defense = (target.defending + 1 // 2) + 1
        print(f" * Nullified all damage taken at the cost of {remaining_defense} defense stacks")
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

if __name__ == "__main__":
    game_loop = GameLoop()

    player = Player()
    player.rename("BOB")
    game_loop.add_player(player)

    player2 = Player()
    player2.rename("ALEX")
    game_loop.add_player(player2)

    game_loop.initialize_game()
    print(game_loop)
    game_loop.main_loop()

# TODO : IMPLEMENT THE FOLLOWING IN THE FUTURE

# FEATURE : negative ranks as healing mechanics because math is math
    # ACTION : invert card (2 actions), can be used together with negative ranks to make a rapid supply of healing cards

# FEATURE : player move choice, changing a move choice is an ACTION, all are started with "stationary"
    # B-hop : removes an additional defense stack from the enemy if your strength matches the card you used
    # Hyper : 1/3 chance to increase the rank of a random card by 3 every action
    # Super : constant x0.80 damage reduction
    # Ultra : 5/8 chance to crit (x1.5 dmg) on attacks
