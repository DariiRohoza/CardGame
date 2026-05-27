# libraries
STYLE_LIB = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
STYLE_LIB_WEIGHTS = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]

SUIT_LIB = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

MOVEMENT_LIB = {
    "DASH-NONE-LEFT": ((0, -50), "SUPER"),
    "DASH-NONE-RIGHT": ((0, 50), "SUPER"),

    "DASH-DOWN-LEFT": ((-20, -30), ("HYPER", "ULTRA")),
    "DASH-DOWN-RIGHT": ((-20, 30), ("HYPER", "ULTRA")),

    "DASH-UP-LEFT": ((20, -30), "FALL-BOOST"),
    "DASH-UP-RIGHT": ((20, 30), "FALL-BOOST"),

    "DASH-DOWN-NONE": ((-50, 0), "BOUNCE-BOOST"),
    "DASH-UP-NONE": ((50, 0), "FALL-BOOST"),

    "JUMP": ((60, 0), "B-HOP"),
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
CARD_PRINT = [("Index", 7), ("Style", 21), ("Rank Suit", 11)]
PLAYER_PRINT = [("Index", 7), ("Name", 9), ("Health", 11), ("Defense", 9), ("Attack Stack", 15),
                ("Actions", 9), ("Speed", 13), ("Move Tech", 13), ("Weakness", 11), ("Strength", 11), ("You?", 7)]
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

MIN_MOVE = 3 + (2 * (ACTION_MULTIPLIER - 1))
VELOCITY_DECAY = 0.85

DEFENSE_STRENGTH_LIM = 10
DEFENSE_WEAKNESS_LIM = 15
DEFENSE_THRESHOLD = 20

MIN_WEAKNESS_CRITICAL = 1