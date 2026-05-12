style_lib = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
style_lib_weights = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]
suit_lib = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

MIN_GENERATED_CARD_RANK = 1
MAX_GENERATED_CARD_RANK = 15

MAX_DECK_SIZE = 52

START_PLAYER_HEALTH = 100.0
ACTION_AMOUNT = 1

MIN_GAME_PLAYERS = 2
MAX_GAME_PLAYERS = 10
PLAYER_HAND_SIZE = 7
STACK_RANK_LIMIT = 7
SUIT_PENALTY = -3
IDENTICAL_BOOST = 3

DEFENSE_WEAKNESS_LIM = 10
DEFENSE_STRENGTH_LIM = 15
DEFENSE_THRESHOLD = 20

MIN_WEAKNESS_CRITICAL = 1

# balanced default : hp = 100, actions = 1 || Multiply actions by n and multiply health by n ** 2