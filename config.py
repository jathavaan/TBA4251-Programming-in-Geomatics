import os
from enum import Enum


class Config(Enum):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to project root
    SOURCE_DIR = os.path.join(ROOT_DIR, "src")  # Path to source folder
    LOG_DIR = os.path.join(SOURCE_DIR, "logger", "logs")  # Path to log folder

    DATA_DIR = os.path.join(ROOT_DIR, "data")  # Path to data folder
    SPEEDBUMP_DATA_PATH = os.path.join(DATA_DIR, "speedbump_lidar.las")  # Path to speedbump lidar data
