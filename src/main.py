from config import Config
from src.file_handling.las import LAS
from src.logger.logger import Logger


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    segmented_point_clouds = las.segmented_point_clouds
    [
        spc.display(spc.point_cloud)
        if spc.plane.standard_deviation() > 10
        else Logger.get_logger(__name__).info(
            f"Plane {spc.plane} has a standard deviation of {spc.plane.standard_deviation()}"
        )
        for spc in segmented_point_clouds
    ]


if __name__ == "__main__":
    main()
