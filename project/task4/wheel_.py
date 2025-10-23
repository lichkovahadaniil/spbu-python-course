from typing import Union
import random as r


class Wheel:
    """
    roulette reel — provides the spin() method, which returns the winning number and color
    european roulette: pockets 0..36, 0 — green, the rest have colors according to the standard.
    """

    def __init__(self, seed: Union[int, None] = None) -> None:
        """
        constructor for wheel

        args:
            seed (int | None): seed for random
        """
        if seed is not None:
            r.seed(seed)

        # base red set
        self.red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.nums = list(range(37))

    def spin(self) -> tuple[int, str]:
        """
        spin control

        args:

        returns:
            num (int): output num
            color (str): output color
        """
        num = r.choice(self.nums)
        color = "green"
        if num in self.red:
            color = "red"
        elif num != 0:
            color = "black"
        return num, color
