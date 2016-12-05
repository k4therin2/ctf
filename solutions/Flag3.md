Flag 3
======

Running on a server at TCP port `mtb.wtf:1776` is the rust
program [tcpdumpflag.rs](../tcpdumpflag.rs). If you open a TCP connection and
wait one second, it will send you a flag. If you send anything within one
second, it will close the connection on you. So you can't visit it with a
browser, instead you should do something like `telnet mtb.wtf 1776`.

The solution is:

```
flag{All men are created equal}
```
