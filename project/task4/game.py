from typing import cast, Any, Optional
import random as r
from project.task4.bot import Bot
from project.task4.wheel_ import Wheel, Color
from project.task4.bet import Bet, ForBet


class Game:
    """
    game maker, storage thebot list, wheel, current condition
    End parameters:
        - or target_bankroll: as soon as someone has reached the target -> the game stops (victory)
        - or max_rounds: when reached, we stop
    """

    def __init__(
        self,
        bots: list[Bot],
        min_bet: int = 1,
        max_rounds: int = 777,
        target_bankroll: Optional[int] = None,
        seed: Optional[int] = None,
    ):
        self.wheel = Wheel(seed=seed)
        self.bots = bots
        self.round = 0
        self.min_bet = min_bet
        self.max_rounds = max_rounds
        self.target_bankroll = target_bankroll
        self.history: list[dict[str, Any]] = []
        if seed is not None:
            r.seed(seed)

    def state(self) -> dict[str, Any]:
        """
        function for game condition

        returns (dict[str, Any]): current game condition"""
        return {
            "round": self.round,
            "bot_states": [b.cond() for b in self.bots],
            "history_len": len(self.history),
        }

    def resolve_bet(self, bet: Bet, outcome: tuple[int, str]) -> bool:
        """
        We will transfer the payout already taking into account the bet: for example, for the number the bet is 1 and the win is 35:1,
        the total profit = 35 (i.e. the bet is returned + 35).
        In the implementation below: return (net_change), where if you lose - bet.amount, if you win +win_amount.

        args:
            bet (Bet): a bet
            outcome (tuple[int, str]): amount, win/lose

        returns (payout, won_flag): payout for bot, win/loose
        """
        number, color = outcome
        if bet.kind == ForBet.NUMBER.value:
            if bet.value == number:
                return True

        elif bet.kind == Color.COLOR.value:
            if number != 0 and bet.value == color:
                return True

        elif bet.kind == ForBet.PARITY.value:
            if number == 0:
                return False
            parity = ForBet.EVEN.value if number % 2 == 0 else ForBet.ODD.value
            if parity == bet.value:
                return True

        return False

    def step(self) -> dict[str, Any]:
        """
        function for one round (step), where:

        - each bot makes a bet (betting)
        - deduct the bet from the bankroll (temporarily)
        - spin the wheel
        - calculate the payout for each bet and update the bankroll
        - update strategies (for example, MartingaleBot.inform_round)
        - save the round in history and increase self.round
                We return the dictionary with the result of the round.

        returns:
            dictionary with round's result
        """
        self.round += 1
        round_record = {"round": self.round, "bets": [], "outcome": None}

        bets_list = cast(list[dict[str, Any]], round_record["bets"])

        bets: dict[Bot, Optional[Bet]] = {}
        for b in self.bots:
            bet = b.betting()

            if bet is not None:

                if bet.amount < self.min_bet:
                    bet.amount = self.min_bet
                if bet.amount > b.bankroll:
                    bet.amount = b.bankroll

                b.bankroll -= bet.amount
            bets[b] = bet
            bets_list.append({"bot_id": b.id, "bet": bet})

        outcome = self.wheel.spin()
        round_record["outcome"] = outcome

        for b, bet in bets.items():
            payout = 0
            won = False
            if bet is None:
                pass
            else:
                won = self.resolve_bet(bet, outcome)
                if won:
                    if bet.kind == ForBet.NUMBER.value:
                        win_profit = bet.amount * 35
                        b.bankroll += bet.amount + win_profit
                        payout = win_profit  # net profit over bet
                    else:
                        win_profit = bet.amount
                        b.bankroll += bet.amount + win_profit
                        payout = win_profit
                else:
                    payout = -bet.amount

            b.record_result(bet, outcome, payout, won)

        self.history.append(round_record)
        return round_record

    def run(self, verbose: bool = False) -> dict[str, Any]:
        """
        for run game

        returns:
            finally list and winners (if there are any)
        """
        winners = []
        while True:
            if self.round >= self.max_rounds:
                break
            if all(b.bankroll < self.min_bet for b in self.bots):
                break

            round_res = self.step()
            if verbose:
                self.print_round(round_res)

            if self.target_bankroll is not None:
                for b in self.bots:
                    if b.bankroll >= self.target_bankroll:
                        winners.append(b)
                if winners:
                    break
        return {
            "rounds_played": self.round,
            "history": self.history,
            "winners": [b.id for b in winners] if winners else [],
        }

    def print_round(self, round_res: dict[str, Any]):
        num, color = round_res["outcome"]
        print(f"Round {round_res['round']}: outcome = {num} ({color})")
        for b in self.bots:
            last = b.history[-1]
            bet = last["bet"]
            if bet is None:
                print(f"  {b.id}: passed, bankroll={b.bankroll}")
            else:
                won = last["win"]
                print(
                    f"  {b.id}: bet({bet.kind}={bet.value}, {bet.amount}) -> {'WIN' if won else 'LOSE'}, bankroll={b.bankroll}"
                )
        print("-" * 40)
