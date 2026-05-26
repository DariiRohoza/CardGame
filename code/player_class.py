from card_class import Card
from constants_libraries import START_PLAYER_HEALTH, ACTION_AMOUNT, INITIAL_SPEED

class Player:
    def __init__(self):
        self.name: str = "PLACEHOLDER"
        self.hand: list[Card] = []
        self.health: float = START_PLAYER_HEALTH

        self.defending: int = 0
        self.attack_stack: float = 0

        self.action_count: int = ACTION_AMOUNT
        self.speed = INITIAL_SPEED  # 2d vector, format : (vertical, horizontal)
        self.move_tech = "" # format : "tech : modifier, modifier"

        # only values from SUIT_LIB or an empty string ""
        self.weakness: str = ""
        self.strength: str = ""

    def __str__(self):
        if self.health <= 0.00:
            return f"A dead player"
        return (f"A player at {self.health:,.2f}hp; {self.action_count} speed; {self.defending} defense stacks; "
                f"Weakness: {self.weakness}; Strength: {self.strength}")

    def speed_value(self) -> int:
        return (self.speed[0] ** 2 + self.speed[1] ** 2) ** 1/2

    def multiply_velocity(self, modifier):
        self.speed = (self.speed[0] * modifier, self.speed[1] * modifier)

    def rename(self, name: str | None = None):
        if name is not None:
            self.name = name
            return name
        while True:
            new_name = input(f"Please enter a new name for the player: ")
            if len(new_name) == 0:
                continue
            break
        self.name = new_name
        return new_name