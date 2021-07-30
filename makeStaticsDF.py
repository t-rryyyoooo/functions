import argparse
import pandas as pd
import SimpleITK as sitk
import numpy as np
from pathlib import Path
import sys
sys.path.append("..")
from utils.utils import printArgs
from tqdm import tqdm

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_dir")
    parser.add_argument("save_path")
    parser.add_argument("--image_names", nargs="*", default=["SE2_resampled.nii.gz", "SE3_resampled.nii.gz"])
    parser.add_argument("--label_name", default="CCRCC_resampled.nii.gz")
    parser.add_argument("--image_indices", nargs="*", default=["SE2", "SE3"])
    parser.add_argument("--label_index", default="CCRCC" )
    parser.add_argument("--search_axis", default=0, type=int)

    args = parser.parse_args()

    return args

def main(args):
    printArgs(args)

    d = dict()
    d["ID"] = []

    suffix_list = ["mean", "std", "min", "median", "max"]
    d[args.label_index + "_size"] = []
    d[args.label_index + "_size_ratio"] = []
    for image_index in args.image_indices:
        for suffix in suffix_list:
            index = image_index + "_" + args.label_index + "_" + suffix
            d[index] = []

    dir_list = sorted(Path(args.data_dir).glob("case_*/{}".format(args.label_name)))
    for directory in dir_list:
        directory = directory.parent
        ID = str(directory).split("/")[-1]
        if ID == "case_016":
            continue
        print(str(directory))

        label_path  = directory / args.label_name
        label_array = sitk.GetArrayFromImage(sitk.ReadImage(str(label_path)))

        masked_image_array_list = []
        for image_name in args.image_names:
            image_path  = directory / image_name
            image_array = sitk.GetArrayFromImage(sitk.ReadImage(str(image_path)))

            masked_image_array_list.append(np.ma.masked_array(image_array, (label_array == 0)))


        d["ID"].append(ID)
        size = (label_array > 0).sum()
        d[args.label_index + "_size"].append(size)
        size_ratio = size / np.prod(label_array.shape)
        d[args.label_index + "_size_ratio"].append(size_ratio)

        for masked_image_array, image_index in zip(masked_image_array_list, args.image_indices):
            mean = np.ma.mean(masked_image_array)
            std  = np.ma.std(masked_image_array)
            Min  = np.ma.min(masked_image_array)
            med  = np.ma.median(masked_image_array)
            Max  = np.ma.max(masked_image_array)
            statics = [mean, std, Min, med, Max]

            assert len(statics) == len(suffix_list)
            for suffix, static in zip(suffix_list, statics):
                index = image_index + "_" + args.label_index + "_" + suffix
                d[index].append(static)

        print("DONE")

    print(d)
    df = pd.DataFrame(d)
    Path(args.save_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.save_path, index=False)

                

if __name__ == "__main__":
    args = parseArgs()
    main(args)
