from project.task4.bot import Bot
from typing import Optional
from project.task4.bet import Bet


class MurderBot(Bot):
    """
    class for murder bot, who increases or reduces his bet after each lose (for input value)
    """

    def __init__(
        self,
        bot_id: str,
        bankroll: int,
        min_bet: int = 1,
        base_bet: int = 1,
        inc_red: int = 2,
    ) -> None:
        """
        MurderBot constructor

        args:
            bot_id (str): id of this bot
            bankroll (int): bankroll of this bot
            min_bet (int) (default=1): minimum bet value
            base_bet (int) (default=1): base bet amount
            inc_red (int) (default=2): value for increasing or reducing the bet
        returns:
            None
        """
        super().__init__(bot_id, bankroll, min_bet)
        self.curr_bet = base_bet
        self.base_bet = base_bet
        self.inc_red = inc_red

    def betting(self) -> Optional[Bet]:
        """
        start with min_bet + 1, place a bet, after lose increase / reduce amount, after win come back to base bet

        returns:
            Bet or None (if pass)
        """
        if self.bankroll < self.min_bet:
            return None

        if not self.history:
            self.curr_bet = self.min_bet + 1
        else:
            last = self.history[-1]
            if last["win"]:
                self.curr_bet = self.base_bet
            else:
                self.curr_bet += self.inc_red

        if self.min_bet < self.curr_bet < self.bankroll:
            return Bet(amount=self.curr_bet, kind="color", value="red")
        else:
            if self.min_bet > self.curr_bet:
                return Bet(amount=self.min_bet, kind="color", value="red")
            else:
                return Bet(amount=self.bankroll, kind="color", value="red")
