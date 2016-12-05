Flag 39
=======
The hint:

> Your friend, a Harvard English professor, is in jail and has written you a strange letter! It seems to be about workout machines, but maybe there is something hidden within the text. 

> Here's what you know: your friend probably wants to communicate something to you. He can't use any complicated cryptography, because he's in jail and they'd totally notice if he was writing down a bunch of figures on a napkin.

> You remember a conversation you were having with him once upon a time, before he went to jail, about a stupid cryptosystem where you split the alphabet in half, assign a 0 for the first half, a 1 for the second half, take the parity of each word, and somehow map that to the alphabet...
>> Hi good dear,
I have some exciting info about the jail. They recently added a great workout device within their good fitness area. Very fun fitness devices will allow their very varied crew in here to hit nice fitness goals.
If I have your goals? No, you shouldn't have goals of less abs. That be scarcely make any sense.
Bye!

To break up the problem, we can infer from our "once upon a time conversation" that we have to do the following things:

* Normalize the content of the letter so we just have words with no punctuation
* Map each character to a bit
* Use the parity to turn some group of words into a number

### Normalizing the Letter

With some python magic, we can put the letter into lowercase and remove fancy whitespace:
```python
letter = letter.lower().replace('\n', ' ')
```

Then, we can use ```string.ascii_lowercase``` to remove unwanted characters:
```python
letter = ''.join(filter(lambda char: char in string.ascii_lowercase + ' ', letter))
```
Which should give you:
```python
In:		letter
Out:	'hi good dear i have some exciting info about the jail they recently added a great workout device within their good fitness area very fun fitness devices will allow their very varied crew in here to hit nice fitness goals if i have your goals no you shouldnt have goals of less abs that be scarcely make any sense bye'
```
Now getting each normalized word is as easy as ```words = letter.split(' ')```.

### Mapping Characters to Bits

We want to map the first half of the alphabet to 0 and the second half to 1. This can be done in one line with a sweet one line dictionary comprehension:
```python
char_map = {c: 1 if ord(c) < ord('n') else 0 for c in string.ascii_lowercase}
```
Then we can map each word in ```words``` to a list of bits:
```python
bits = [[char_map[c] for c in word] for word in words]
```
Quick sanity check:
```python
In:		words[12]
Out:	'recently'
In:		bits[12]
Out:	[1, 0, 0, 0, 1, 1, 0, 1]
```

### Bits to Parity to Numbers

Parity is the state of something being either even or odd. For our list ```bits```, we can then figure out the parity:
```python
parity = [sum(b) % 2 for b in bits]
```
Now that we have the parity, which is what our friend told us to do, we have to guess how they might have encoded letters into the parity bits. The simplest possible encoding would be to group every 5 bits and encode ```a = 0```, ```b = 1```, etc. Since 5 bits would give a total of 32 possible values, we know the entire alphabet, or at least one case, can be encoded into it.

Lets define a few helper functions:
```python
from functools import reduce  # python3

group = lambda iterable, n: list(zip(*[iter(iterable)] * n))
twos = lambda bits: reduce(lambda a, b: 2 * a + b, bits, 0)
```
```python
In:		group([1, 2, 3, 4, 5, 6], 3)
Out:	[(1, 2, 3), (4, 5, 6)]
In:		twos((0, 0, 1, 0, 1))
Out:	5
```
We can then use these to figure out the 5 bit values and offset their 0 to the ascii ```a```:
```python
groups = group(parity, 5)
nums = [ord('a') + twos(group) for group in groups]
```
And finally we can reveal the flag:
```python
In:		''.join(map(chr, nums))
Out:	'flaggetmeout'
```
