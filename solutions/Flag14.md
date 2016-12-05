Flag 14
=======

The hint:

> Have fun!
>
> ```
> char turing[]="\033\027\002\032\000\131\015\024\014\015\036\016\022\021\012\107\006";
> char semaphore='}';char trie='{';char link_state='c';int main(int argc,char **argv){
> int i;for(i=0;i<sizeof(turing)-1;i++){if(i%3==0){putchar(turing[i]^semaphore);}else
> if(i%3==1){putchar(turing[i]^trie);}else{putchar(turing[i]^link_state);}}putchar('\n');}
> ```

This is a neat block of obfuscated code. If you've used C before, you might be
able to tell that it's C. In particular, the use of `char **` and functions like
`putchar()` would be things that most obviously differentiate this from other
C-like languages.

**Simple Solution:** Just compile and run the code! It'll spit out a flag, even
though you can't read one out of the source code.

```
flag{:poopemoji:}
```

**The fun stuff:** If you [format][] it (which you don't really need to do to
solve the puzzle), you get the following code:

```c
char turing[] = "\033\027\002\032\000\131\015\024\014\015\036\016\022\021\012\107\006";
char semaphore = '}';
char trie = '{';
char link_state = 'c';
int main(int argc, char ** argv) {
  int i;
  for (i = 0; i < sizeof(turing) - 1; i++) {
    if (i % 3 == 0) {
      putchar(turing[i] ^ semaphore);
    } else
    if (i % 3 == 1) {
      putchar(turing[i] ^ trie);
    } else {
      putchar(turing[i] ^ link_state);
    }
  }
  putchar('\n');
}
```

This is an implementation of the [XOR cipher][]. Basically, given a sequence of
bytes (plaintext or ciphertext) and another sequence of bytes (the key), you XOR
(exclusive OR) the bytes of the key with the bytes of the message, repeating the
key as necessary. This operation can encrypt plaintext to produce ciphertext,
and if you do the same thing with the ciphertext, you'll get back the original
plaintext!

In particular, this implementation uses a key of length three: `"}{c"`. To
obfuscate it a bit more, it uses a bunch of if statements and modular arithmetic
to achieve the same result that you would get from a simpler implementation:

```c
char *ciphertext[] = "...";
char *key [] = "}{c";
int keylen = sizeof(key) - 1;
for (int i = 0; i < sizeof(ciphertext) - 1; i++) {
  // XOR!
  putchar(ciphertext[i] ^ key[i % keylen]);
}
putchar('\n');
```

Also the variables have some weird and misleading names in the original code!

The `turing` variable contains the encrypted flag, and when the program runs, it
prints out the decrypted flag and exits. Interestingly enough, the operation for
encrypting and decrypting is the same!

[format]: http://codebeautify.org/c-formatter-beautifier
[XOR cipher]: https://en.wikipedia.org/wiki/XOR_cipher
