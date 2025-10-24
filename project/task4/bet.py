from project.task4.wheel_ import Color
from enum import Enum


class Bet:
    """
    class for bets
    """

    def __init__(self, amount: int, kind: str, value: int | str) -> None:
        """
        constructor for bet

        args:
            quantity: amount
            kind: "number" | "color" | "parity" | "range" (i implement "number", "color" and "parity")
            value: for kind=="number" -> int; for "color" -> "red"/"black"; for "parity" -> "even"/"odd"
        """
        self.amount = amount
        self.kind = kind
        self.value = value


class ForBet(Enum):
    """
    class for enum:

    enums variables:

    """

    NUMBER = "number"
    PARITY = "parity"
    EVEN = "even"
    ODD = "odd"
