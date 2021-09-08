import SimpleITK as sitk
import argparse
from utils.utils import printArgs

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("image_path")
    parser.add_argument("save_path")
    parser.add_argument("--radius", default=5, type=int)

    args = parser.parse_args()

    return args

def main(args):
    printArgs(args)

    img = sitk.ReadImage(args.image_path)

    f = sitk.BinaryDilateImageFilter()
    f.SetKernelRadius(args.radius)
    print("Kernel size: ", f.GetKernelRadius())

    print("Dilating images...")
    f_img = f.Execute(img)
    print("DONE")

    print("Saving image to {}...".format(args.save_path))
    sitk.WriteImage(f_img, args.save_path, True)
    print("DONE")

if __name__ == "__main__":
    args = parseArgs()
    main(args)
