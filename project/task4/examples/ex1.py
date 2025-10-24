import sys
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

    with open("project/task4/examples/example1.txt", "w") as f:

        class Tee(object):
            def __init__(self, original, file):
                self.original = original
                self.file = file

            def write(self, s):
                self.original.write(s)
                self.file.write(s)

            def flush(self):
                self.original.flush()
                self.file.flush()

        original_stdout = sys.stdout
        sys.stdout = Tee(original_stdout, f)

        try:
            result = game.run(verbose=True)
            print("Game ended after", result["rounds_played"], "rounds")
            print("Winners:", result["winners"])
        finally:
            sys.stdout = original_stdout


if __name__ == "__main__":
    main()
