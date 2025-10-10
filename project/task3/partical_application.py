from typing import Callable, Any


def curry_explicit(func: Callable, arity: int) -> Callable:
    """
    turns a function of several parameters into a function of a single parameter

    args:
        func (Callable): function for currying
        arity (int) : arity for currying
    returns:
        a function of a single parameter
    """
    if arity < 0:
        raise ValueError(f"The arity must be greater, than 0")

    def inner(*args: Any) -> Callable:
        if len(args) > arity:
            raise TypeError(
                f"Incorrect quantity of arguments :(\n got {len(args)}, expected {arity}\n"
            )
        if len(args) == arity:
            return func(*args)
        return lambda x: inner(*args, x)

    return inner


def uncurry_explicit(func: Callable, arity: int) -> Callable:
    """
    turns a function of a single parameter into a function of several parameters

    args:
        func (Callable): function for uncurrying
        arity (int) : arity for currying
    returns:
        a function of several parameters
    """
    if arity < 0:
        raise ValueError(f"The arity must be greater, than 0")

    def inner(*args: Any) -> Callable:
        if len(args) != arity:
            raise TypeError(
                f"Incorrect quantity of arguments :(\n got {len(args)}, expected {arity}\n"
            )
        res = func
        for item in args:
            res = res(item)
        return res

    return inner
