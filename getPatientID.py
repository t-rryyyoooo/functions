import argparse
from pathlib import Path
def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_dir", help="/sandisk/data/tsukbuaData/kidney, This direcoty has case_000, case_001, ...")
    parser.add_argument("--target_name")
    parser.add_argument("--knot", default=", ")
    parser.add_argument('--need_double_mark', action="store_true", help='True -> "000", "001", ..., False -> 000, 001')

    args = parser.parse_args()

    return args

def main(args):
    target_dir  = Path(args.target_dir)
    target_name = "case_*/"
    if args.target_name is not None:
        target_name = target_name + args.target_name
        idx = -2
    else:
        idx = -1

    for target in sorted(target_dir.glob(target_name)):
        ID     = str(target).split("/")[idx][5:]
        if args.need_double_mark:
            output = '"{}"'.format(ID)
        else:
            output = '{}'.format(ID)
        print(output, end=args.knot)


if __name__ == "__main__":
    args = parseArgs()
    main(args)

