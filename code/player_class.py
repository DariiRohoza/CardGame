from card_class import Card
from constants_libraries import START_PLAYER_HEALTH, ACTION_AMOUNT, INITIAL_SPEED

class Player:
    def __init__(self):
        # hand | passive_tech : are not shown
        self.name: str = "PLACEHOLDER"
        self.hand: list[Card] = []
        self.health: float = START_PLAYER_HEALTH

        self.defending: int = 0
        self.attack_stack: float = 0

        self.action_count: int = ACTION_AMOUNT
        self.speed: tuple[float, float] = INITIAL_SPEED
        self.active_tech: str = ""
        self.passive_tech: dict[str, str] = {} # tech: modifiers

        # only values from SUIT_LIB or an empty string ""
        self.weakness: str = ""
        self.strength: str = ""

    def __str__(self):
        if self.health <= 0.00:
            return f"A dead player"
        return (f"A player at {self.health:,.2f}hp; {self.action_count} speed; {self.defending} defense stacks; "
                f"Weakness: {self.weakness}; Strength: {self.strength}")

    def print_speed(self, units: bool = False):
        if units:
            return f"({self.speed[0]:,.2f} m/s, {self.speed[1]:,.2f} m/s)"
        return f"({self.speed[0]:,.2f}, {self.speed[1]:,.2f})"

    def speed_value(self) -> int:
        return ((self.speed[0] ** 2) + (self.speed[1] ** 2)) ** (1/2)

    def rename(self, name: str | None = None):
        if name is not None:
            self.name = name
            return name
        while True:
            new_name = input(f"Please enter a new name for the player: ")
            if 0 <= len(new_name) <= 7:
                continue
            break
        self.name = new_name
        return new_name