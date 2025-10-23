from project.task4.bot import Bot
from typing import Optional, Any
from project.task4.bet import Bet


class FixBot(Bot):
    """
    this bot always placing a fixed bet (same amount and num)
    """

    def __init__(
        self,
        bot_id: str,
        bankroll: int,
        amount: int,
        min_bet: int = 1,
        fixed_kind: str = "color",
        fixed_val: Any = "black",
    ) -> None:
        """
        FixBot constructor

        args:
            bot_id (str): id of this bot
            bankroll (int): bankroll of this bot
            min_bet (int) (default=1): minimum bet value
            fixed_knd (str) (default="color"): fixed kind = color
            fixed_val (Any) (default="black): fixed color = black
        returns:
            None
        """
        super().__init__(bot_id, bankroll, min_bet)
        self.fix_amount = amount
        self.fix_kind = fixed_kind
        self.fix_value = fixed_val

    def betting(self) -> Optional[Bet]:
        """
        funtion for place a bet

        returns:
            pass or Bet
        """
        if self.bankroll < max(self.min_bet, self.fix_amount):
            return None
        return Bet(amount=self.fix_amount, kind=self.fix_kind, value=self.fix_value)
