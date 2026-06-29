fsatfetch: cure your bad habit of mistyping
=======================================

A fork of SL (Steam Locomotive) that runs across your terminal when you misspell any of the following commands:  
``fastfetch, neofetch, pfetch, qwqfetch, hyfetch``  
It's just a joke command, and not useful at all.

## dependencies
- `gcc`
- `ncurses` (e.g. `libncurses-dev` on debian/ubuntu, `ncurses` on arch)
- `python3`

## install
```sh
make
make install
```
restart your shell after installing, or run the export line printed by the installer.

## uninstall
```sh
make uninstall
```

Copyright 1993,1998,2014 Toyoda Masashi (mtoyoda@acm.org)
Forked by cmyksoda (jaxi@cmyksoda.cc)

![](demo.gif)
