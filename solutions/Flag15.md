Flag 15
=======

The hint:

> Misha sent you a strange download link to a program that says "don't run me".
> Could he be trying to use reverse psychology on you? Who knows! But there is a
> flag somewhere in this program, if you can snoop it out.
>
> - [Linux](../bin/DontRunMe)
> - [macOS](../bin/DontRunMe.mac)
> - [Windows](../bin/DontRunMe.exe)

These download links are for compiled versions of [DontRunMe.c](../DontRunMe.c).
The code has to run on all 3 operating systems, so it looks a bit gross as a
result. However, the basic stuff it does is:

1. Send some random packets of data to `mtb.wtf` on [UDP][] port 58008.
2. Then, send the flag to `mtb.wtf` on UDP port 58008.
3. Then, send some more random packets.

The code uses the same XOR cipher as Flag 14 to store the key so that you can't
simply run `strings` on the binary and find the flag.

The easiest approach is hinted at by the additional info in the hint: use
Wireshark, check out UDP port 58008. If you run Wireshark, capture on your
normal internet connection, set a filter that says simply `udp`, and then run
the program, you'll see a burst of traffic. If you look through those packets,
you'll see random data in all but one, which contains the flag:

```
FLAG{c_is_the_best_and_you_should_all_learn_it}
```

A more involved approach
------------------------

This isn't the only way you could find the flag. Imagine that you ran strings on
the program. You wouldn't have found the flag, but you may have stumbled upon
the following interesting bit of text:

```
random/keys+are#more%secure[but,oh.well
```

Maybe you solved the previous flag well enough to understand that I was using
the XOR cipher a lot. Then maybe you found the encrypted string and used that
key to successfully decrypt the flag. That seems like a lot of ifs and buts
though.

On the other hand, you know that there's a flag in there, and this "key" hints
at it being encrypted. Presumably, the flag has to be decrypted at some point
before it can be used in the program. You notice that when you run the program,
it pauses at the screen:

```
$ ./DontRunMe
If a flag goes through a wire, does it make any noise?
<enter to quit, you may want to run me again>
```

You can use this opportunity to kill the process and create a [core dump][]:

```
# from a separate terminal
$ pkill -QUIT DontRunMe
```

The `SIGQUIT` signal tells the operating system to kill the process and create a
core dump, which is a file containing the memory contents of the program. Some
very useful stuff right there. Depending on your computer you may need to do
some wizardry to find where the core dump went. For me (Stephen) on Arch Linux,
I needed to use `coredumpctl list` to find a list of core dump files. I found
the core dump for `DontRunMe` and used `coredumpctl info DontRunMe` to output
the filename of the core dump. Since it was LZ4 compressed, I then used the
following to decompress, find strings, and search for the flag (case
insensitive):

```
$ lz4cat FILENAME | strings | grep -i 'flag{'
FLAG{c_is_the_best_and_you_should_all_learn_it}
```

Point is, there's lots of ways to skin the cat. This way involves no wireshark
or understanding of networking, but it does involve understanding some more
in-depth Linux/Unix concepts, like core dumps, signals, the strings program, and
grep. Plus, it's entirely possible that this might not have worked! If I had
decided to be more secretive with my program, I could have just re-encrypted the
flag immediately after sending it, so that the flag would be decrypted in memory
for only as long as I needed to send it. This would have made it *much* harder
to use the core dump approach.

[UDP]: https://en.wikipedia.org/wiki/User_Datagram_Protocol
[core dump]: https://en.wikipedia.org/wiki/Core_dump
