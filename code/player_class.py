from card_class import Card
from constants_libraries import START_PLAYER_HEALTH, ACTION_AMOUNT

class Player:
    def __init__(self):
        self.name: str = "PLACEHOLDER"
        self.hand: list[Card] = []
        self.health: float = START_PLAYER_HEALTH
        self.action_count: int = ACTION_AMOUNT
        self.defending: int = 0
        self.attack_stack: float = 0

        # only values from suit_lib and an empty string ""
        self.weakness: str = ""
        self.strength: str = ""

    def __str__(self):
        if self.health <= 0.00:
            return f"A dead player"
        return (f"A player at {self.health:,.2f}hp; {self.action_count} speed; {self.defending} defense stacks; "
                f"hand hidden; --> Weakness: {self.weakness}; Strength: {self.strength}")

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