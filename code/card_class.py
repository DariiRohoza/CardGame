from constants_libraries import STYLE_LIB, SUIT_LIB, MIN_GENERATED_CARD_RANK

class Card:
    def __init__(self):
        self.suit: int = -1
        self.rank: int = 0
        self.style: str = ""

    def __str__(self):
        if self.suit == -1 or self.rank == 0 or self.style == "":
            return (f"Value(s) missing, can't print properly, skipping..."
                    f"--> Value: {self.rank}{SUIT_LIB[self.suit]}, Style: {self.style}")
        return f"{self.style} {self.rank}{SUIT_LIB[self.suit]} card!"

    def add_info(self, suit: int, rank: int, style: str):
        # validating suit and rank
        if type(suit) is not int or type(rank) is not int or type(style) is not str:
            raise TypeError(f"Suit ({suit}) or rank {rank} or style {style}: Invalid type")
        elif suit not in SUIT_LIB.keys() or rank < MIN_GENERATED_CARD_RANK or style not in STYLE_LIB:
            raise ValueError(f"Suit ({suit}) or rank {rank} or style {style}: Invalid value")
        elif self.suit != -1 or self.rank != 0 or self.style != "":
            raise ValueError(f"Suit ({suit}) or rank {rank} or style {style}: A value is already assigned")
        else:
            self.suit = suit
            self.rank = rank
            self.style = style