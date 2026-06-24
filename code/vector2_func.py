from math import cosh

from player_class import Player
from constants_libraries import SPEED_IMPACT, VELOCITY_DECAY_X, VELOCITY_DECAY_Y


def sech(x):
    return 1 / cosh(x)

def vector2_add(vector1: tuple, vector2: tuple):
    speed_x = vector1[0] + vector2[0]
    speed_y = vector1[1] + vector2[1]
    vector1 = (speed_x, speed_y)
    return vector1

def vector2_mult(vector1: tuple, vector2: tuple):
    speed_x = vector1[0] * vector2[0]
    speed_y = vector1[1] * vector2[1]
    vector1 = (speed_x, speed_y)
    return vector1

def vector2_dir(vector): # returns a pair of values, can only be 0, 1 or -1
    vector_x, vector_y = vector
    dir_x = (vector_x > 0) - (vector_x < 0)
    dir_y = (vector_y > 0) - (vector_y < 0)
    return dir_x, dir_y

def vector2_decay(player: Player, vel_dx: float | int = 1, vel_dy: float | int = 1):
    vel_mult_x = sech((player.speed_value() * vel_dx) / (VELOCITY_DECAY_X * SPEED_IMPACT))
    vel_mult_y = sech((player.speed_value() * vel_dy) / (VELOCITY_DECAY_Y * SPEED_IMPACT))
    vel_mult = (vel_mult_x, vel_mult_y)
    player.speed = vector2_mult(player.speed, vel_mult)