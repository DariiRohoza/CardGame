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