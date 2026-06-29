#==========================================
#    Makefile: makefile for sl 5.1
#	Copyright 1993, 1998, 2014
#                 Toyoda Masashi
#		  (mtoyoda@acm.org)
#	Last Modified: 2014/03/31
#
#    Forked by cmyksoda (jaxi@cmyksoda.cc)
#    Last Modified: 2026/06/29
#==========================================
CC          = gcc
CFLAGS      = -O -Wall
PRIMARY     = fsatfetch
INSTALL_DIR = $(HOME)/.local/bin/$(PRIMARY)

all: $(PRIMARY)

$(PRIMARY): sl.c sl.h
	$(CC) $(CFLAGS) -o $@ sl.c -lncurses

install: $(PRIMARY)
	mkdir -p $(INSTALL_DIR)
	cp $(PRIMARY) $(INSTALL_DIR)/$(PRIMARY)
	python3 permlinks.py install $(PRIMARY) $(INSTALL_DIR)

uninstall:
	python3 permlinks.py uninstall

clean:
	rm -f $(PRIMARY)

distclean: clean