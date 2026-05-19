from random import shuffle, randint, choices
from card_class import Card
from constants_libraries import (suit_lib, style_lib, style_lib_weights,
                                 MIN_GENERATED_CARD_RANK, MAX_GENERATED_CARD_RANK, MAX_DECK_SIZE)

class Deck:
    def __init__(self):
        self.cards: list[Card] = []

    def __len__(self):
        return len(self.cards)

    def print_deck(self):
        for item in self.cards:
            print(item)

    def draw_card(self) -> Card:
        if len(self) == 0:
            print(f"The deck is empty, calling fill to complete the new deck before drawing a card")
            self.fill()
        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)

    # fill the deck to the brim with random cards
    def fill(self):
        cards_to_add = MAX_DECK_SIZE - len(self.cards)
        for _ in range(cards_to_add):
            self.cards.append(generate_card())

def generate_card() -> Card:
    card = Card()
    suit_choice = randint(0, len(suit_lib)-1)
    rank_choice = randint(MIN_GENERATED_CARD_RANK, MAX_GENERATED_CARD_RANK)
    style_choice = choices(list(style_lib.keys()), weights=style_lib_weights, k=1)[0]
    card.add_info(suit_choice, rank_choice, style_choice)
    return card