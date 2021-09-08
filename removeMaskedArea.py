import argparse
import numpy as np
import SimpleITK as sitk
from utils.utils import getImageWithMeta, printArgs

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("image_path")
    parser.add_argument("mask_path")
    parser.add_argument("save_path")

    args = parser.parse_args()

    return args

def main(args):
    printArgs(args)

    image = sitk.ReadImage(args.image_path)
    mask  = sitk.ReadImage(args.mask_path)

    image_array = sitk.GetArrayFromImage(image)
    mask_array  = sitk.GetArrayFromImage(mask)


    print("Removig masked area...")
    min_value = image_array.min()
    masked_image_array = np.where(mask_array, min_value, image_array)
    print("Done")

    print("Saving image to {}...".format(args.save_path))
    masked_image = getImageWithMeta(masked_image_array, image)

    sitk.WriteImage(masked_image, args.save_path)
    print("Done")


if __name__ == "__main__":
    args = parseArgs()
    main(args)
