import os
from enum import Enum


class Config(Enum):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    SPEEDBUMP_DATA_PATH = os.path.join(DATA_DIR, "speedbump_lidar.las")
