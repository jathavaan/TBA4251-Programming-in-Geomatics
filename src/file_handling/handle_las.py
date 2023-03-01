from dataclasses import dataclass

import laspy
import numpy as np
import pandas as pd
from laspy import LasData
import open3d as o3d

from src.file_handling.file_handler import FileHandler
from src.logger.logger import Logger


@dataclass
class HandleLAS(FileHandler):
    __file: LasData
    __points: pd.DataFrame

    def __init__(self, file_path: str) -> None:
        if not file_path.endswith(".las"):
            raise TypeError("File must be a .las file")

        super().__init__(file_path=file_path, logger=Logger.get_logger(__name__))
        self._open()

    @property
    def file(self) -> LasData:
        return self.__file

    @file.setter
    def file(self, file: LasData) -> None:
        if not LasData:
            raise TypeError("File must be a LasData object")

        self.__file = file

    @property
    def points(self) -> pd.DataFrame:
        return self.__points

    @points.setter
    def points(self, points: pd.DataFrame) -> None:
        if not isinstance(points, pd.DataFrame):
            raise TypeError("Points must be a pandas DataFrame")

        if points.empty:
            raise ValueError("Points cannot be empty")

        self.__points = points

    def _open(self) -> None:
        with laspy.open(self.file_path) as lf:
            las = lf.read()  # Reading the LAS file and storing as LasData object
            self.file = las

        self.logger.info(f"Reading {self.file_path}")
        self.logger.info(f"Dimension names: {', '.join(self.file.point_format.dimension_names)}")
        self.logger.info(f"No. of points in LAS file: {len(self.file.points)}")

        x, y, z = self.file["X"], self.file["Y"], self.file["Z"]  # Extracting the X, Y and Z coordinates
        self.points = pd.DataFrame(np.array([x, y, z]).T)  # Storing the coordinates in a pandas DataFrame
        self.logger.info("Created Pandas DataFrame with X, Y and Z coordinates")

    def display_point_cloud(self) -> None:
        point_cloud = o3d.geometry.PointCloud()  # Creating an empty point cloud
        point_cloud.points = o3d.utility.Vector3dVector(self.points.to_numpy())  # Adding the points to the point cloud
        self.logger.info("Displaying point cloud...")
        o3d.visualization.draw_geometries([point_cloud])  # Displaying the point cloud
        self.logger.info("Point cloud displayed")
