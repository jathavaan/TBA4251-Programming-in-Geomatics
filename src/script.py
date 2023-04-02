import numpy as np
from config import Config
from src.file_handling.las import LAS
from itertools import pairwise

def main() -> None:
    las = LAS(file_path=Config.SPEEDBUMP_DATA_PATH.value)
    las.flag_LAS()
    segmented_LAS = las.segmented_LAS
    flagged_LAS = []

    for i, j in pairwise(segmented_LAS):
        if i.flagged and j.flagged:
            flagged_LAS.append(i)
            flagged_LAS.append(j)

    pc = las.point_cloud
    merged_pc = las.merge_segmented_pc(*flagged_LAS)
    mean = np.mean([l.SD(l.point_cloud) for l in segmented_LAS])
    # las.display(pc)
    las.display(merged_pc)


if __name__ == "__main__":
    main()
