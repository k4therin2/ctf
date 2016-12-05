Flag 6
======

The hint:

> Time to dust off your 233 knowledge. It's a linked list!

The link takes you to `/linkedlist/4040240587`, which returns the following:

```
next: 482900906
```

If you go to `/linkedlist/482900906`, you see another number, and the pattern
continues. There are well over a hundred items in this list, making it rather
impractical to follow by hand.

Some Javascripting or Python+requests wizardry can help you follow this chain. I
choose Python!

```python
import re
import requests

URL = 'https://ctf.brennan.io/linkedlist/%d'
START = 4040240587

def follow(start=START):
    # Regexes to help us along the way.
    flag_pattern = re.compile(r'flag{.*}', re.I)
    next_pattern = re.compile(r'next: (\d+)')

    current_message = ''
    current_number = start

    # Keep going till we find a flag.
    while True:
        current_url = URL % current_number
        current_message = requests.get(current_url).text

        if flag_pattern.search(current_message):
            return flag_pattern.search(current_message).group(0)

        current_number = int(next_pattern.search(current_message).group(1))
        print(current_number)

    return flag_pattern.search(current_message).group(0)
```

Unfortunately, this first stab at it doesn't work. You can run this for a while,
but it just keeps going. And it goes by really fast, so it feels wrong that the
linked list could be this long. Maybe your code is blindly going in a big
circle? So you modify your code to keep track of what numbers you've already
visited:

```python
import re
import requests

URL = 'https://ctf.brennan.io/linkedlist/%d'
START = 4040240587

def follow(start=START):
    # Regexes to help us along the way.
    flag_pattern = re.compile(r'flag{.*}', re.I)
    next_pattern = re.compile(r'next: (\d+)')

    current_message = ''
    current_number = start
    visited = {start} # ADDED

    # Keep going till we find a flag.
    while True:
        current_url = URL % current_number
        current_message = requests.get(current_url).text

        if flag_pattern.search(current_message):
            return flag_pattern.search(current_message).group(0)

        current_number = int(next_pattern.search(current_message).group(1))
        print(current_number)

        # ADDED
        if current_number in visited:
            print('DUPLICATE')
            return None
        visited.add(current_number)

    return flag_pattern.search(current_message).group(0)
```

And what do you know, the function terminates pretty quickly. The first
duplicated node was 1041076672. If you go through the output and find the first
occurrence of that node, you'll find that the node before it was 425101183. If
you manually visit that node, you see that its page says:

```
next: 1041076672 but the real one is: 3506824557
```

If you then start following the list from the "real one", you get to the flag:

```python
>>> follow(3506824557)
4068663810
3361578469
173931658
2604327608
4077109072
1170610549
3417008397
2467291240
4234243506
304929842
1788629081
2836148587
1486555373
1321846281
716697196
2830838390
687241805
1269474893
330611746
'flag{never_break_the_chain}'
```

And so the flag is

```
flag{never_break_the_chain}
```

Incidentally, this is a Fleetwood Mac [reference][ref]. NOT Taylor Swift.

Alternative
-----------

You don't *have* to look at the list item before the first occurrence of the
first duplicated item. (That sentence alone is a bit of a mouthful). Instead,
you could just have your code print out each message body as it goes, hoping
that you would see something odd jump at you.

Behind The Scenes
-----------------

You can look at the function `linkedlist()` in [server.py][] to see how this
works. The nodes are all stored in one big dictionary in [linkedlist.py][], with
comments showing fork and loop and everything.

[server.py]: ../server/server.py
[linkedlist.py]: ../server/linkedlist.py

[ref]: https://www.youtube.com/watch?v=XAqdnACpud8
