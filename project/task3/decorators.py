from typing import Callable, Any


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
        curr = dict()

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
                + [
                    (make_cache(k), make_cache(kwargs[k]))
                    for k in sorted(kwargs.items())
                ]
            )  # tuple is caching (as opposed to list)

            print(keys)

            if keys not in save:
                res = func(*args, **kwargs)
                save[keys] = res
            else:
                res = save[keys]

            cnt = 0
            while len(save) > num:
                for key in save:
                    if cnt > 0:
                        curr[key] = save[key]
                    cnt += 1
                save = curr.copy()
                curr.clear()

            return res

        return inner

    return wrapper
