import yaml

# Use the libYAML versions if possible
try:
    from yaml import CLoader as Loader, CDumper as Dumper
    import zlib
    from base64 import b64encode, b64decode
except ImportError:
    from yaml import Loader, Dumper


def deserialize(b64encoded_cassete):
    compressed_cassete = b64decode(b64encoded_cassete.encode())
    cassette_string = zlib.decompress(compressed_cassete).decode()
    return yaml.load(cassette_string, Loader=Loader)

def serialize(cassette_dict):
    cassette_string = yaml.dump(cassette_dict, Dumper=Dumper)
    compressed_cassete = zlib.compress(cassette_string.encode())
    return b64encode(compressed_cassete).decode()
