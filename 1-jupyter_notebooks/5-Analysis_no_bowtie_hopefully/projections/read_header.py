import numpy as np
import argparse

# parse the file name
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', metavar='f', type=str, nargs='+',
                    help='an integer for the accumulator')
args = parser.parse_args()

# read the file
f = np.load(args.file[0], allow_pickle=True)


for item in f[0].items():
    print(item)
