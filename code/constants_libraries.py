# libraries
STYLE_LIB = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
STYLE_LIB_WEIGHTS = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]

SUIT_LIB = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

MOVEMENT_LIB = {
    "DASH-NONE-LEFT": [(0, -50), "SUPER"],
    "DASH-NONE-RIGHT": [(0, 50), "SUPER"],

    "DASH-DOWN-LEFT": [(-20, -30), ("HYPER", "ULTRA")],
    "DASH-DOWN-RIGHT": [(-20, 30), ("HYPER", "ULTRA")],

    "DASH-UP-LEFT": [(20, -30), "FALL-BOOST"],
    "DASH-UP-RIGHT": [(20, 30), "FALL-BOOST"],

    "DASH-DOWN-NONE": [(-40, 0), "FALL-BOOST"],
    "DASH-UP-NONE": [(40, 0), "FALL-BOOST"],

    "JUMP": [(60, 0), ("FALL-BOOST", "B-HOP")],
    "STALL": [(0, 0), "NONE"]
}

# table printing
CARD_PRINT = [("Index", 7), ("Style", 21), ("Rank Suit", 11)]
PLAYER_PRINT = [("Index", 7), ("Name", 9), ("Health", 11), ("Actions", 9), ("Speed", 13), ("Move Tech", 13),
                ("Defense", 9), ("Attack Stack", 15), ("Weakness", 11), ("Strength", 11), ("You?", 7)]
MOVEMENT_PRINT = [("Index", 7), ("Move", 21), ("Vector", 15), ("Movement Tech", 21)]

# set action multiplier to any number change hp and action count accordingly | default is 1
ACTION_MULTIPLIER = 1

# card variables
MIN_GENERATED_CARD_RANK = 1
MAX_GENERATED_CARD_RANK = 15

# deck variables
MAX_DECK_SIZE = 52

# player variables
START_PLAYER_HEALTH = 100.0 * (ACTION_MULTIPLIER ** 2)
ACTION_AMOUNT = 1 * ACTION_MULTIPLIER
INITIAL_SPEED = (0, 0)

# game-loop variables
MIN_GAME_PLAYERS = 2
MAX_GAME_PLAYERS = 10
PLAYER_HAND_SIZE = 7

STACK_RANK_LIMIT = 7
SUIT_PENALTY = -3
IDENTICAL_BOOST = 3

MIN_MOVE = 3 * ACTION_MULTIPLIER
VELOCITY_DECAY = 0.85

DEFENSE_STRENGTH_LIM = 10
DEFENSE_WEAKNESS_LIM = 15
DEFENSE_THRESHOLD = 20

MIN_WEAKNESS_CRITICAL = 1