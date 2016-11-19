#!/usr/bin/env python3
from functools import reduce
from base64 import b64encode

# I08uSTJVNEY/EnscchNnDnsIJVE0VTdYPEU4


def sweet_hash(string):
    x = 69
    byte = []

    for char in string:
        byte.append(x ^ ord(char))
        x ^= ord(char)

    return b64encode(bytes(byte))
