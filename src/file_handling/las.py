import math
from dataclasses import dataclass

import laspy
import numpy as np
import open3d as o3d
import pandas as pd

from config import Config
from src.file_handling.file_handler import FileHandler
from src.logger.logger import Logger
from src.model.plane import Plane


@dataclass
class LAS(FileHandler):
    __point_cloud: o3d.geometry.PointCloud
    __parent_las: 'LAS'
    __segmented_LAS: list['LAS']
    __plane: Plane
    __flagged: bool

    def __init__(
            self,
            file_path: str = None,
            point_cloud: o3d.geometry.PointCloud = None,
            parent: 'LAS' = None
    ) -> None:
        """
        Initializes the LAS object. If path is not None a new parent LAS object is created,
        otherwise a child object is created
        :param file_path:
        :param point_cloud:
        """
        # TODO: Check why filename is defined all the time

        if file_path is not None and point_cloud is not None:
            raise TypeError("File path and point cloud cannot both be set at initialization")

        if file_path is not None:
            if not file_path.endswith(".las"):
                raise TypeError("File must be a .las file")

            self.parent_las = None  # Setting parent LAS to None as default
            super().__init__(file_path=file_path, logger=Logger.get_logger(__name__))
        elif point_cloud is not None:
            super().__init__(file_path=None, logger=Logger.get_logger(__name__))

        if parent is not None:
            self.parent_las = parent

        if self.__is_parent():
            self.logger.info("Creating parent LAS object")
            self._open()  # Opening file and setting point cloud
            self.segmented_LAS = [pc for pc in self.__segment_point_cloud(self.point_cloud)]  # Segments the point cloud
            self.flag_LAS()  # Flags the LAS object if the difference between plane and point cloud is too large
        else:
            if parent is None:
                raise TypeError("Parent cannot be None")

            if not isinstance(parent, LAS):
                raise TypeError("Parent must be a LAS object")

            self.logger.info("Creating child LAS object")
            self.point_cloud = point_cloud
            self.segmented_LAS = []

        self.plane = self.__generate_plane(self.point_cloud)
        self.flagged = False  # Sets flagged to False by default
        self.logger.info("Iteration complete\n")

    @property
    def point_cloud(self) -> o3d.geometry.PointCloud:
        """
        Returns the point cloud
        :return:
        """
        return self.__point_cloud

    @point_cloud.setter
    def point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> None:
        """
        Sets the point cloud
        :param point_cloud:
        :return:
        """
        if point_cloud is None:
            raise TypeError("Point cloud cannot be None")

        if not isinstance(point_cloud, o3d.geometry.PointCloud):
            raise TypeError("Point cloud must be an open3d.geometry.PointCloud object")

        # TODO: Add point cloud manipulation here
        # TODO: Check if it is necessary to run a voxel downsize here

        self.__point_cloud = point_cloud
        self.logger.info("Point cloud set")

    @property
    def parent_las(self) -> 'LAS':
        """
        Returns the parent LAS object
        :return:
        """
        return self.__parent_las

    @parent_las.setter
    def parent_las(self, parent_las: 'LAS') -> None:
        """
        Sets the parent LAS object
        :param parent_las:
        :return:
        """
        if not isinstance(parent_las, LAS) and parent_las is not None:
            raise TypeError("Parent LAS must be a LAS object")

        self.__parent_las = parent_las

    @property
    def plane(self) -> Plane:
        """
        Returns the plane
        :return:
        """
        return self.__plane

    @plane.setter
    def plane(self, plane: Plane) -> None:
        """
        Sets the plane
        :param plane:
        :return:
        """
        if plane is None:
            raise TypeError("Plane cannot be None")

        if not isinstance(plane, Plane):
            raise TypeError("Plane must be a Plane object")

        self.__plane = plane

    @property
    def segmented_LAS(self) -> list['LAS']:
        """
        Returns the segmented point clouds
        :return:
        """
        return self.__segmented_LAS

    @segmented_LAS.setter
    def segmented_LAS(self, segmented_LAS: list['LAS']) -> None:
        """
        Sets the segmented point clouds
        :param segmented_LAS:
        :return:
        """
        if segmented_LAS is None:
            raise TypeError("Segmented point clouds cannot be None")

        if not isinstance(segmented_LAS, list):
            raise TypeError("Segmented point clouds must be a list")

        self.__segmented_LAS = segmented_LAS
        self.logger.info("Segmented point clouds updated")

    @property
    def flagged(self) -> bool:
        return self.__flagged

    @flagged.setter
    def flagged(self, flagged: bool) -> None:
        self.__flagged = flagged

    def add_plane(self, plane: Plane) -> None:
        """
        Adds a plane to the list of planes
        :param plane:
        :return:
        """
        if plane is None:
            raise TypeError("Plane cannot be None")

        if not isinstance(plane, Plane):
            raise TypeError("Plane must be a Plane object")

        if plane not in self.planes:
            self.planes.append(plane)
            self.logger.info(f"{plane} added")

    def filter(self, filter_type: str) -> list['LAS']:
        """
        Filters the point clouds based on the type
        :param filter_type: The type of filter to apply; either 'mean', 'sd' or 'se'
        :return:
        """
        if filter_type is None:
            raise TypeError("Type cannot be None")

        if not isinstance(filter_type, str):
            raise TypeError("Type must be a string")

        if filter_type not in ["mean", "sd", "se"]:
            raise ValueError("Type must be either 'mean', 'sd' or 'se'")

        filter_type = filter_type.lower()
        match filter_type:
            case "mean":
                lower_bound, upper_bound = Config.MEAN_THRESHOLD.value
                return list(filter(lambda las: lower_bound < las.plane.mean < upper_bound, self.segmented_LAS))
            case "sd":
                lower_bound, upper_bound = Config.SD_THRESHOLD.value
                return list(filter(lambda las: lower_bound < las.plane.SD < upper_bound, self.segmented_LAS))
            case "se":
                lower_bound, upper_bound = Config.SE_THRESHOLD.value
                return list(filter(lambda las: lower_bound < las.plane.SE < upper_bound, self.segmented_LAS))

    def merge_segmented_pc(self, *LAS_objects) -> o3d.geometry.PointCloud:
        merged_las_df = pd.concat(
            [
                self.__pc_to_df(s_LAS.plane.point_cloud) for s_LAS in self.segmented_LAS
                if Config.SD_THRESHOLD.value[0] < self.SD(s_LAS.point_cloud) < Config.SD_THRESHOLD.value[1]
            ] if len(LAS_objects) == 0 else [
                self.__pc_to_df(s_LAS.plane.point_cloud) for s_LAS in LAS_objects
            ]
        )

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(merged_las_df.to_numpy())
        return point_cloud

    def flag_LAS(self) -> None:
        las_list = self.segmented_LAS

        for las in las_list:
            inliers_df = las.plane.inliers
            x_real = np.array(inliers_df.x)
            y_real = np.array(inliers_df.y)
            z_real = np.array(inliers_df.z)

            z_plane = np.array([
                las.plane.z(x, y) for x, y in zip(x_real, y_real)
            ])

            diff = np.abs(z_real - z_plane)  # Difference in z-value between the plane and the point cloud
            SD = np.std(diff)

            if SD > Config.SD_THRESHOLD.value[0]:
                las.flagged = True  # Flagging if difference SD is larger than threshold
                self.logger.info(f"FLAGGED PLANE: {las.plane}")

    def display(self, *point_clouds: o3d.geometry.PointCloud) -> None:
        """
        Displays the point cloud in a 3D viewer
        :return:
        """
        if not point_clouds:
            point_clouds = None

        self.logger.info("Displaying point cloud...")
        self.logger.info(f"Point cloud has {len(self.point_cloud.points)} points")

        o3d.visualization.draw_geometries(
            [self.point_cloud] if point_clouds is None else [pc for pc in point_clouds],  # Point cloud to display
            point_show_normal=Config.SHOW_NORMAL_VECTORS.value,
        )  # Displaying the point cloud

        self.logger.info("Point cloud displayed")

    def _open(self) -> None:
        """
        Opens the LAS file and sets the point cloud
        :return:
        """
        with laspy.open(self.file_path) as lf:
            las = lf.read()

        self.logger.info(f"Reading {self.file_path}")
        self.logger.debug(f"Dimension names: {', '.join(las.point_format.dimension_names)}")

        print()

        x, y, z = las.X, las.Y, las.Z  # Get the X, Y, Z coordinates
        points = pd.DataFrame(data=np.array([x, y, z]).T, columns=["x", "y", "z"])  # Storing coordinates in a DataFrame
        point_cloud = self.__df_to_pc(points)  # Converting the DataFrame to a PointCloud object
        self.point_cloud = point_cloud  # Setting the point cloud

    @property
    def mean(self, point_cloud: o3d.geometry.PointCloud) -> float:
        """
        Calculates the mean of the inliers
        :return:
        """
        return self.__pc_to_df(point_cloud).z.mean()

    def VAR(self, point_cloud: o3d.geometry.PointCloud) -> float:
        return self.__pc_to_df(point_cloud).z.var()

    def SD(self, point_cloud: o3d.geometry.PointCloud) -> float:
        return self.__pc_to_df(point_cloud).z.std()

    def SE(self, point_cloud: o3d.geometry.PointCloud) -> float:
        return self.SD(point_cloud) / np.sqrt(self.__pc_to_df(point_cloud).size)

    def __is_parent(self) -> bool:
        """
        Checks if the LAS object is a parent
        :return:
        """
        return self.parent_las is None

    def __voxel_downsample(self, point_cloud: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Downsamples the point cloud using a voxel grid
        :param point_cloud:
        :return:
        """
        self.logger.info(f"Downsampling point cloud with voxel size: {Config.VOXEL_SIZE.value}")
        point_cloud = point_cloud.voxel_down_sample(
            voxel_size=Config.VOXEL_SIZE.value
        )  # Downsampling the point cloud
        self.logger.info(f"Point cloud downsampled to {len(point_cloud.points)} points")
        return point_cloud

    def __generate_plane(self, point_cloud: o3d.geometry.PointCloud) -> Plane:
        if self.__is_parent():
            pass
            # point_cloud = self.__voxel_downsample(point_cloud)  # Downsampling the point cloud if self is parent

        self.logger.info("Generating plane...")
        plane_model, inlier_indexes = point_cloud.segment_plane(
            distance_threshold=Config.DISTANCE_THRESHOLD.value,
            ransac_n=Config.RANSAC_N.value,
            num_iterations=Config.NUM_ITERATIONS.value,
        )  # Generating plane model

        a, b, c, d = plane_model  # Extracting the plane model parameters
        plane = Plane(a, b, c, d)  # Creating a Plane object

        inlier_points_df = self.__pc_to_df(point_cloud).iloc[inlier_indexes]  # Converting the pc to df
        plane.inliers = inlier_points_df  # Setting the inliers

        self.logger.debug(f"Generated plane: {plane} with {len(plane.inliers)} inliers")
        return plane

    def __segment_point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> list['LAS']:
        """
        Segments the point cloud into smaller point clouds
        :param point_cloud:
        :return:
        """
        self.logger.info("Segmenting point cloud into smaller frames...")
        pc_df = self.__pc_to_df(point_cloud)  # Converting the point cloud to a DataFrame
        origin = pc_df.iloc[0]  # Getting the origin point
        Logger.get_logger(__name__).debug(f"Origin {origin.x, origin.y, origin.z}")
        pc_df -= origin  # Adjusting the DataFrame by subtracting the origin
        Logger.get_logger(__name__).debug(f"Translated origin to (0, 0, 0)")

        segment_count = math.floor(
            Config.SPLIT_SCALE_FACTOR.value * pc_df.size  # TODO: Setup a new formula for this
        )  # No. of rows per split

        self.logger.info(f"No. of rows per split: {segment_count}")

        segmented_point_clouds = []

        for i in range(segment_count):
            start = i * segment_count
            end = (i + 1) * segment_count

            if start > len(point_cloud.points):
                break  # Break if start is greater than the no. of points

            if end > len(point_cloud.points):
                end = len(point_cloud.points)  # Set end to the no. of points if end is greater than the no. of points

            self.logger.debug(f"Splitting points from {start} to {end}")

            df = pd.DataFrame(np.asarray(point_cloud.points), columns=["x", "y", "z"])

            df = pd.DataFrame(np.asarray(point_cloud.points)[start:end], columns=["x", "y", "z"])
            segmented_point_cloud = self.__df_to_pc(df)
            segmented_las_obj = LAS(point_cloud=segmented_point_cloud, parent=self)
            segmented_point_clouds.append(segmented_las_obj)

        return segmented_point_clouds

    def __df_to_pc(self, points: pd.DataFrame) -> o3d.geometry.PointCloud:
        """
        Converts a pandas DataFrame to an open3d.geometry.PointCloud object
        :return:
        """
        self.logger.debug("Converting DataFrame to PointCloud object...")
        if points.empty:
            self.logger.warning("Points are empty")

            if self.__is_parent():
                exit(-1)  # Exits program if parent point cloud is empty

        self.logger.debug(f"No. of points in DataFrame: {len(points)}")

        origin = points.iloc[0]  # Getting the origin point

        x, y, z = origin  # Getting the x, y, z coordinates of the origin point
        self.logger.debug(f"Origin point: ({x}, {y}, {z})")

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points.to_numpy())
        return point_cloud

    def __pc_to_df(self, point_cloud: o3d.geometry.PointCloud) -> pd.DataFrame:
        """
        Converts an open3d.geometry.PointCloud object to a pandas DataFrame
        :return:
        """
        self.logger.debug("Converting PointCloud object to DataFrame...")
        points = np.asarray(point_cloud.points)
        points = pd.DataFrame(data=points, columns=["x", "y", "z"])
        return points

    def __repr__(self) -> str:
        return f"is parent: {self.__is_parent()}; " \
               f"no. of children: {len(self.segmented_LAS)}; " \
               f"no. of points: {len(self.point_cloud.points)}; " \
               f"plane: {self.plane};"
