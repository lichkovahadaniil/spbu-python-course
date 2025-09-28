from __future__ import annotations
from typing import Union
from project.vectors import Vector


class Matrix:
    def __init__(self, matrix: list[list[Union[int, float]]]):
        """constructor

        save input value as a 'value' of matrix
        """
        self.value = [Vector(matrix[i]) for i in range(len(matrix))]

        if not matrix or not matrix[0]:
            raise ValueError("The incorrect dimension of the matrix")

        for i in range(1, len(self)):
            if len(self[i]) != len(self[i - 1]):
                raise ValueError("The incorrect dimension of the matrix")

    def __getitem__(self, key: int) -> Vector:
        """The operator for get vector from the matrix by the index (key)

        args:
            key (int): key for vector
        returns:
            Vector: vector, which is in this matrix by the key
        """
        return self.value[key]

    def __len__(self) -> int:
        """length function

        returns:
            int: len of the matrix-type Python object
        """
        return len(self.value)

    def __add__(self, matrix: Matrix) -> Matrix:
        """Implementation of the matrix addition

        args:
            matrix (Matrix): another matrix for addition with this
        returns:
            Matrix: the result of adding two matrices
        """

        if len(matrix) != len(self) or len(self[0]) != len(matrix[0]):
            raise ValueError("Matrices must be the same dimension")

        return Matrix([matrix[i] + self[i] for i in range(len(self))])

    def __str__(self) -> str:
        """The overload for the print function

        returns:
            str: The str-matrix, not the address of the object
        """
        return "[" + "\n".join(str(vec) for vec in self.value) + "]"

    def transp(self) -> Matrix:
        """Matrix transposition

        returns:
            A matrix with columns replaced by rows
        """
        return Matrix(
            [
                Vector([self[i][j] for i in range(len(self))])
                for j in range(len(self[0]))
            ]
        )

    def mProduct(self, matrix: Matrix) -> Matrix:
        """The matrix multiplication

        args:
            matrix (Matrix): another matrix for multiplication with current
        returns:
            Matrix: the result of multiplying two matrices
        """
        if len(self[0]) != len(matrix):
            raise ValueError("Dimension error, must be n*k and k*m")

        return Matrix(
            [
                Vector(
                    [
                        sum([self[i][j] * matrix[j][k] for j in range(len(self[0]))])
                        for k in range(len(matrix[0]))
                    ]
                )
                for i in range(len(self))
            ]
        )  # i can write it "in one line", but.. it's sooooo unreadable

    def __eq__(self, other: Matrix) -> bool:
        """The overload for the == or !=

        returns:
            bool: True if equal, else False
        """
        return self.value == other.value
