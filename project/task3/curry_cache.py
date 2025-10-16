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

    curr: dict[int, tuple[Any, ...]] = dict()

    def inner(*args: Any) -> Callable:
        nonlocal curr
        if len(curr) == 0:
            if len(args) > 1:
                raise TypeError(
                    f"Incorrect quantity of arguments :(\n got {len(args)}, expected {arity}\n"
                )
        else:
            if len(curr[0]) > 1:
                raise TypeError("Incorrect quantity of arguments")

        if len(args) > arity:
            raise TypeError(
                f"Incorrect quantity of arguments :(\n got {len(args)}, expected {arity}\n"
            )
        elif len(args) == arity:
            return func(*args)

        def next_call(*new_arg):
            curr[0] = new_arg
            return inner(*args, *new_arg)

        return next_call

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


def deco_cache(num: int = 0) -> Callable:
    """
    the decorator for caching of function executing result
    (saving calculation results for a different set of function arguments)

    args:
        func (Callable): function for memoization
        num (int): quantity of the saving results
    returns:
        a decorator that adds caching to a function.
    """

    def wrapper(func: Callable) -> Callable:
        save = dict()

        def make_cache(arg):
            if isinstance(arg, dict):
                return tuple(sorted((key, make_cache(val)) for key, val in arg.items()))
            if isinstance(arg, (list, set)):
                return tuple(make_cache(val) for val in arg)
            return arg

        def inner(*args, **kwargs) -> Any:

            if num == 0:
                return func(*args, **kwargs)

            nonlocal save
            keys = tuple(
                [make_cache(a) for a in args]
                + [(make_cache(k), make_cache(v)) for k, v in sorted(kwargs.items())]
            )  # tuple is caching (as opposed to list)

            if keys not in save:
                res = func(*args, **kwargs)
                save[keys] = res
            else:
                res = save[keys]

            if len(save) > num:
                oldest_key = next(iter(save))
                del save[oldest_key]

            return res

        return inner

    return wrapper
