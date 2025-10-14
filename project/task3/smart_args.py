from typing import Callable, Any
import copy
from inspect import signature
import random


def smart_args(func: Callable) -> Callable:
    """
    The @smart_args decorator, which analyzes the default value types of function arguments and,
    depending on this, copies and/or calculates them before executing the function.

    - Evaluated(func_without_args) --- substitutes the default value calculated at the time of the call
    - Isolated() --- this is a dummy default value; the argument must be passed, but at the time of transmission it is copied (deep copy)

    args:
        func (Callable): function for wrapping
    returns:
        Calable
    """
    sg = signature(func)  # list of args and default values
    par = sg.parameters

    def wrapper(*args, **kwargs):
        assert len(args) == 0, "must be only kwargs"

        dct_args_iso = sg.bind_partial(*args)
        dct_args_iso.apply_defaults()
        dct_args_eva = sg.bind_partial(*args, **kwargs)
        dct_args_eva.apply_defaults()

        final_args = {}

        for key, value in dct_args_iso.arguments.items():
            if isinstance(value, Isolated):
                if key in kwargs:
                    final_args[key] = copy.deepcopy(kwargs[key])
                elif hasattr(value, "obj"):
                    final_args[key] = copy.deepcopy(value.obj)
                else:
                    final_args[key] = None
                continue

            if isinstance(value, Evaluated):
                if key in kwargs:
                    final_args[key] = kwargs[key]
                else:
                    final_args[key] = value.func()
                continue

            if key in kwargs:
                final_args[key] = kwargs[key]
            else:
                final_args[key] = value

        return func(**final_args)

    return wrapper


class Evaluated:
    """
    a class that specifies that you need to call the function passed to it without arguments and substitute the result
    """

    def __init__(self, func: Callable) -> None:
        """
        constructor for Evaluated

        args:
            func (Callable)
        returns:
            None
        """
        if isinstance(func, Evaluated):
            raise KeyError("no need to combine Isolated and Evaluated")
        self.func = func


class Isolated:
    """
    a class for specifying that the argument should be changed to a deepcopy of the argument
    """

    def __init__(self, obj=None) -> None:
        """
        constructor for Isolated

        args:
            obj (Callable)
        returns:
            None
        """
        if isinstance(obj, Evaluated):
            raise KeyError("no need to combine Isolated and Evaluated")
        self.obj = obj
