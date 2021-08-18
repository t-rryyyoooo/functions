import argparse
import SimpleITK as sitk
import numpy as np
from utils.utils import getImageWithMeta, printArgs

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--label_path_list", nargs="*")
    parser.add_argument("--save_path")

    args = parser.parse_args()

    return args

def checkValue(org, label, c):
    if label == 0:
        return org
    else:
        if org == 0:
            return c
        else:
            return org

def main(args):
    printArgs(args)
    label_list = []
    for label_path in args.label_path_list:
        label = sitk.ReadImage(label_path)
        label_list.append(label)
    
    label_array_list = []
    for label in label_list:
        label_array = sitk.GetArrayFromImage(label)
        label_array_list.append(label_array)

    integrated_array = np.zeros_like(label_array_list[0], dtype=np.uint8)
    ufunc = np.frompyfunc(checkValue, 3, 1)
    for i, label_array in enumerate(label_array_list[::-1]):
        i = len(label_array_list) - i
        integrated_array = ufunc(integrated_array, label_array, i)

    integrated = getImageWithMeta(integrated_array.astype(np.uint8), label_list[0])
    sitk.WriteImage(integrated, args.save_path)

if __name__ == "__main__":
    args = parseArgs()
    main(args)


