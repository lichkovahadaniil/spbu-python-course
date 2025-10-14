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

    def wrapper(*args, **kwargs) -> Callable:
        """
        wrapper

        important:
            - only default values for isolated
            - default and **kwargs for evaluated
        """
        assert len(args) == 0, "must be only kwargs"

        dct_args_iso = sg.bind_partial(*args)
        dct_args_iso.apply_defaults()

        dct_args_eva = sg.bind_partial(*args, **kwargs)
        dct_args_eva.apply_defaults()

        flag_iso, flag_eva = False, False
        isolated_keys = set()

        for key, value in dct_args_iso.arguments.items():
            if isinstance(value, Isolated):
                if key in kwargs:
                    dct_args_iso.arguments[key] = copy.deepcopy(kwargs[key])
                isolated_keys.add(key)
                flag_iso = True
            if isinstance(value, Evaluated):
                flag_eva = True

        for key, value in dct_args_eva.arguments.items():
            if isinstance(value, Evaluated):
                if key not in kwargs:
                    dct_args_eva.arguments[key] = value.func()
                flag_eva = True

        if flag_eva:
            return func(**dct_args_eva.arguments)
        else:
            final_args = dict(dct_args_iso.arguments)
            for k, v in kwargs.items():
                if k not in isolated_keys:
                    final_args[k] = v
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
