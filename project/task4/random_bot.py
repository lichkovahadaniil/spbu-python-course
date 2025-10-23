from project.task4.bot import Bot
from typing import Optional
from project.task4.bet import Bet
import random as r


class RandomBot(Bot):
    """
    this bot randomly chooses a color or bets on a number
    """

    def betting(self) -> Optional[Bet]:
        """
        funtion for place a bet

        returns:
            pass or Bet
        """
        if self.bankroll < self.min_bet:
            return None
        amt = r.randint(self.min_bet, self.bankroll)
        kind = r.choice(["color", "number", "parity"])
        val: int | str = 0
        if kind == "color":
            val = r.choice(["red", "black"])
        elif kind == "parity":
            val = r.choice(["even", "odd"])
        else:
            val = r.randint(0, 36)
        return Bet(amount=amt, kind=kind, value=val)
