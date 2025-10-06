from functools import reduce
from typing import Callable, Iterable, Generator, Any, Sequence


def generator(data: Iterable[Any]) -> Generator:
    """
    a generator, that lazy-sequentially outputs elements

    args:
        data (Iterable): any iterable object (list, range, generator...)
    returns:
        generator, that lazy-sequentially outputs elements
    """
    for i in data:
        yield i


def pipeline(source: Iterable[Any], *operations: Callable) -> Any:
    """
    a pipeline, that sequentially applies passed operations to the input sequence

    args:
        source (Iterable)": any iterable object (list, range, generator...)
        *operations (Callable): operations for the sequential execution (* convert to the tuple)
    returns:
        any value
        example:
            - map, filter returns lazy-iterator
            - reduce returns one finally value
    """
    result = source
    for oper in operations:
        result = oper(result)

    return result


def collect(gen: Iterable[Any], output_type: Callable = list) -> Sequence:
    """
    collects generator's result into a collection (list default)

    args:
        gen (Iterable): generator for processing
        output_type (Callable): the callable object, that create the sequence
    returns:
        collection
    """
    return output_type(gen)
