from config import Config
from src.file_handling.las import LAS


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    print(las)


if __name__ == "__main__":
    main()
