import SimpleITK as sitk
import numpy as np
from scipy.signal import convolve
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("label_path")
    parser.add_argument("save_path")
    parser.add_argument("-r", "--radius", type=int, default=1)
    parser.add_argument("--num_class", type=int, default=14)

    args = parser.parse_args()

    return args

def main(args):
    label       = sitk.ReadImage(args.label_path)
    label_array = sitk.GetArrayFromImage(label)

    label_array_onehot = makeOnehot(label_array, args.num_class)

    output_array = None
    print("Calculating...")
    for c in range(args.num_class):
        lawc = countAmbientLabel(label_array_onehot[..., c], radius=args.radius)
        lawc = lawc[np.newaxis, ...]

        if output_array is None:
            output_array = lawc
        else:
            output_array = np.concatenate([output_array, lawc], axis=0)
    print("Done.")

    print("Saving array to {}...".format(args.save_path))
    np.save(args.save_path, output_array)


def countAmbientLabel(array, radius=1):
    ndim = array.ndim
    kernel = np.ones([1 + 2*radius] * ndim)

    count_array = convolve(array, kernel, mode="same")

    return count_array


def makeOnehot(array, num_class):
    return np.eye(num_class)[array]

if __name__ == "__main__":
    args = parseArgs()
    main(args)
