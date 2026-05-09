from player_class import Player
from gameloop_class import GameLoop

if __name__ == "__main__":
    game_loop = GameLoop()

    player = Player()
    player.rename("BOB")
    game_loop.add_player(player)

    player2 = Player()
    player2.rename("ALEX")
    game_loop.add_player(player2)

    game_loop.initialize_game()
    game_loop.main_loop()

# TODO : IMPLEMENT THE FOLLOWING IN THE FUTURE

# FEATURE : Add file saving, having a default file with a relative / absolute path so that games are saved to those files

# FEATURE : player move choice, changing a move choice is an ACTION, all are started with "stationary"
    # B-hop : removes an additional defense stack from the enemy if your strength matches the card you used
    # Hyper : 1/3 chance to increase the rank of a random card by 3 every action
    # Super : constant x0.80 damage reduction
    # Ultra : 5/8 chance to crit (x1.5 dmg) on attacks

# FEATURE : negative ranks as healing mechanics because math is math
    # ACTION : invert card (2 actions), can be used together with negative ranks to make a rapid supply of healing cards