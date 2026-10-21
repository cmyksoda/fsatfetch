fsatfetch: cure your bad habit of mistyping
=======================================

a fork of sl (steam locomotive) that runs across your terminal when you misspell any of the following commands:  
``fastfetch, neofetch, pfetch, qwqfetch, hyfetch``  
it's just a joke command, and not useful at all.

## dependencies
- `gcc`
- `ncurses` (e.g. `libncurses-dev` on debian/ubuntu, `ncurses` on arch)
- `python3`

## install
```sh
make
make install
```
restart your shell after installing, or source your rc file (`~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`) to activate it immediately.

## uninstall
```sh
make uninstall
```

![](demo.gif)

## Credits

- **sl** by Toyoda Masashi ([mtoyoda/sl](https://github.com/mtoyoda/sl)), the steam locomotive fsatfetch is forked from, with later fixes by Chris Seymour, Jeff Schwab, and Ryan Jacobs
- **fsatfetch** forked from sl by cmyksoda (jaxi@cmyksoda.cc)
- **ncurses**, which draws the animation in the terminal

## License

fsatfetch is released under the [same license as sl](LICENSE), a short permissive license. Everyone is permitted to do anything with the program, including copying, modifying, and improving it, unless they try to pretend they wrote it, and the copyright notice has to appear in all copies. The author disclaims any responsibility with regard to the software.

Copyright 1993,1998,2014 Toyoda Masashi (mtoyoda@acm.org)

---

*This project was made with AI assistance. For more information, see [my AI usage statement](https://github.com/cmyksoda/cmyksoda/blob/main/AI_USAGE.md).*
