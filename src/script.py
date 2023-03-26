import numpy as np
import open3d as o3d
import pandas as pd
from matplotlib import pyplot as plt

from config import Config
from src.file_handling.las import LAS
from src.logger.logger import Logger


def main() -> None:
    LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)


if __name__ == "__main__":
    main()
