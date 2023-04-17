#!/usr/bin/python3

import sqlite3
import random


def generate_md5_str():
    return "%008x" % random.getrandbits(32)


def watch_kays():
    print(generate_md5_str())


def main():
    watch_kays()


if __name__ == "__main__":
    main()
