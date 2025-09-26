from __future__ import annotations
from typing import Union


class Vector:
    # constructor
    def __init__(self, vec: list[Union[int, float]]):
        """constructor
        save input value in the 'value'
        """
        self.value = vec

    def __len__(self) -> int:
        """len function

        returns:
            len of the vector-type Python object
        """
        return len(self.value)

    def sProduct(self, vec1: Vector) -> Union[int, float]:
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
        """the cos of the angle between this and the another vector

        args:
            vec1 (Vector): another vector for the angle calculation
        returns:
            float: the cos of the angle between this and the another vector
        """
        return self.sProduct(vec1) / (self.norm() * vec1.norm())

    def norm(self) -> float:
        """the norm (length) of this vector

        returns:
            float: the norm of this vector
        """
        return sum([x**2 for x in self.value]) ** 0.5
