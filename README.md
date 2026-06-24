# CardGame

## Launching the game

1. Open the folder in an IDE like Visual Studio Code or Pycharm
2. (If needed) Install at minimum python 3.14
3. (If needed) Install the pyfiglet module and/or the rich module
4. Open and launch the main.py file
5. Enjoy!

### Modifying Important Variables

Assuming you have already been able to launch the game, follow these steps:

1. Open the constants_libraries.py file
2. Using the table below, navigate to the variable you wish to change and modify the value assigned to it
3. Enjoy!

| Variable                | Consequence                                                                                                                                                                                                       |
|:------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ACTION_MULTIPLIER       | Automatically adjusts the game balance to the amount of actions the players have.                                                                                                                                 |
|                         |
| MIN_GENERATED_CARD_RANK | Changes the minimum generated rank, going below 1 is not advised.                                                                                                                                                 |
| MAX_GENERATED_CARD_RANK | Changes the maximum generated rank.                                                                                                                                                                               |
|                         |
| MAX_DECK_SIZE           | Changes the size of the deck used in the game.                                                                                                                                                                    |
|                         |
| START_PLAYER_HEALTH     | The health a player has at the beginning of the game.                                                                                                                                                             |
| ACTION_AMOUNT           | The amount of actions that can be performed by a player in 1 round.                                                                                                                                               |
| INITIAL_SPEED           | A 2D vector in the form (x, y) aka (horizontal, vertical) that determines the initial speed of all players.                                                                                                       |
|                         |
| MIN_GAME_PLAYERS        | Minimum amount of players, going below 2 is not advised as you will be forced to attack yourself.                                                                                                                 |
| MAX_GAME_PLAYERS        | Maximum amount of players.                                                                                                                                                                                        |
| PLAYER_HAND_SIZE        | Amount of cards a player has access to at a given time, should be smaller than MAX_DECK_SIZE / MAX_GAME_PLAYERS.                                                                                                  |
|                         |
| STACK_RANK_LIMIT        | Maximum rank that can be used for the "Stack Attack Value" action.                                                                                                                                                |
| PARRY_LONGEVITY         | The amount of turns that a parry lasts for, includes the turn the parry was initiated.                                                                                                                            |
| SUIT_PENALTY            | Penalty that is applied to mergers of cards with different suits.                                                                                                                                                 |
| IDENTICAL_BOOST         | Bonus added for identical cards during merging.                                                                                                                                                                   |
|                         |
| MIN_MOVE                | The minimum amount of moves that can be performed during the "Move" action.                                                                                                                                       |
| SPEED_IMPACT            | The value by which your speed is devided to get its effect on the amount of moves, damage and actions.                                                                                                            |
| VELOCITY_DECAY_X        | The variable by which the horizontal component of the player vector is modified to simulate air-drag and other factors that passively reduce the velocity of a given object, scales with the speed of the player. |
| VELOCITY_DECAY_Y        | The variable by which the verctical component of the player vector is modified to simulate air-drag and other factors that passively reduce the velocity of a given object, scales with the speed of the player.  | 
|                         |
| DEFENSE_STRENGTH_LIM    | The threshold past which attacker strength has a smaller impact on damage.                                                                                                                                        |
| DEFENSE_WEAKNESS_LIM    | The threshold past which target weakness has no impact on damage.                                                                                                                                                 |
| DEFENSE_THRESHOLD       | The threshold past which damage is completely absobed but defense is removed at a faster pace.                                                                                                                    |
| MIN_WEAKNESS_CRITICAL   | Minimum additional defense stacks removed from the target if the attacking card has the same suit as the target's weakness.                                                                                       |

Do not change the variables above the ACTION_MULTIPLIER unless you know what you're doing, it is key those stay the way they are.
