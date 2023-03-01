from config import Config
from src.file_handling.handle_las import HandleLAS


def main() -> None:
    las = HandleLAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    las.display_point_cloud()


if __name__ == "__main__":
    main()
