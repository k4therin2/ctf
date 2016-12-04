import string
import re
from itertools import zip_longest

letter_map = {l: 0 if ord(l) - ord('A') < 13 else 1 for l in string.ascii_uppercase}
message = '''
Hi good dear,<br><br>

I have some exciting info about the jail. They recently added a great workout
device within their good fitness area. Very fun fitness devices will allow
their very varied crew in here to hit nice fitness goals.<br><br>

If I have your goals? No, you shouldn't have goals of less abs. That be
scarcely make any sense.<br><br>

Bye!
'''


def wordlist(message):
    words = message.upper().split()
    non_letters = re.compile(r'[^A-Z]')
    return [non_letters.sub('', w) for w in words]


def parity(words):
    sums = [sum(letter_map[l] for l in w) for w in words]

    print('PARITY COMPUTATION')
    maxlen = max(map(len, words))
    for w, s in zip(words, sums):
        bstr = ''.join('1' if letter_map[l] else '0' for l in w)
        pad = ' ' * (maxlen - len(w))
        print('%s - %s: %d' % (pad + w, pad + bstr, s % 2))

    return [s % 2 for s in sums]


# http://stackoverflow.com/a/312644/820319
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def binary(l):
    """Takes [1, 0, 1, 0] and returns 10, e.g."""
    num = 0
    for i, x in enumerate(l):
        num += int(x) * (2 ** (len(l) - i - 1))
    return num


def unchunk(par, n):
    """Takes a list of bits, breaks it into several chunks of length n, and
    then converts each chunk into a number."""
    numbers = []
    for group in grouper(n, par):
        if None in group:
            return numbers
        numbers.append(binary(group))
    return numbers


def translate(chunks):
    s = ''
    for c in chunks:
        s += string.ascii_uppercase[c % 26]
    return s


def main():
    import sys
    if len(sys.argv) < 2:
        msg = message
    else:
        with open(sys.argv[1]) as f:
            msg = f.read()
    wl = wordlist(msg)
    par = parity(wl)
    nums = unchunk(par, 5)
    print(translate(nums))


if __name__ == '__main__':
    main()
