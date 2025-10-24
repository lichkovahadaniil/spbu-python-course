import abc
from typing import Optional, Any
from project.task4.bet import Bet
import random as r


class Bot(abc.ABC):
    """
    The basic bot, keeps the ID, bankroll, and betting history
    """

    def __init__(self, bot_id: str, bankroll: int, min_bet: int = 1) -> None:
        """
        constructor for bots

        args:
            bot_id (int): bot id
            bankroll (int): bankroll
            min_bet (int) (default=1): min bet
        """
        self.id = bot_id
        self.bankroll = bankroll
        self.min_bet = min_bet
        self.history: list[dict[str, Any]] = []

    def cond(self) -> dict[str, Any]:
        """
        show current condition

        returns:
            dict of id, bankroll, len of history
        """
        return {"id": self.id, "bankroll": self.bankroll, "history": self.history}

    @abc.abstractmethod
    def betting(self) -> Optional[Bet]:
        """
        place a bet

        returns:
            Bet or None (if pass)
        """
        raise NotImplementedError

    def record_result(
        self, bet: Optional[Bet], outcome: tuple[int, str], payout: int, win: bool
    ) -> None:
        """
        i recorded the result of the round in the bot's history and update the bankroll (the fee is already included in the Game)
        args:
            bet (Optional[bet.Bet]): bet
            outcome (tuple[int, str]): outcome of the game
            payout (int): payout
            win (bool): win true/false
        """
        self.history.append(
            {
                "bet": bet,
                "payout": payout,
                "win": win,
                "outcome": outcome,
                "bankroll-after": self.bankroll,
            }
        )


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
