import logging
import os
from enum import Enum


class Config(Enum):
    # PATHS
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to project root
    SOURCE_DIR = os.path.join(ROOT_DIR, "src")  # Path to source folder
    LOG_DIR = os.path.join(SOURCE_DIR, "logger", "logs")  # Path to log folder

    DATA_DIR = os.path.join(ROOT_DIR, "data")  # Path to data folder
    SPEEDBUMP_DATA_PATH = os.path.join(DATA_DIR, "speedbump_lidar.las")  # Path to speedbump lidar data

    # SETTINGS
    # General settings
    LOGGING_LEVEL = logging.INFO  # Logging level
    SHOW_NORMAL_VECTORS = False  # Whether to show normal vectors in the 3D viewer

    # Voxel grid settings
    VOXEL_SIZE = 1e3  # Voxel size for downsampling

    # RANSAC settings
    DISTANCE_THRESHOLD = 175  # Distance threshold for RANSAC algorithm
    RANSAC_N = 3  # Number of points to sample for RANSAC algorithm
    NUM_ITERATIONS = 150  # Number of iterations for RANSAC algorithm

    # Plane split settings
    SPLIT_SCALE_FACTOR = 3e-3  # Scaling factor for splitting the point cloud into smaller dataframes [0, 1]

    # Thresholds
    SE_THRESHOLD = 1.8, 2.3
    SD_THRESHOLD = 430, 435
