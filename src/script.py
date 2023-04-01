from config import Config
from src.file_handling.las import LAS
from itertools import pairwise

def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    las.flag_LAS()
    flagged_LAS = []

    for i, j in pairwise(las.segmented_LAS):
        if i.flagged and j.flagged:
            flagged_LAS.append(i)
            flagged_LAS.append(j)

    pc = las.point_cloud
    merged_pc = las.merge_segmented_pc(*flagged_LAS)
    # las.display(pc)
    las.display(merged_pc)


if __name__ == "__main__":
    main()
