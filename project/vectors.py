from __future__ import annotations
from typing import Sequence
import math


class Vector:
    # constructor
    def __init__(self, vec: Sequence[int | float]):
        """constructor

        save input value as a 'value' of vector
        """
        self.value = vec
        if len(self) == 0:
            raise ValueError("The incorrect value of the vector")

    def __len__(self) -> int:
        """length function

        returns:
            int: len of the vector-type Python object
        """
        return len(self.value)

    def sProduct(self, vec1: Vector) -> float:
        """scalar product

        args:
            vec1 (Vector): another vector for the product
        returns:
            int: scalar product of this and the another vector
        """

        if len(self) != len(vec1):
            raise ValueError("vectors must be the same size")

        return sum([self.value[i] * vec1.value[i] for i in range(len(self))])

    def angle(self, vec1: Vector) -> float:
        """the angle between this and the another vector

        args:
            vec1 (Vector): another vector for the angle calculation
        returns:
            float: the angle between this and the another vector
        """
        return math.acos(self.sProduct(vec1) / (self.norm() * vec1.norm()))

    def norm(self) -> float:
        """the norm (length) of this vector

        returns:
            float: the norm of this vector
        """
        return sum([x**2 for x in self.value]) ** 0.5

    def __getitem__(self, key: int) -> float:
        """The operator for get value from the vector by the index (key)

        args:
            key (int): key for value
        returns:
            float: value, which is in this vector by the key
        """
        return self.value[key]

    # addition
    def __add__(self, vec: Vector) -> Vector:
        """additional functionality for correct matrix addition work

        args:
            vec (Vector): another vector for the addition
        returns:
            Vector: result of addition
        """
        if len(self) != len(vec):
            raise ValueError("Dimension error")

        return Vector([self[i] + vec[i] for i in range(len(self))])

    def __str__(self) -> str:
        """The overload for the print function

        returns:
            str: The str-vector, not the address of the object
        """
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """The overload for the == or !=

        returns:
            bool: True if equal, else False
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return self.value == other.value
