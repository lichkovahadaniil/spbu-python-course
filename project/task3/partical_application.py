from typing import Callable, Any


def curry_explicit(func: Callable, airty: int) -> Callable:
    """
    turns a function of several parameters into a function of a single parameter

    args:
        func (Callable): function for currying
        airty (int) : airty for currying
    returns:
        a function of a single parameter
    """

    def inner(*args: Any) -> Callable:
        if len(args) == airty:
            return func(*args)
        return lambda x: inner(*args, x)

    return inner


def uncurry_explicit(func: Callable, airty: int) -> Callable:
    """
    turns a function of a single parameter into a function of several parameters

    args:
        func (Callable): function for uncurrying
        airty (int) : airty for currying
    returns:
        a function of several parameters
    """

    def inner(*args: Any) -> Callable:
        if len(args) != airty:
            raise TypeError(f"Incorrect quantity of arguments :(")
        res = func
        for item in args:
            res = res(item)
        return res

    return inner
