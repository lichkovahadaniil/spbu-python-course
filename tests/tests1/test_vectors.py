import pytest
from project.task1.vectors import Vector
import math


@pytest.mark.parametrize(
    "vec1, vec2, output", [([1, 2], [3, 4], 11), ([-1, 2.5], [3, -4], -13)]
)
def test_scalar_product(vec1, vec2, output):
    v1, v2 = Vector(vec1), Vector(vec2)
    assert v1 * v2 == output


@pytest.mark.parametrize(
    "vec1, vec2, output",
    [
        (
            [1, 2],
            [3, 4],
            math.acos(11 / ((1**2 + 2**2) * (3**2 + 4**2)) ** 0.5),
        ),
        (
            [-1, 2.5],
            [3, -4],
            math.acos(-13 / (((-1) ** 2 + 2.5**2) * (3**2 + (-4) ** 2)) ** 0.5),
        ),
    ],
)
def test_angle(vec1, vec2, output):
    v1, v2 = Vector(vec1), Vector(vec2)
    assert v1.angle(v2) == output


@pytest.mark.parametrize(
    "vec1, output",
    [([1, 2], (1**2 + 2**2) ** 0.5), ([-1, 2.5], ((-1) ** 2 + 2.5**2) ** 0.5)],
)
def test_norm(vec1, output):
    v1 = Vector(vec1)
    assert v1.norm() == output


@pytest.mark.parametrize(
    "vec1, vec2, output", [([1, 2], [3, 4], [4, 6]), ([-1, 2.5], [3, -4], [2, -1.5])]
)
def test_addition(vec1, vec2, output):
    v1, v2, v3 = Vector(vec1), Vector(vec2), Vector(output)
    assert v1 + v2 == v3


def test_add_dim():

    v1 = Vector([1, 2])
    v2 = Vector([1, 2, 3])
    with pytest.raises(ValueError, match="Dimension error"):
        v1 + v2


def test_empty_vector():

    with pytest.raises(ValueError, match="The incorrect value of the vector"):
        Vector([])
