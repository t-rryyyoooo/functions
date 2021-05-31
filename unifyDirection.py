import argparse
import SimpleITK as sitk
import numpy as np
import sys
sys.path.append("..")
from utils.utils import getImageWithMeta, printArgs
from pathlib import Path

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("image_path")
    parser.add_argument("ref_path")
    parser.add_argument("save_path")

    args = parser.parse_args()

    return args

def main(args):
    printArgs(args)

    image = sitk.ReadImage(args.image_path)
    ref   = sitk.ReadImage(args.ref_path)

    image_array = sitk.GetArrayFromImage(image)

    unified_image = getImageWithMeta(image_array[::-1, ::-1, :], ref)
    Path(args.save_path).parent.mkdir(exist_ok=True, parents=True)

    sitk.WriteImage(unified_image, args.save_path)

if __name__ == "__main__":
    args = parseArgs()
    main(args)
