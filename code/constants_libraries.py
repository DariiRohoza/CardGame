# libraries
STYLE_LIB = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
STYLE_LIB_WEIGHTS = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]

SUIT_LIB = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

MOVEMENT_LIB = {
    "DASH-NONE-LEFT": ((-50, 0), "SUPER"),
    "DASH-NONE-RIGHT": ((50, 0), "SUPER"),

    "DASH-DOWN-LEFT": ((-30, -20), ("HYPER", "ULTRA")),
    "DASH-DOWN-RIGHT": ((30, -20), ("HYPER", "ULTRA")),

    "DASH-UP-LEFT": ((-30, 20), "FALL-BOOST"),
    "DASH-UP-RIGHT": ((30, 20), "FALL-BOOST"),

    "DASH-DOWN-NONE": ((0, -50), "BOUNCE-BOOST"),
    "DASH-UP-NONE": ((0, 50), "FALL-BOOST"),

    "JUMP": ((0, 40), "B-HOP"),
    "STALL": ((0, 0), "NONE")
}
# TECH : SUPER, HYPER, ULTRA, B-HOP, FALL-BOOST, BOUNCE-BOOST
# MODIFIERS : EXTENDED, SLIDE, HIGH-JUMP, SLOW-FALL, FAST-FALL, CHAIN (repeated use)
MOVEMENT_TECH_LIB = {
    ("DASH-NONE-LEFT", "JUMP"): "SUPER",
    ("DASH-NONE-RIGHT", "JUMP"): "SUPER",
    ("DASH-NONE-LEFT", "STALL", "JUMP"): "SUPER : EXTENDED",
    ("DASH-NONE-RIGHT", "STALL", "JUMP"): "SUPER : EXTENDED",
    ("DASH-NONE-LEFT", "STALL", "STALL"): "SUPER : SLIDE",
    ("DASH-NONE-RIGHT", "STALL", "STALL"): "SUPER : SLIDE",

    ("DASH-DOWN-LEFT", "JUMP"): "HYPER",
    ("DASH-DOWN-RIGHT", "JUMP"): "HYPER",
    ("DASH-DOWN-LEFT", "STALL", "JUMP"): "HYPER : EXTENDED",
    ("DASH-DOWN-RIGHT", "STALL", "JUMP"): "HYPER : EXTENDED",
    ("DASH-DOWN-LEFT", "STALL", "STALL"): "HYPER : SLIDE",
    ("DASH-DOWN-RIGHT", "STALL", "STALL"): "HYPER : SLIDE",

    ("DASH-DOWN-LEFT", "STALL", "STALL", "JUMP"): "ULTRA",
    ("DASH-DOWN-RIGHT", "STALL", "STALL", "JUMP"): "ULTRA",

    ("JUMP", "STALL", "JUMP"): "B-HOP",
    ("JUMP", "STALL", "DASH-NONE-LEFT", "JUMP"): "B-HOP : EXTENDED",
    ("JUMP", "STALL", "DASH-NONE-RIGHT", "JUMP"): "B-HOP : EXTENDED",
    ("JUMP", "STALL", "DASH-DOWN-LEFT", "JUMP"): "B-HOP : HIGH-JUMP",
    ("JUMP", "STALL", "DASH-DOWN-RIGHT", "JUMP"): "B-HOP : HIGH-JUMP",

    ("DASH-UP-LEFT", "STALL"): "FALL-BOOST",
    ("DASH-UP-RIGHT", "STALL"): "FALL-BOOST",
    ("DASH-UP-LEFT", "STALL", "JUMP"): "FALL-BOOST : SLOW-FALL",
    ("DASH-UP-RIGHT", "STALL", "JUMP"): "FALL-BOOST : SLOW-FALL",
    ("DASH-UP-LEFT", "STALL", "DASH-DOWN-NONE"): "FALL-BOOST : FAST-FALL",
    ("DASH-UP-RIGHT", "STALL", "DASH-DOWN-NONE"): "FALL-BOOST : FAST-FALL",

    ("DASH-DOWN-NONE", "JUMP"): "BOUNCE-BOOST",
    ("DASH-DOWN-NONE", "DASH-UP-LEFT", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP",
    ("DASH-DOWN-NONE", "DASH-UP-RIGHT", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP",
    ("DASH-DOWN-NONE", "STALL", "JUMP"): "BOUNCE-BOOST : EXTENDED",
    ("DASH-DOWN-NONE", "STALL", "DASH-UP-LEFT", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP | EXTENDED",
    ("DASH-DOWN-NONE", "STALL", "DASH-UP-RIGHT", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP | EXTENDED"
}

# table printing
MAX_ACTIVE_TECH_LEN = 27
CARD_PRINT = [("Index", 7), ("Style", 20), ("Rank Suit", 11)]
PLAYER_PRINT = [("Index", 7), ("Name", 9), ("Health", 8), ("Defense", 9), ("Atk. Stack", 12),
                ("Actions", 9), ("Speed", 14), ("Active Tech", MAX_ACTIVE_TECH_LEN), ("Weakness", 10), ("Strength", 10), ("You?", 6)]
MOVEMENT_PRINT = [("Index", 7), ("Move", 18), ("Vector", 12), ("Movement Tech", 17)]

# set action multiplier to a number > 0 to change hp and action count accordingly | default is 1, recommended is 2
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

MIN_MOVE = 3 + (2 * (ACTION_MULTIPLIER - 1))
SPEED_IMPACT = 50 * (ACTION_MULTIPLIER ** (1/2))
VELOCITY_DECAY_X = 0.80
VELOCITY_DECAY_Y = 0.90

DEFENSE_STRENGTH_LIM = 10
DEFENSE_WEAKNESS_LIM = 15
DEFENSE_THRESHOLD = 20

MIN_WEAKNESS_CRITICAL = 1