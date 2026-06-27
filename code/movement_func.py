from itertools import product

from vector2_func import vector2_add, vector2_mult, vector2_dir

from move_tech_class import MoveTech
from player_class import Player
from constants_libraries import MARK_LIB, MOVEMENT_LIB, MOVEMENT_TECH_LIB


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

def evaluate_movement_chunks(movement_chunks: list[tuple], player: Player) -> list[MoveTech]:
    tech_list: list[MoveTech] = []
    for chunk in movement_chunks:
        if chunk in MOVEMENT_TECH_LIB.keys():
            tech, modifiers, chain_count = MOVEMENT_TECH_LIB[chunk]
            tech_list.append(MoveTech(tech, modifiers, chain_count))
        for move in chunk:
            move_vector = MOVEMENT_LIB[move][0]

            mv_dir_x, mv_dir_y = vector2_dir(move_vector)
            plr_dir_x, plr_dir_y = vector2_dir(player.speed)
            dif_dir_x = mv_dir_x + plr_dir_x
            dif_dir_y = mv_dir_y + plr_dir_y

            mult_x = (29 / 120) * dif_dir_x ** 3 - (1 / 2) * dif_dir_x ** 2 - (29 / 120) * dif_dir_x + (3 / 2)
            mult_y = (29 / 120) * dif_dir_y ** 3 - (1 / 2) * dif_dir_y ** 2 - (29 / 120) * dif_dir_y + (3 / 2)
            move_vector = vector2_mult(move_vector, (mult_x, mult_y))

            player.speed = vector2_add(player.speed, move_vector)
    return tech_list

def evaluate_tech_list(tech_list: list[MoveTech], player: Player):
    for i in range(len(tech_list)):
        if player.active_tech is None:
            player.transfer_active_tech(tech_list[i])
            continue
        if tech_list[i] == player.active_tech:
            player.active_tech.add_chain()
            print(f" <*> CHAIN modifier added to {player.name}'s active tech ({player.active_tech})")

def get_player_passive(player: Player, string: str) -> list[MoveTech]:
    matched_keys = [t for t in player.passive_tech if t.tech == string.upper()]
    return matched_keys

def unpack_mtl(dct: dict[tuple, tuple]) -> dict[tuple, tuple]:
    unpacked_dct = {}

    for key, value in dct.items():
        # Find all element indices that contain a '*'
        star_indices = [i for i, elem in enumerate(key) if "*" in elem]

        if not star_indices:
            unpacked_dct[key] = value
            continue

        # Generate every combination of LEFT/RIGHT for each independent '*'
        for combo in product(MARK_LIB["*"], repeat=len(star_indices)):
            star_values = dict(zip(star_indices, combo))
            new_key = list(key)

            # Replace each '*' with its assigned value
            for i, val in star_values.items():
                new_key[i] = new_key[i].replace("*", val)

            # Replace each '<' with the most recent '*' value to its left
            last_star_value = None
            for i in range(len(key)):
                if i in star_values:
                    last_star_value = star_values[i]
                elif "<" in key[i] and last_star_value is not None:
                    new_key[i] = key[i].replace("<", last_star_value)

            unpacked_dct[tuple(new_key)] = value

    return unpacked_dct


MOVEMENT_TECH_LIB = unpack_mtl(MOVEMENT_TECH_LIB) # passive unpacking