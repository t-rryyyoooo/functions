import argparse
import numpy as np
import SimpleITK as sitk
from itertools import product
import sys
sys.path.append("..")
from utils.utils import getImageWithMeta, printArgs
from collections import deque
from pathlib import Path

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("label_path")
    parser.add_argument("save_path")

    args = parser.parse_args()

    return args

class DFS():
    def __init__(self, label_array):
        self.label_array = label_array
        self.roi_array   = np.zeros_like(label_array)

        self.zero_list = np.array([0] * self.label_array.ndim)
        self.size_list = np.array(self.label_array.shape)


        self.stack = deque([])
        self.cnt   = 0


    def scanVoxels(self):
        ranges  = [range(s) for s in self.label_array.shape]
        indices = [i for i in product(*ranges)]

        for index in indices:
            idx = tuple([[i] for i in index])
            if self.label_array[idx] == 1 and self.roi_array[idx] == 0:
                yield index

    def changeValueInList(self, l, position, value):
        ll = l.copy()
        ll[position] = value
        return ll

    def __call__(self):
        for new_index in self.scanVoxels():
            self.cnt += 1
            self.stack.append(list(new_index) + [self.cnt])
            print("Start index: {}".format(new_index))
            print("The number of ROI: {}".format(self.cnt))

            while self.stack:
                index_cnt = self.stack.pop()
                index     = index_cnt[:-1]
                idx       = tuple([[i] for i in index_cnt[:-1]])
                cnt       = index_cnt[-1]
                if (index < self.zero_list).any() or (index >= self.size_list).any():
                    continue

                if self.label_array[idx] == 0 or self.roi_array[idx] > 0:
                    continue

                self.roi_array[idx] = cnt

                for i in range(self.label_array.ndim):
                    for r in [-1, 1]:
                        ci  = index[i] + r
                        dist_index = self.changeValueInList(index_cnt, i, ci)

                        self.stack.append(dist_index)

            print(self.roi_array.max())

def main(args):
    printArgs(args)
    label       = sitk.ReadImage(args.label_path)
    label_array = sitk.GetArrayFromImage(label)

    dfs = DFS(label_array)
    dfs()

    roi = getImageWithMeta(dfs.roi_array, label)
    print("Saving label array counted roi...", end=" ", flush=True)
    Path(args.save_path).parent.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(roi, args.save_path, True)
    print("DONE", flush=True)

if __name__ == "__main__":
    args = parseArgs()
    main(args)


