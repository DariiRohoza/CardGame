from pyfiglet import figlet_format
from pyinputplus import inputInt
from time import sleep

from gameloop_actions import (attack_turn, stack_attack_value, player_parry, refurbish_card_suit, increase_card_rank,
                              merge_card_rank, stylize_card, drop_half_cards, defend, move_player)
from printing_func import print_hand, print_players
from vector2_func import vector2_decay

from player_class import Player
from constants_libraries import MIN_GAME_PLAYERS, MAX_GAME_PLAYERS


class GameLoop:
    def __init__(self):
        self.player_list: list[Player] = []
        self.counter: int = 0
        self.action_counter: int = 0
        self.conclude_game: bool = False

    def __str__(self):
        return f"A game with {len(self.player_list)} players"

    def initialize_game(self):
        if len(self.player_list) < MIN_GAME_PLAYERS:
            print(f"Insufficient players, skipping...")
        else:
            print(f"All requirements have been fulfilled, the game is starting...")
            for idx, item in enumerate(self.player_list):
                self.player_list[idx].fill_hand()

    def add_player(self, new_player: Player):
        if len(self.player_list) == MAX_GAME_PLAYERS:
            print(f"Player limit reached, can't add more players, skipping...")
        elif new_player.hand:
            print(f"Player hand needs to be empty to be added, skipping...")
        else:
            self.player_list.append(new_player)

    def main_loop(self):
        while not self.conclude_game:
            sleep(0.35)
            velocity_modifier = 1
            no_decay = False
            curr_player = self.fetch_curr()

            print(f">>> It is now {curr_player.name}'s turn\n\n"
                  f"Pick an options from those below by inputting the number in front of it\n"
                  f"00 : Conclude Game / Quit\n"
                  f"01 : Attack Player\n"
                  f"02 : Stack Attack Value\n"
                  f"03 : Start a Parry\n"
                  f"04 : Refurbish Card Suit\n"
                  f"05 : Increase Card Rank\n"
                  f"06 : Merge Card Rank\n"
                  f"07 : Stylize Card\n"
                  f"08 : Exchange half of your hand\n"
                  f"09 : Defend\n"
                  f"10 : Move\n"
                  f"11 : View Other Players\n"
                  f"12 : View Hand\n")

            user_choice_option = inputInt(prompt="User input: ", min=0, max=12)

            match user_choice_option:
                case 0:
                    if input(f" - Type \"quit\" to stop the program: ").lower() == "quit":
                        self.conclude_game = True

                case 1: attack_turn(curr_player, self.player_list)
                case 2: stack_attack_value(curr_player)
                case 3: player_parry(curr_player)
                case 4: refurbish_card_suit(curr_player)
                case 5: increase_card_rank(curr_player)
                case 6: merge_card_rank(curr_player)
                case 7: stylize_card(curr_player)
                case 8: drop_half_cards(curr_player)
                case 9: defend(curr_player, 2)
                case 10: velocity_modifier = move_player(curr_player)
                case 11: print_players(self.player_list, curr_player)
                case 12: print_hand(curr_player, curr_player.hand)

            if 0 < user_choice_option <= 10:
                self.iterate_turn()

            if len(self.player_list) == 1:
                print(f">>> A winner has been found!\n")
                self.conclude_game = True
                game_winner(self.player_list[0])

            if curr_player.speed_value() > 0 and self.action_counter == 0 and not no_decay:
                vector2_decay(curr_player, velocity_modifier, velocity_modifier)
                print(f">>> Applied velocity decay to {curr_player.name} "
                      f"(final speed : {curr_player.speed_value():,.2f})\n)")

            if curr_player.parry_time > 0 and self.action_counter == 0:
                curr_player.parry_time -= 1

            if curr_player.parry_time == 0 and curr_player.parry_card is not None:
                parry_card = curr_player.parry_card
                curr_player.parry_card = None
                print(f">>> {curr_player.name}'s parry card expired : {parry_card}\n")

    def iterate_turn(self):
        self.action_counter += 1
        self.counter %= len(self.player_list)
        if self.action_counter >= self.player_list[self.counter].action_count:
            self.counter += 1
            self.action_counter = 0
        self.counter %= len(self.player_list)

    def fetch_curr(self) -> Player:
        return self.player_list[self.counter]


def game_winner(winner: Player):
    print(f"The player that has eliminated all the other players and won is!\n",
          figlet_format(f"{winner.name}", font="larry3d"))