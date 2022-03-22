from os import listdir, walk
from os.path import join
import argparse

from vcr.serializers.yamlserializer import deserialize as read_data
from vcr.serializers.gzipserializer import serialize as write_data
from pathlib import Path

def yaml_to_gzip(fpin, fpout):
    with open(fpin, 'r') as fi:
        with open(fpout, 'w') as fo:
            data = fi.read()
            yaml_data = read_data(data)
            compressed_data = write_data(yaml_data)
            fo.write(compressed_data)

def scan(dir_in, dir_out):
    print("Scanning...")
    for root, providers, _ in walk(dir_in):
        print(root)
        for provider in providers:
            ind = join(root, provider)
            for file in listdir(ind):
                Path(join(dir_out, provider)).mkdir(parents=True, exist_ok=True)
                fpin = join(root, provider, file)
                fpout = join(dir_out, provider, file)
                yaml_to_gzip(fpin, fpout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('IN', help='Input directory with cassettes.')
    parser.add_argument('OUT', help='Output directory.')
    args = parser.parse_args()
    scan(args.IN, args.OUT)


if __name__ == "__main__":
    main()