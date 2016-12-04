# flag 23
# python crap.py 'flag{whatever}'

import random
from itertools import zip_longest


JUNK = '!"#$%&\'()*+,-./:;<=>?@[\\]^`|~'


def hide_message(message, junk):
    output = ''
    for c in message:
        for _ in range(random.randint(400, 600)):
            output += random.choice(junk)
        output += c
    for _ in range(random.randint(400, 600)):
        output += random.choice(junk)
    return output


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def wrap_message(message):
    return '\n'.join(''.join(x for x in t) for t in grouper(80, message, ''))


if __name__ == '__main__':
    import sys
    print(wrap_message(hide_message(sys.argv[1], JUNK)))
