from config import Config
from src.file_handling.las import LAS


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    segmented_point_clouds = (spc for spc in las.segmented_point_clouds)
    [spc.display() for spc in segmented_point_clouds]


if __name__ == "__main__":
    main()
