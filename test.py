import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--example', nargs='?', const=1, type=int)
args = parser.parse_args()
print(args)