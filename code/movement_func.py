from vector2_func import vector2_add, vector2_mult, vector2_dir

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

def evaluate_movement_chunks(movement_chunks: list[tuple], player: Player) -> list[str]:
    tech_list = []
    for chunk in movement_chunks:
        if chunk in MOVEMENT_TECH_LIB.keys():
            tech_list.append(MOVEMENT_TECH_LIB[chunk])
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

def evaluate_tech_list(tech_list: list[str], player: Player):
    for i in range(len(tech_list)):
        if tech_list[i] == player.active_tech:
            player.active_tech += " \\ CHAIN"
            print(f" <*> CHAIN modifier added to {player.name}'s active tech ({player.active_tech})")
            continue
        player.transfer_active_tech(tech_list[i])

def get_player_passive(player: Player, string: str) -> list[tuple]:
    matched_keys = [(key, value) for key, value in player.passive_tech.items() if string in key]
    return matched_keys

def get_tech_modifiers(active_tech: str):
    active_tech, modifiers_list, chain_len = active_tech, [], 0
    if " \\ " in active_tech:
        active_tech, chain = active_tech.split(" \\ ", maxsplit=1)
        chain_len = len(chain.split(" \\ "))
    if " : " in active_tech:
        active_tech, modifiers = active_tech.split(" : ", maxsplit=1)
        modifiers_list = modifiers.split(" | ")
    return active_tech, modifiers_list, chain_len

def unpack_mtl(dct: dict[tuple, str]) -> dict[tuple, str]:
    unpacked_dct = {}
    for key in dct.keys():
        key_symbols: list[str] = [sym for sym in MARK_LIB.keys() if sym in " ".join(key)]
        if not key_symbols:
            unpacked_dct[key] = dct[key]
            continue
        prev = None
        for sym in key_symbols:
            if sym == "<" and prev is not None:
                sym = prev
            prev = sym
            if sym == "*":
                for item in MARK_LIB[sym]:
                    joined_key = " ".join(key)
                    modified_key = tuple(joined_key.replace(sym, item).split(" "))
                    unpacked_dct[modified_key] = dct[key]
    return unpacked_dct


MOVEMENT_TECH_LIB = unpack_mtl(MOVEMENT_TECH_LIB) # passive unpacking