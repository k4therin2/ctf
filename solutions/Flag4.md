Flag 4
======

The hint:

> All we know is this:
>
> ```
> ZmxhZ3t0b3VjaF9hbmRfZ299
> ```

That is a blob of [base64][] encoded text. You could use Python like this to
decode it:

```python
>>> import base64
>>> base64.b64decode('ZmxhZ3t0b3VjaF9hbmRfZ299')
b'flag{touch_and_go}'
```

([Python base64 module docs][doc])

And so the flag is:

```
flag{touch_and_go}
```

Hidden Flag
-----------

During the event, I (Stephen) offered a special "extra" flag for finding the
somewhat obscure Taylor Swift reference in the flags. The hint and flag for this
challenge together form "all we know is touch and go", a lyric from "State of
Grace", the first song from her album *Red*. The hidden flag for discovering
this was: `flag{dat_tswizzle_reference_tho}`.

[base64]: https://en.wikipedia.org/wiki/Base64
[doc]: https://docs.python.org/3/library/base64.html
