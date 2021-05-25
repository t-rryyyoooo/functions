import SimpleITK as sitk
import numpy as np
from pathlib import Path
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

class PerimeterLabelArrayCreater():
    def __init__(self, label_array=None, radius=1, num_class=14):
        self.label_array = label_array
        self.radius      = radius
        self.num_class   = num_class

    def __call__(self):
        onehot_array = self.makeOnehot(self.label_array, args.num_class)

        perimeter_array = None
        for c in range(args.num_class):
            pa = self.countAmbientLabel(onehot_array[..., c], radius=self.radius)
            pa = pa[np.newaxis, ...]

            if perimeter_array is None:
                perimeter_array = pa
            else:
                perimeter_array = np.concatenate([perimeter_array, pa], axis=0)
        counter_array = self.countAmbientLabel(np.ones_like(self.label_array), radius=args.radius)

        perimeter_array /= counter_array

        return perimeter_array

    def makeOnehot(self, array, num_class):
        return np.eye(num_class)[array]

    def countAmbientLabel(self, array, radius=1):
        ndim = array.ndim
        kernel = np.ones([1 + 2*radius] * ndim)

        count_array = convolve(array, kernel, mode="same")

        return count_array

def main(args):
    label       = sitk.ReadImage(args.label_path)
    label_array = sitk.GetArrayFromImage(label)

    plc = PerimeterLabelArrayCreater(
                label_array = label_array,
                radius      = args.radius,
                num_class   = args.num_class
                )

    output_array = plc()

    print("Saving array to {}...".format(args.save_path))
    Path(args.save_path).parent.mkdir(parents=True, exist_ok=True)

    np.save(args.save_path, output_array)

if __name__ == "__main__":
    args = parseArgs()
    main(args)
