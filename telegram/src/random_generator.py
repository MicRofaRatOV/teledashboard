import random


def generate_md5_str():
    return "%032x" % random.getrandbits(128)