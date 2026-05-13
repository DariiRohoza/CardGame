# CardGame

## Launching the game

1. Open the folder in an IDE like Visual Studio Code or Pycharm
2. (If needed) Install at minimum python 3.12
3. (If needed) Install the pyfiglet module
4. Open and launch the main.py file
5. Enjoy!

### Modifying Important Variables

Assuming you have already been able to launch the game, follow these steps:

1. Open the constants_libraries.py file
2. Using the table below, navigate to the variable you wish to cahnge and modify the value assigned to it
3. Enjoy!

| Variable | Consequence |
|:-------:|:-------|
| ACTION_MULTIPLIER | Automatically adjusts the game balance to the amount of actions the players have. |
| MIN_GENERATED_CARD_RANK | Changes the minimum generated rank, going below 1 is not advised |
| MAX_GENERATED_CARD_RANK | Changes the maximum generated rank |
| MAX_DECK_SIZE | Changes the size of the deck used in the game |
| START_PLAYER_HEALTH | The health a player has at the beginning of the game |
| ACTION_AMOUNT | The amount of actions that can be performed by a player in 1 round |
| MIN_GAME_PLAYERS | Minimum amount of players, going below 2 is not advised as you will be forced to attack yourself |
| MAX_GAME_PLAYERS | Maximum amount of players |
| PLAYER_HAND_SIZE | Amount of cards a player has access to at a given time, should be smaller than MAX_DECK_SIZE / MAX_GAME_PLAYERS |
| STACK_RANK_LIMIT | Maximum rank that can be used for the "Stack Attack Value" action |
| SUIT_PENALTY | Penalty that is applied to mergers of cards with different suits |
| IDENTICAL_BOOST | Bonus added for identical cards during merging |
| DEFENSE_STRENGTH_LIM | The threshold past which attacker strength has a smaller impact on damage |
| DEFENSE_WEAKNESS_LIM | The threshold past which target weakness has no impact on damage |
| DEFENSE_THRESHOLD | The threshold past which damage is completely absobed but defense is removed at a faster pace |
| MIN_WEAKNESS_CRITICAL | Minimum additional defense stacks removed from the target if the attacking card has the same suit as the target's weakness |

## Future Plans

**FEATURE** : Add file saving, having a default file with a relative / absolute path so that games are saved to those files

**FEATURE** : player move choice, changing a move choice is an ACTION, all are started with "stationary"
1. _B-hop_ : removes an additional defense stack from the enemy if your strength matches the card you used
2. _Hyper_ : 1/3 chance to increase the rank of a random card by 3 every action
3. _Super_ : constant x0.80 damage reduction
4. _Ultra_ : 5/8 chance to crit (x1.5 dmg) on attacks
