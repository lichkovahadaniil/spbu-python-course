import pytest
from project.vectors import Vector
from project.matrices import Matrix
import math


@pytest.mark.parametrize(
    "mt1, mt2, output",
    [
        ([[1, 2], [3, 4]], [[3, 4], [5, 6]], [[4, 6], [8, 10]]),
        ([[1, 2, 3], [4, 5, 6]], [[3, 4, 5], [5, 6, 7]], [[4, 6, 8], [9, 11, 13]]),
    ],
)
def test_addition(mt1, mt2, output):
    m1, m2, m3 = Matrix(mt1), Matrix(mt2), Matrix(output)
    result = m1 + m2

    for i in range(len(result)):
        for j in range(len(result[0])):
            assert result[i][j] == m3[i][j]


@pytest.mark.parametrize(
    "mt1, mt2, output",
    [
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]], [[58, 64], [139, 154]]),
        ([[2, 0], [0, 2]], [[3, 1], [1, 3]], [[6, 2], [2, 6]]),
    ],
)
def test_multi(mt1, mt2, output):
    m1, m2, m3 = Matrix(mt1), Matrix(mt2), Matrix(output)
    result = m1 * m2

    for i in range(len(result)):
        for j in range(len(result[0])):
            assert result[i][j] == m3[i][j]


@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
        ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
        ([[1], [2], [3]], [[1, 2, 3]]),
        ([[1, 2, 3]], [[1], [2], [3]]),
    ],
)
def test_transp(matrix, expected):
    m1 = Matrix(matrix)
    m2 = Matrix(expected)
    result = m1.transp()

    for i in range(len(result)):
        for j in range(len(result[0])):
            assert result[i][j] == m2[i][j]


def test_multi_dim():

    m1 = Matrix([[1, 2], [3, 4]])  # 2x2
    m2 = Matrix([[1, 2, 3]])  # 1x3
    with pytest.raises(ValueError, match="Dimension error"):
        m1 * m2


def test_add_dim():

    m1 = Matrix([[1, 2], [3, 4]])  # 2x2
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])  # 2x3
    with pytest.raises(ValueError, match="Matrices must be the same dimension"):
        m1 + m2


def test_empty_matrix():

    with pytest.raises(ValueError, match="The incorrect dimension of the matrix"):
        Matrix([])


def test_irregular_matrix():

    with pytest.raises(ValueError, match="The incorrect dimension of the matrix"):
        Matrix([[1, 2], [3, 4, 5]])
