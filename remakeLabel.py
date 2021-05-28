import SimpleITK as sitk
import numpy as np
import argparse
from pathlib import Path
import sys
sys.path.append("..")
from utils.utils import getImageWithMeta

def parseArgs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("label_path")
    parser.add_argument("save_path")
    parser.add_argument("--num_class", default=14, type=int)
    parser.add_argument("--ignore_classes", nargs="*", type=int)
    parser.add_argument("--squeeze", action="store_true")

    args = parser.parse_args()

    return args


def main(args):
    label       = sitk.ReadImage(args.label_path)
    label_array = sitk.GetArrayFromImage(label)

    cnt = 0
    for c in range(args.num_class):
        if c in args.ignore_classes:
            label_array = np.where(label_array == c, 0, label_array)

        else:
            if args.squeeze:
                label_array = np.where(label_array == c, cnt, label_array)
                cnt += 1
            else:
                label_array = np.where(label_array == c, c, label_array)
    
    print("Max_num_class: ", label_array.max())
    re_label = getImageWithMeta(label_array, label)
    Path(args.save_path).parent.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(re_label, args.save_path, True)

if __name__ == "__main__":
    args = parseArgs()
    main(args)

