import pytest
from typing import Optional
from project.task4.bet import Bet
from project.task4.bot import Bot, FixBot, MurderBot, RandomBot
from project.task4.wheel_ import Wheel
from project.task4.game import Game


class TestWheel:
    def test_spin_green(self):
        wheel = Wheel(seed=52)
        for _ in range(100):
            num, color = wheel.spin()
            if num == 0:
                assert color == "green"
                return
        pytest.fail("Did not get green in 100 spins, adjust seed")


class TestBetResolution:
    @pytest.fixture
    def game_fixture(self):
        return Game(bots=[], seed=3847)

    def test_resolve_number_win(self, game_fixture):
        bet = Bet(10, "number", 26)
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is True

    def test_resolve_number_loss(self, game_fixture):
        bet = Bet(10, "number", 25)
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is False

    def test_resolve_color_win(self, game_fixture):
        bet = Bet(10, "color", "black")
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is True

    def test_resolve_color_loss(self, game_fixture):
        bet = Bet(10, "color", "red")
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is False

    def test_resolve_color_green_loss(self, game_fixture):
        bet = Bet(10, "color", "black")
        outcome = (0, "green")
        assert game_fixture.resolve_bet(bet, outcome) is False

    def test_resolve_parity_win_even(self, game_fixture):
        bet = Bet(10, "parity", "even")
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is True

    def test_resolve_parity_loss_odd(self, game_fixture):
        bet = Bet(10, "parity", "odd")
        outcome = (26, "black")
        assert game_fixture.resolve_bet(bet, outcome) is False


class TestFixBot:
    def test_betting_enough_bankroll(self):
        bot = FixBot(
            "fix", 50, amount=5, fixed_kind="color", fixed_val="black", min_bet=1
        )
        bet = bot.betting()
        assert bet is not None
        assert bet.amount == 5
        assert bet.kind == "color"
        assert bet.value == "black"

    def test_betting_low_bankroll(self):
        bot = FixBot("fix", 3, amount=5, min_bet=1)
        bet = bot.betting()
        assert bet is None  # Since 3 < 5

    def test_record_result(self):
        bot = FixBot("fix", 50, amount=5)
        bet = Bet(5, "color", "black")
        bot.record_result(bet, (26, "black"), 5, True)
        assert len(bot.history) == 1
        assert bot.history[0]["win"] is True
        assert bot.history[0]["payout"] == 5


class TestMurderBot:
    def test_initial_bet(self):
        bot = MurderBot("murder", 50, min_bet=1, base_bet=2, inc_red=2)
        bet = bot.betting()
        assert bet is not None
        assert bet.amount == 2
        assert bet.kind == "color"
        assert bet.value == "red"

    def test_after_loss_increase(self):
        bot = MurderBot("murder", 50, base_bet=2, inc_red=2)
        bot.betting()
        bot.record_result(Bet(2, "color", "red"), (26, "black"), -2, False)
        bet = bot.betting()
        assert bet.amount == 4

    def test_after_win_reset(self):
        bot = MurderBot("murder", 50, base_bet=2, inc_red=2)
        bot.betting()
        bot.record_result(Bet(2, "color", "red"), (21, "red"), 2, True)
        bet = bot.betting()
        assert bet.amount == 2

    def test_low_bankroll(self):
        bot = MurderBot("murder", 1, min_bet=2, base_bet=2, inc_red=2)
        bet = bot.betting()
        assert bet is None


class TestRandomBot:
    def test_betting_rand_bot(self):
        bot = RandomBot("rand", 50, min_bet=1)
        bet = bot.betting()
        assert bet is not None
        assert 1 <= bet.amount <= 50
        assert bet.kind in ["color", "number", "parity"]

    def test_low_bankroll(self):
        bot = RandomBot("rand", 0, min_bet=1)
        bet = bot.betting()
        assert bet is None


class TestGame:
    @pytest.fixture
    def bots_fixture(self):
        return [
            FixBot("fix", bankroll=50, amount=5, fixed_kind="color", fixed_val="black"),
            MurderBot("murder", bankroll=50, base_bet=2, inc_red=2),
            RandomBot("rand", bankroll=50),
        ]

    @pytest.fixture
    def game_with_bots(self, bots_fixture):
        return Game(
            bots_fixture, min_bet=1, max_rounds=10, target_bankroll=100, seed=3847
        )

    def test_state_initial(self, game_with_bots):
        state = game_with_bots.state()
        assert state["round"] == 0
        assert len(state["bot_states"]) == 3
        assert state["bot_states"][0]["bankroll"] == 50
        assert state["history_len"] == 0

    def test_step_changes_state(self, game_with_bots):
        initial_state = game_with_bots.state()
        game_with_bots.step()
        new_state = game_with_bots.state()
        assert new_state["round"] == 1
        assert (
            new_state["bot_states"][0]["bankroll"]
            != initial_state["bot_states"][0]["bankroll"]
        )
        assert new_state["history_len"] == 1

    def test_step_updates_bankrolls(self, game_with_bots, bots_fixture):
        game_with_bots.step()
        assert bots_fixture[0].bankroll == 55
        assert bots_fixture[1].bankroll == 48
        assert len(bots_fixture[0].history) == 1
        assert bots_fixture[0].history[0]["win"] is True
        assert bots_fixture[1].history[0]["win"] is False

    def test_run_until_max_rounds(self, game_with_bots):
        result = game_with_bots.run()
        assert result["rounds_played"] == 10
        assert len(result["history"]) == 10
        assert result["winners"] == []

    def test_run_with_target_reached(self, bots_fixture):
        game = Game(
            bots_fixture, min_bet=1, max_rounds=100, target_bankroll=55, seed=3847
        )
        result = game.run()
        assert result["rounds_played"] < 100
        assert "fix" in result["winners"]

    def test_all_broke_stops(self):
        broke_bots = [
            FixBot("fix", bankroll=0, amount=5),
            MurderBot("murder", bankroll=0, base_bet=2, inc_red=2),
            RandomBot("rand", bankroll=0),
        ]
        game = Game(broke_bots, min_bet=1, max_rounds=10)
        result = game.run()
        assert result["rounds_played"] == 0

    def test_payout_number_win(self):
        class CustomBot(Bot):
            def betting(self) -> Optional[Bet]:
                return Bet(10, "number", 26)

        custom = CustomBot("custom", 50, min_bet=1)
        game = Game([custom], seed=3847)
        game.step()
        assert custom.bankroll == 400
        assert custom.history[0]["payout"] == 350
        assert custom.history[0]["win"] is True

    def test_history_records(self, game_with_bots):
        game_with_bots.step()
        assert len(game_with_bots.history) == 1
        record = game_with_bots.history[0]
        assert record["round"] == 1
        assert record["outcome"] == (29, "black")
        assert len(record["bets"]) == 3
