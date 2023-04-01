from config import Config
from src.file_handling.las import LAS


def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    las.flag_LAS()
    flagged_LAS = [l for l in las.segmented_LAS if l.flagged]
    [print(l.SD(l.point_cloud)) for l in flagged_LAS]
    merged_pc = las.merge_segmented_pc(*flagged_LAS)
    las.display(merged_pc)


if __name__ == "__main__":
    main()
