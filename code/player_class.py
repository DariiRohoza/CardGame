from card_class import Card
from constants_libraries import MOVEMENT_TECH_LIB, START_PLAYER_HEALTH, ACTION_AMOUNT, INITIAL_SPEED

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
        self.active_tech: str = "" # after being used as an active, moves to the passive list to be used again
        self.passive_tech: dict[str, str] = {} # (tech + modifier) : CHAIN(s)

        # only values from SUIT_LIB or an empty string ""
        self.weakness: str = ""
        self.strength: str = ""

    def __str__(self):
        if self.health <= 0.00:
            return f"A dead player"
        return (f"{self.name}; {self.health:,.2f}hp with {self.defending} defense stacks "
                f"(Strength: {self.strength} & Weakness: {self.weakness})")

    def print_speed(self, units: bool = False):
        if units:
            return f"({self.speed[0]:,.2f} m/s, {self.speed[1]:,.2f} m/s)"
        return f"({self.speed[0]:,.2f}, {self.speed[1]:,.2f})"

    def speed_value(self) -> int:
        return ((self.speed[0] ** 2) + (self.speed[1] ** 2)) ** (1/2)

    def transfer_active_tech(self, replacement: str | None = None) -> str:
        chain = ""
        active_tech = self.active_tech
        if replacement is not None and replacement in MOVEMENT_TECH_LIB.values():
            self.active_tech = replacement
            print(f" <*> Updated {self.name}'s active tech to be {self.active_tech}")

        if active_tech == "":
            return "none"
        if " \\ " in active_tech:
            active_tech, chain = active_tech.split(" \\ ", maxsplit=1)
            chain = " \\ " + chain
        if active_tech not in self.passive_tech.keys():
            self.passive_tech.update({active_tech: chain})
            print(f" <*> Added {active_tech}{chain} to {self.name}'s passive tech list")
            return "added"
        self.passive_tech[active_tech] += " \\ CHAIN" + chain
        print(f" <*> CHAIN modifier added to {active_tech} in {self.name}'s passive tech list")
        return "chain"

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