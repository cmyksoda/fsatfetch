#==========================================
#    Makefile: makefile for sl 5.1
#	Copyright 1993, 1998, 2014
#                 Toyoda Masashi
#		  (mtoyoda@acm.org)
#	Last Modified: 2014/03/31
#
#    Forked by cmyksoda (jaxi@cmyksoda.cc)
#    Last Modified: 2026/07/01
#==========================================
CC          = gcc
CFLAGS      = -O -Wall
PRIMARY     = fsatfetch
INSTALL_DIR = $(HOME)/.local/bin

all: $(PRIMARY)

$(PRIMARY): sl.c sl.h
	$(CC) $(CFLAGS) -o $@ sl.c -lncurses
	
install: $(PRIMARY)
	mkdir -p $(INSTALL_DIR)
	cp $(PRIMARY) $(INSTALL_DIR)/$(PRIMARY)
	python3 hooks.py install $(INSTALL_DIR)/$(PRIMARY)
	mkdir -p $(HOME)/.local/share/man/man1
	cp fsatfetch.1 $(HOME)/.local/share/man/man1/fsatfetch.1
	mandb -q 2>/dev/null || true
	
uninstall:
	python3 hooks.py uninstall
	rm -f $(INSTALL_DIR)/$(PRIMARY)
	rm -f $(HOME)/.local/share/man/man1/fsatfetch.1
	
clean:
	rm -f $(PRIMARY)
	
distclean: clean