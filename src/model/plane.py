from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.logger.logger import Logger


@dataclass
class Plane:
    __logger: Logger
    __a: float  # x
    __b: float  # y
    __c: float  # z
    __d: float  # Distance from origin
    __inliers: pd.DataFrame  # Inliers of the plane

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        """
        Constructor for the Plane class
        :param a:
        :param b:
        :param c:
        :param d:
        """
        self.logger = Logger.get_logger(__name__)

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.inliers = pd.DataFrame({
            "x": [],
            "y": [],
            "z": [],
        })

    @property
    def logger(self) -> Logger:
        return self.__logger

    @logger.setter
    def logger(self, logger: Logger) -> None:
        if not logger:
            raise TypeError("Logger cannot be empty")

        self.__logger = logger

    @property
    def a(self) -> float:
        return self.__a

    @a.setter
    def a(self, a: float) -> None:
        if a is None:
            raise TypeError("Cannot be None")
        self.__a = a

    @propertyz
    def b(self) -> float:
        return self.__b

    @b.setter
    def b(self, b: float) -> None:
        if b is None:
            raise TypeError("Cannot be None")
        self.__b = b

    @property
    def c(self) -> float:
        return self.__c

    @c.setter
    def c(self, c: float) -> None:
        if c is None:
            raise TypeError("Cannot be None")
        self.__c = c

    @property
    def d(self) -> float:
        return self.__d

    @d.setter
    def d(self, d: float) -> None:
        if d is None:
            raise TypeError("Cannot be None")

        self.__d = d

    @property
    def inliers(self) -> pd.DataFrame:
        return self.__inliers

    @inliers.setter
    def inliers(self, inliers: pd.DataFrame) -> None:
        if not isinstance(inliers, pd.DataFrame):
            raise TypeError("Inliers must be a pandas DataFrame")

        self.__inliers = inliers

    def add_point(self, point: np.array) -> None:
        """
        Adds a point to the inliers
        :param point:
        :return:
        """
        if point is None:
            raise TypeError("Point cannot be null")

        # FIXME: Points to dataframe is not being added correctly
        self.inliers.loc[len(self.inliers)] = point

    def z(self, x: float, y: float) -> float:
        """
        Calculates the z value of the plane
        :param x:
        :param y:
        :return:
        """
        return (-self.a * x - self.b * y - self.d) / self.c

    def z_distance(self, x: float, y: float, z: float) -> float:
        """
        Calculates the distance between the point and the plane
        :param x:
        :param y:
        :param z:
        :return:
        """
        if not x:
            raise TypeError("x cannot be null")

        if not y:
            raise TypeError("y cannot be null")

        if not z:
            raise TypeError("z cannot be null")

        plane_z = self.z(x, y)

        return z - plane_z

    def mean(self) -> float:
        """
        Calculates the mean of the inliers
        :return:
        """
        z = self.inliers.z.mean()
        return z

    def standard_deviation(self) -> float:
        mean = self.mean()
        z = self.inliers.z
        return np.sqrt(np.sum((z - mean) ** 2) / len(z))

    def __repr__(self):
        return f"{self.a:.4f}x + {self.b:.4f}y + {self.c:.4f}z + {self.d:.4f}=0"
