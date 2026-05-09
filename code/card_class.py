from constants_libraries import suit_lib, style_lib, MIN_GENERATED_CARD_RANK

class Card:
    def __init__(self):
        self.card_value: tuple[int, int] = (0,0) # suit 1st, rank 2nd
        self.style: str = ""

    def __str__(self):
        if self.card_value is None or self.style is None:
            return (f"Value(s) missing, can't print properly, skipping..."
                    f"--> Value: {self.card_value}, Style: {self.style}")
        return f"{self.style} {str(self.card_value[1]) + suit_lib[self.card_value[0]]} card!"

    def add_info(self, suit: int, rank: int, style: str):
        # Validating {Suit} and {Rank}
        if type(suit) is not int or type(rank) is not int:
            raise TypeError(f"Suit ({suit}) or rank {rank}: Invalid type")
        elif suit not in suit_lib.keys() or rank < MIN_GENERATED_CARD_RANK:
            raise ValueError(f"Suit ({suit}) or rank {rank}: Invalid value")
        elif self.card_value != (0,0):
            raise ValueError(f"A value is already assigned, skipping...")
        else:
            self.card_value = (suit, rank)

        # Validating {Style}
        if type(style) is not str:
            raise TypeError(f"Style {style}: Invalid type")
        elif style not in style_lib:
            raise ValueError(f"Style {style}: Invalid value")
        elif self.style != "":
            raise ValueError(f"A value is already assigned, skipping...")
        else:
            self.style = style