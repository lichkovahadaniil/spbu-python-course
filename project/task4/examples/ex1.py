from project.task4.bot import MurderBot, RandomBot, FixBot
from project.task4.game import Game


def main():
    bots = [
        FixBot(
            "fixprice", bankroll=50, amount=5, fixed_kind="color", fixed_val="black"
        ),
        MurderBot("murder_bro", bankroll=50, base_bet=2, inc_red=2),
        RandomBot("ugaday_cho_vikinu", bankroll=50),
    ]
    game = Game(bots, min_bet=1, max_rounds=100, target_bankroll=77, seed=123)
    result = game.run(verbose=True)
    print("Game ended after", result["rounds_played"], "rounds")
    print("Winners:", result["winners"])


if __name__ == "__main__":
    main()
