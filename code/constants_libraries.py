# libraries
STYLE_LIB = {"Failed": 0.01, "Dull": 0.75, "Cool": 1.0, "Bold": 1.25, "Awesome": 1.5,
             "Stylish": 2.0, "Stunningly Stylish": 2.5, "Pristine": 3.0, "Omega": 5.0}
STYLE_LIB_WEIGHTS = [0.01, 0.13, 0.50, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01]

SUIT_LIB = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

MARK_LIB = {
    "*" : ("LEFT", "RIGHT"),
    "<" : "COPY LAST"
}

MOVEMENT_LIB = {
    "DASH-NONE-LEFT": ((-15, 0), "SUPER"),
    "DASH-NONE-RIGHT": ((15, 0), "SUPER"),

    "DASH-DOWN-LEFT": ((-10, -5), ("HYPER", "ULTRA")),
    "DASH-DOWN-RIGHT": ((10, -5), ("HYPER", "ULTRA")),

    "DASH-UP-LEFT": ((-10, 5), "FALL-BOOST"),
    "DASH-UP-RIGHT": ((10, 5), "FALL-BOOST"),

    "DASH-DOWN-NONE": ((0, -15), "BOUNCE-BOOST"),
    "DASH-UP-NONE": ((0, 15), "FALL-BOOST"),

    "JUMP": ((0, 10), "B-HOP"),
    "STALL": ((0, 0), "NONE")
}
# TECH : SUPER, HYPER, ULTRA, B-HOP, FALL-BOOST, BOUNCE-BOOST
# MODIFIERS : EXTENDED, SLIDE, HIGH-JUMP, SLOW-FALL, FAST-FALL, CHAIN (repeated use)
MOVEMENT_TECH_LIB = {
    ("DASH-NONE-*", "JUMP"): "SUPER",
    ("DASH-NONE-*", "STALL", "JUMP"): "SUPER : EXTENDED",
    ("DASH-NONE-*", "STALL", "STALL"): "SUPER : SLIDE",
    ("DASH-NONE-*", "STALL", "DASH-NONE-<", "STALL"): "SUPER : SLIDE | EXTENDED",

    ("DASH-DOWN-*", "JUMP"): "HYPER",
    ("DASH-DOWN-*", "STALL", "JUMP"): "HYPER : EXTENDED",
    ("DASH-DOWN-*", "STALL", "STALL"): "HYPER : SLIDE",
    ("DASH-DOWN-*", "STALL", "DASH-DOWN-<", "STALL"): "HYPER : SLIDE | EXTENDED",

    ("DASH-DOWN-*", "DASH-DOWN-<", "STALL", "JUMP"): "ULTRA",
    ("DASH-DOWN-*", "DASH-DOWN-<", "STALL", "STALL", "JUMP"): "ULTRA : EXTENDED",

    ("JUMP", "STALL", "JUMP"): "B-HOP",
    ("JUMP", "STALL", "DASH-NONE-*", "JUMP"): "B-HOP : EXTENDED",
    ("JUMP", "STALL", "DASH-DOWN-*", "JUMP"): "B-HOP : HIGH-JUMP",
    ("JUMP", "STALL", "DASH-NONE-*", "STALL", "JUMP"): "B-HOP : HIGH-JUMP, EXTENDED",

    ("DASH-UP-*", "STALL"): "FALL-BOOST",
    ("DASH-UP-*", "STALL", "JUMP"): "FALL-BOOST : SLOW-FALL",
    ("DASH-UP-*", "STALL", "DASH-DOWN-NONE"): "FALL-BOOST : FAST-FALL",

    ("DASH-DOWN-NONE", "JUMP"): "BOUNCE-BOOST",
    ("DASH-DOWN-NONE", "DASH-UP-*", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP",
    ("DASH-DOWN-NONE", "STALL", "JUMP"): "BOUNCE-BOOST : EXTENDED",
    ("DASH-DOWN-NONE", "STALL", "DASH-UP-*", "JUMP"): "BOUNCE-BOOST : HIGH-JUMP | EXTENDED",
}

TECH_SPEED_LIB = {
    "SUPER" :         (20,   8),
    "HYPER" :         (26,   3),
    "ULTRA":          (1.5,  1.3),
    "B-HOP":          (28,   10),
    "FALL-BOOST":     (3.5,  -30),
    "BOUNCE-BOOST":   (3.5,  25)
}

# table printing
CARD_PRINT = [("Index", 7), ("Style", 20), ("Rank Suit", 11)]
PLAYER_PRINT = [("Index", 7), ("Name", 9), ("Health", 8), ("Defense", 9), ("Atk. Stack", 12),
                ("Actions", 9), ("Speed", 14), ("Weakness", 10), ("Strength", 10), ("You?", 6)]
MOVEMENT_PRINT = [("Index", 7), ("Move", 18), ("Vector", 12), ("Movement Tech", 17)]

# set action multiplier to a number > 0 to change hp and action count accordingly | default is 1, recommended is 2
ACTION_MULTIPLIER = 1

# card variables
MIN_GENERATED_CARD_RANK = 1
MAX_GENERATED_CARD_RANK = 15

# deck variables
MAX_DECK_SIZE = 26 * ACTION_MULTIPLIER

# player variables
START_PLAYER_HEALTH = 100.0 * (ACTION_MULTIPLIER ** 2)
ACTION_AMOUNT = ACTION_MULTIPLIER
INITIAL_SPEED = (0, 0)

# game-loop variables
MIN_GAME_PLAYERS = 2
MAX_GAME_PLAYERS = 10
PLAYER_HAND_SIZE = 7

STACK_RANK_LIMIT = 7
PARRY_LONGEVITY = 4
SUIT_PENALTY = -4
IDENTICAL_BOOST = 6

MIN_MOVE = 2 + ACTION_MULTIPLIER
SPEED_IMPACT = 50 * (ACTION_MULTIPLIER ** (1/2))
VELOCITY_DECAY_X = 8
VELOCITY_DECAY_Y = 9

DEFENSE_STRENGTH_LIM = 10
DEFENSE_WEAKNESS_LIM = 15
DEFENSE_THRESHOLD = 20

MIN_WEAKNESS_CRITICAL = 1