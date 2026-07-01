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

## Tips & Tricks
Printing players and printing your own hand can be used without action cost.

#### Attack Player
1. If the opponent has lots of defense, you can attack them with cards they are weak against, draining the defense they have until you can use a strong card to deal a lot of damage.
2. Going faster than your opponent increases your damage and decreses theirs.

#### Stack Attack Value
1. Using cards with higher style values is more efficient than spamming weak cards for stacking value.
2. Strength gives a 1.5x multiplier for the attack stack, allowing players to get up to 52.5 value from a singular card (given that STACK_RANK_LIMIT = 7).

#### Parrying
1. Speed modifiers are added before parrying, a stronger parry card will as such be more effective against faster opponents.
2. Weakness and Strength affect the effectiveness of parrying.

#### Refurbishing Card Suits
1. This action will remove your weakness if the target suit is the same as your weakness.
2. It will grant you strength with the chosen suit.

#### Card Rank Increase
1. Speed is very wffective at buffing this action, to the point that going about 200 m/s will make this action more effective than merging.
2. This action grants a singular defense stack every time it is activated.

#### Merging Cards
1. Can be used to slowly cycle your deck unlike rank increasing.

#### Stylize
1. Style is the most important value for increasing damage and being able to increase it for already strong cards is a good idea.

#### Discarding Cards
1. Can be used for deck-cycling to regain stronger cards after using them.

#### Defending
1. The first couple defense stacks are stronger than the rest, as such even a couple defense staxks combined with fast movemenr speed can significantly increse survivability.

#### Movement
1. Dashes that have "NONE" as one of the direction can have that none and oone of the dashes removed (example: dash-none-left can be weitten as dash-left).
2. Certain sequences of movements can be used to perform tech that buff movement speed significantly as well as buffing certain actions.
