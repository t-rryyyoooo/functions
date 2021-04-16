import argparse
import SimpleITK as sitk
from pathlib import Path

args = None

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("imagePath", help="$HOME/Desktop/data/kits19/case_00000")
    parser.add_argument("savePath", help="$HOME/Desktop/data/kits19/case_00000")
    parser.add_argument("--input_name", default="imaging.nii.gz")
    parser.add_argument("--save_name", default="imaging_resampled.nii.gz")
    parser.add_argument("--spacing", default=[1.0, 1.0, 1.0], type=float, nargs=3)

    args = parser.parse_args()
    return args


def changeSpacing(img, spacing, is_label=False):
    # original shape
    inputShape = img.GetSize()
    inputSpacing = img.GetSpacing()
    newShape = [ int(1 + ish * isp / osp) for ish, isp, osp in zip(inputShape, inputSpacing, spacing)]
    print("Change spacing from {} to {}.".format(inputSpacing, spacing))
    print("So, Change shape from {} to {}.".format(inputShape, newShape))
    
    if img.GetNumberOfComponentsPerPixel() == 1:
        minmax = sitk.MinimumMaximumImageFilter()
        minmax.Execute(img)
        minval = minmax.GetMinimum()
    else:
        minval = None

    resampler = sitk.ResampleImageFilter()
    resampler.SetSize(newShape)
    resampler.SetOutputOrigin(img.GetOrigin())
    resampler.SetOutputDirection(img.GetDirection())
    resampler.SetOutputSpacing(spacing)
    
    
    if minval is not None:
        resampler.SetDefaultPixelValue(minval)
    if is_label:
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
   
    resampled = resampler.Execute(img)
    
    return resampled

def main(args):
    imagePath = Path(args.imagePath) / args.input_name

    image = sitk.ReadImage(str(imagePath))
    resampledImage = changeSpacing(image, [*args.spacing])

    saveImagePath = Path(args.savePath) / args.save_name

    print("saving Image to {}...".format(saveImagePath))
    sitk.WriteImage(resampledImage, str(saveImagePath), True)
    print("Done.")

if __name__=="__main__":
    args = parseArgs()
    main(args)
