from config import Config
from src.file_handling.las import LAS


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    filtered_LAS = (l for l in las.filter_deviations())
    for filtered_las in filtered_LAS:
        print(filtered_las)



if __name__ == "__main__":
    main()
