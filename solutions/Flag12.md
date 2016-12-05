Flag 12
=======

The hint:

> Liberatore has encrypted his secret using a hash function! Luckily, he chose very weak hash function. Given the hashed flag, reverse-engineer the function to find the original value!

Looking at the provided code:
```python
def sweet_hash(string):
    x = 42
    byte = []

    for char in string:
        byte.append(x ^ ord(char))
        x ^= ord(char)

    return b64encode(bytes(byte))
```
We can see that there's an initial value ```x = 42``` which gets XOR'd against the first character of the string. XOR is its own inverse, so we know that:

```A ^ A ^ B = B```

Additionally, the XOR operator is commutative, so we know that:

```A ^ B = B ^ A```

We can apply these two facts to attack the algorithm. We know that ```byte[i] ^ x[i] = string[i]```, so can derive the first character of the flag with very little effort. Next, the value ```x[i+1]``` gets set to ```x[i] ^ string[i]```. We can then make the substitution:

```x[i+1] = x[i] ^ string[i] = x[i] ^ (byte[i] ^ x[i])```

and then simplify using the inverse and commutative properties:

```
x[i+1] = x[i] ^ byte[i] ^ x[i]
x[i+1] = x[i] ^ x[i] ^ byte[i]
x[i+1] = byte[i]
```

So even though the hash process seems complex and unpredictable for an unknown input, it turns out we had the key the whole time! Now we can write an un-hashing function by using ```x = 42``` for the first byte and the previous byte for all the others:

```python
def unhash(binary):
    x = 42
    hash_bytes = b64decode(binary)
    string = ''

    for byte in hash_bytes:
        string += chr(x ^ byte)
        x = byte

    return string
```
```python
In:     unhash(b'TCBBJl06WylQfRRzHXwIYRRnSj5bOlg3UypX')
Out:    'flag{gary-ignatius-teabody}'
```

As it turns out, it is actually easier to decrypt this information than it is to encrypt it... Maybe it's time for Liberatore to choose a different algorithm!

Notes
====
In python, ```ord``` returns the integer key code (in Unicode) for a single character. Its complement, ```chr```, returns the single-character string for a given key code.

This code uses Base-64 encoding rather than raw bytes. The methods ```b64encode``` and ```b64decode``` are provided by the module ```base64```.

In general, a hash function is a so-called "trapdoor" function, meaning that it should be impossible to simply reverse the function to get the input for a given output. Particularly strong hash functions, used in actual cryptographic algorithms, have a few other interesting properties, including that if an attacker knew any subsequence of the output, it can't be used to derive earlier or later bytes in the output. Hashes like md5 are also used to map large blobs of binary data to a more managable fingerprint, so if you're downloading a large file your computer can with high probability verify that it downloaded it correctly.
