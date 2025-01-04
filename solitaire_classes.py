from copy import deepcopy

from cards import Deck, Card, Literal


class MisMatchColour(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class WrongCard(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class Desk:
    def __init__(self, deck: "Deck"):
        self.desk: list[tuple[list["Card"], list["Card"]]] = [([], [])
                                                              for _ in
                                                              range(7)]

        for layer in range(7):
            for index in range(layer, 7):
                if index == layer:
                    self.desk[index][1].append(deck.draw())
                else:
                    self.desk[index][0].append(deck.draw())

    def put_in(self, card: "Card", column: int) -> None:
        if column < 0 or column > 7:
            raise ValueError("Invalid column id")

        if not isinstance(card, Card):
            raise ValueError("Wrong class")

        if len(self.desk[column][1]) == 0:
            if card.value != 13:
                raise WrongCard("Only kings are allowed empty columns.")
        else:
            if self.desk[column][1][-1].color == card.color:
                raise MisMatchColour(
                    "Can not put the same colour on each other.")

            if self.desk[column][1][-1].value - 1 != card.value:
                raise WrongCard(
                    "Card needs to be one less then card already there.")

        self.desk[column][1].append(card)

    def get_out(self, columns: int) -> "Card":
        if len(self.desk[columns][1]) == 0:
            raise IndexError("Column does not have cards.")

        if len(self.desk[columns][1]) > 1:
            return self.desk[columns][1].pop()

        if len(self.desk[columns][0]) > 0:
            self.desk[columns][1].append(self.desk[columns][0].pop())
        return self.desk[columns][1].pop(0)

    def move_card(self, from_column: int, to_column: int) -> None:
        desk_save = deepcopy(self.desk)

        try:
            card = self.get_out(from_column)
            self.put_in(card, to_column)
        except (IndexError, MisMatchColour, WrongCard, ValueError) as e:
            print(e)
            self.desk = desk_save

    def __repr__(self) -> str:
        r_list: list[list[str]] = []

        for id, column in enumerate(self.desk):
            hidden, shown = column
            if len(r_list) < (len(hidden) + len(shown)):
                for _ in range(len(r_list), (len(hidden) + len(shown))):
                    r_list.append(["   " for _ in range(id)])

            for index in range(len(r_list)):
                if index < len(hidden):
                    r_list[index].append("...")
                elif index < (len(hidden) + len(shown)):
                    r_list[index].append(shown[index - len(hidden)].__repr__())
                else:
                    r_list[index].append("   ")

        return "\n".join([" ".join(_) for _ in r_list]).removesuffix("\n")


class SuitStack:
    _suit_encode: dict[str | None, str] = {"S": "♠", "C": "♣",
                                           "H": "♥", "D": "◆", None: ""}

    def __init__(self, suite: Literal["S", "C", "H", "D"]):
        if suite not in ["S", "C", "H", "D"]:
            raise ValueError("Suit is invalid.")

        self.suite: Literal["S", "C", "H", "D"] = suite
        self.stack: list["Card"] = []

    @property
    def complete(self) -> bool:
        return (len(self.stack) == 13)

    def push(self, card: "Card") -> None:
        if card.suit != self.suite:
            raise WrongCard("Wrong suite of card for the stack.")

        if len(self.stack) == 0:
            if card.value == 1:
                self.stack.append(card)
                return
            else:
                raise WrongCard("Can not start stack on a non Ace.")

        if self.stack[-1].value + 1 == card.value:
            self.stack.append(card)
        else:
            raise WrongCard('Card is not next in stack.')

    def pull(self) -> "Card":
        return self.stack.pop()

    def __repr__(self) -> str:
        if len(self.stack) == 0:
            return f".{SuitStack._suit_encode[self.suite]}."

        return self.stack[-1].__repr__()


def main():
    d = Deck()
    desk = Desk(d)
    print(d.amount_cards)
    print(desk)
    desk.get_out(0)
    desk.get_out(3)
    print(desk)
    try:
        desk.get_out(0)
    except IndexError:
        print("column empty works")

    desk.put_in(Card(5, "S"), 1)
    print(desk)
    desk.move_card(2, 0)
    print(desk)
    desk.move_card(1, 0)
    print(desk)


if __name__ == '__main__':
    main()
