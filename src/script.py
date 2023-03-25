import open3d as o3d

from config import Config
from src.file_handling.las import LAS
from src.logger.logger import Logger


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    [print(LAS.plane) for LAS in las.segmented_point_clouds]


if __name__ == "__main__":
    main()
