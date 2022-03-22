from os import listdir, walk
from os.path import join
import argparse

from vcr.serializers import gzipserializer, yamlserializer


READ_CONTENT = {
    "gzip": gzipserializer.deserialize,
    "yaml": yamlserializer.deserialize,
}

def check_format(fpin, format):
    if format not in READ_CONTENT.keys():
        raise Exception("Format not recognized")
    with open(fpin, 'r') as fi:
        data = fi.read()
        try:
            READ_CONTENT[format](data)
        except Exception as e:
            raise Exception(f"Cassette '{fpin}' not encoded in format '{format}'") from e

def scan(dir_in, format):
    print("Scanning...")
    for root, providers, _ in walk(dir_in):
        print(root)
        for provider in providers:
            ind = join(root, provider)
            for file in listdir(ind):
                fpin = join(root, provider, file)
                check_format(fpin, format)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('IN', help='Input directory')
    parser.add_argument('FORMAT', help='Cassettes format')
    args = parser.parse_args()
    scan(args.IN, args.FORMAT)


if __name__ == "__main__":
    main()