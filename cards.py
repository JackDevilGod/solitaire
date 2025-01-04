from typing import Literal
from math import trunc
from random import shuffle
from copy import deepcopy


class Card:
    _suit_encode: dict[str | None, str] = {"S": "♠", "C": "♣",
                                           "H": "♥", "D": "◆", None: ""}
    _value_encode: dict[int, str] = ({_: " " + str(_) for _ in range(2, 10)} |
                                     {10: "10"} |
                                     {1: " A", 11: " J", 12: " Q", 13: " K",
                                      14: "JKR"})

    def __init__(self, value: int,
                 suit: Literal["S", "C", "H", "D", None]) -> None:
        if value <= 13:
            if value < 1:
                raise ValueError("Invalid card value")
            if suit not in ["S", "C", "H", "D"]:
                raise ValueError("Invalid suit")
        else:
            if value != 14:
                raise ValueError("Invalid value for card")
            if suit is not None:
                raise ValueError("14 can only have a None suit")

        self.value: int = value
        self.suit: str | None = suit

        if self.suit in ["H", "D"]:
            self.color: Literal["red", "black", None] = "red"
        elif self.suit in ["C", "S"]:
            self.color = "black"
        else:
            self.color = None

    def __repr__(self) -> str:
        return (f"{Card._value_encode[self.value]}" +
                f"{Card._suit_encode[self.suit]}")


class Deck:
    _proper_deck: list[Card] = []
    for suit in ["S", "H", "C", "D"]:
        for value in range(1, 14):
            _proper_deck.append(Card(value, suit))

    def __init__(self, amount_jokers: int = 0) -> None:
        self.cards: list[Card] = deepcopy(Deck._proper_deck)

        for _ in range(amount_jokers):
            self.cards.append(Card(14, None))

    @property
    def amount_cards(self) -> int:
        return len(self.cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise IndexError("Deck has ran out of cards")

        return self.cards.pop()

    def put_top(self, card: Card) -> None:
        self.cards.append(card)

    def put_bottom(self, card: Card) -> None:
        self.cards.insert(0, card)

    def shuffle(self, times: int = 1) -> None:
        if times < 0:
            raise ValueError("Can not shuffle negative times.")

        for _ in range(times):
            shuffle(self.cards)

    def reset(self, deck: list[Card] | None = None) -> None:
        if deck is None:
            self.cards = deepcopy(Deck._proper_deck)
        else:
            self.cards = deepcopy(deck)

    def __repr__(self) -> str:
        length: int = trunc((len(self.cards))**0.5)
        r_list: list[str] = [_.__repr__() + " " for _ in self.cards]
        insert_steps: int = trunc(len(r_list)/length)

        for index in range(insert_steps, 0, -1):
            r_list.insert(index * length, "\n")

        return "".join(r_list).removesuffix("\n")


def main():
    d = Deck(2)
    print(d)
    print(d.amount_cards)
    while d.amount_cards > 1:
        d.draw()
        print(d)


if __name__ == '__main__':
    main()
