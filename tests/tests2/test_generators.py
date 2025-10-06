import pytest
from functools import reduce
from project.task2.generator import generator, pipeline, collect


@pytest.mark.parametrize(
    "data, operations, expect",
    [
        (
            generator([1, 2, 3, 4, 5, 6, 7]),
            lambda x: map(lambda y: y * 2, x),
            [2, 4, 6, 8, 10, 12, 14],
        ),
        (
            generator([1, 2, 3, 4, 5, 6, 7]),
            lambda x: filter(lambda v: v % 2 == 0, x),
            [2, 4, 6],
        ),
    ],
)
def test_built_in(data, operations, expect):
    res = collect(pipeline(data, operations))
    assert res == expect


@pytest.mark.parametrize(
    "data, operations, expect",
    [
        # map
        (generator([1, 2, 3]), [lambda x: map(lambda y: y * 2, x)], [2, 4, 6]),
        # filter
        (
            generator([1, 2, 3, 4, 5]),
            [lambda x: filter(lambda v: v % 2 == 0, x)],
            [2, 4],
        ),
        # reduce
        (
            generator([1, 2, 3, 4]),
            [
                lambda x: filter(lambda v: v > 2, x),
                lambda x: reduce(lambda a, b: a + b, x, 0),
            ],
            7,
        ),
    ],
)
def test_pipeline(data, operations, expect):
    result = pipeline(data, *operations)
    if isinstance(result, int):
        assert result == expect
    else:
        assert collect(result) == expect


@pytest.mark.parametrize(
    "data, func, expect",
    [(generator([1, 2, 3]), lambda g: (x * x for x in g), [1, 4, 9])],
)
def test_custom_function(data, func, expect):
    result = collect(pipeline(data, func))
    assert result == expect


@pytest.mark.parametrize(
    "data1, data2, operations, expect",
    [
        (
            generator([1, 2, 3]),
            [10, 20, 30],
            [
                lambda x: zip(x, [10, 20, 30]),
                lambda x: map(lambda pair: pair[0] + pair[1], x),
            ],
            [11, 22, 33],
        )
    ],
)
def test_zip_inside_pipeline(data1, data2, operations, expect):
    result = pipeline(data1, *operations)
    assert collect(result) == expect
