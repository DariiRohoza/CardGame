from typing import Optional

from card_class import Card
from deck_class import Deck
from move_tech_class import MoveTech
from constants_libraries import START_PLAYER_HEALTH, ACTION_AMOUNT, INITIAL_SPEED, PLAYER_HAND_SIZE


class Player:
    def __init__(self):
        self.name: str = "PLACEHOLDER"
        self.hand: list[Card] = []
        self.deck: Deck = Deck()
        self.health: float = START_PLAYER_HEALTH

        self.parry_card: Optional[Card] = None
        self.parry_time: int = 0

        self.defending: int = 0
        self.attack_stack: float = 0

        self.action_count: int = ACTION_AMOUNT
        self.speed: tuple[float, float] = INITIAL_SPEED
        self.active_tech: Optional[MoveTech] = None
        self.passive_tech: list[MoveTech] = []

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

    def transfer_active_tech(self, replacement: Optional[MoveTech] = None) -> str:
        tech = self.active_tech
        if replacement is not None:
            self.active_tech = replacement
            print(f" <*> Updated {self.name}'s active tech to be {self.active_tech}")
        else:
            self.active_tech = None

        if tech is None:
            return "none"
        elif tech not in self.passive_tech:
            self.passive_tech.append(tech)
            print(f" <*> Added {tech} to {self.name}'s passive tech list")
            return "added"
        idx = self.passive_tech.index(tech)
        for _ in range(tech.chain_count + 1):
            self.passive_tech[idx].add_chain()
        print(f" <*> CHAIN added to a tech in {self.name}'s passive tech list ({tech} -> {self.passive_tech[idx]})")
        return "chain"

    def fill_hand(self):
        if len(self.deck) == 0:
            self.deck.fill()
        to_fill = PLAYER_HAND_SIZE - len(self.hand)
        for _ in range(to_fill):
            self.hand.append(self.deck.draw_card())

    def move_to_deck(self, card: Card):
        self.hand.remove(card)
        self.deck.return_card(card)

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