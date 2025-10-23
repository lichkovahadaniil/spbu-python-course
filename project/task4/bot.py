import abc
from typing import Optional, Any
from project.task4.bet import Bet


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
