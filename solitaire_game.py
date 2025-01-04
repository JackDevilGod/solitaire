import re

from typing import TYPE_CHECKING
from copy import deepcopy
from solitaire_classes import Deck, Desk, SuitStack, WrongCard, MisMatchColour

if TYPE_CHECKING:
    from solitaire_classes import Card


class FailedExecution(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class Solitaire:
    _suits: list[str] = ["S", "D", "C", "H"]
    _columns: list[str] = [str(_) for _ in range(1, 8)]
    _places: list[str] = (_columns +
                          ["drawn"] +
                          _suits)

    def __init__(self):
        self.card_deck: Deck = Deck()
        self.card_deck.shuffle(5)
        self.card_spread: Desk = Desk(self.card_deck)
        self.suite_stacks: list[SuitStack] = [SuitStack(_)
                                              for _ in Solitaire._suits]
        self.drawn_stack: list["Card"] = []

    @property
    def finished(self) -> bool:
        return all([_.complete for _ in self.suite_stacks])

    def draw(self) -> None:
        if self.card_deck.amount_cards == 0:
            raise IndexError("card deck is empty.")

        drawn: list[Card] = []

        while len(drawn) < 3:
            drawn.append(self.card_deck.draw())

            if self.card_deck.amount_cards == 0:
                self.drawn_stack = drawn + self.drawn_stack
                raise IndexError("Deck ran out of cards, while drawing.")
        self.drawn_stack = drawn + self.drawn_stack

    def reset_deck(self) -> None:
        if self.card_deck.amount_cards != 0:
            raise IndexError("Card deck not empty.")

        self.card_deck.reset(self.drawn_stack)
        self.drawn_stack.clear()

    def from_to(self, from_place: str, to_place: str) -> None:
        if (from_place not in Solitaire._places or
                to_place not in Solitaire._places):
            raise ValueError("Invalid places. Use the following.\n" +
                             "|".join(Solitaire._places))
        if to_place == "drawn":
            raise ValueError("Can not put cards back into draw pile.")

        temp_save: Solitaire = deepcopy(self)
        try:
            if from_place in Solitaire._suits:
                from_card: "Card" = self.suite_stacks[
                    Solitaire._suits.index(from_place)].pull()
            if from_place in Solitaire._columns:
                from_card = self.card_spread.get_out(int(from_place))
            else:
                from_card = self.drawn_stack.pop(0)
        except IndexError:
            self = temp_save
            raise FailedExecution("Failed to get the card.")

        try:
            if to_place in Solitaire._suits:
                self.suite_stacks[
                    Solitaire._suits.index(to_place)].push(from_card)
            else:
                self.card_spread.put_in(from_card, int(to_place))
        except (WrongCard, ValueError, MisMatchColour) as e:
            print(e)
            self = temp_save
            return

    def __repr__(self) -> str:
        top_bar: str = " ".join([_.__repr__() for _ in self.suite_stacks] +
                                ["   "] +
                                [self.drawn_stack[0].__repr__()
                                 if len(self.drawn_stack) > 0
                                 else "EEE"] +
                                ["..."
                                 if self.card_deck.amount_cards > 0
                                 else "EEE"])
        return top_bar + "\n" + self.card_spread.__repr__() + '\n'


def main():
    game: Solitaire = Solitaire()
    c_pattern: str = r"from (.+) to (.+)"

    while not game.finished:
        print(game)

        # region user input
        print("draw | reset | 'from _ to _'")
        command: str = input().lower()

        if command == "draw":
            try:
                game.draw()
            except IndexError as i:
                print(i)
        elif command == "reset":
            try:
                game.reset_deck()
            except IndexError as i:
                print(i)
        else:
            decoded_command = re.fullmatch(c_pattern, command)

            if decoded_command is None:
                print("Invalid command")
                continue

            from_p, to_p = decoded_command.groups()
            try:
                game.from_to(from_p, to_p)
            except ValueError as v:
                print(v)
        # end region


if __name__ == '__main__':
    main()
