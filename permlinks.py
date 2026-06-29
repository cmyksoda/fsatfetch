#!/usr/bin/env python3
"""
permlinks.py — install/uninstall fsatfetch with all permutation symlinks
"""

from itertools import permutations
import json, os, sys

SOURCES  = ['fastfetch', 'neofetch', 'pfetch', 'qwqfetch', 'hyfetch']
MANIFEST = os.path.expanduser('~/.fsatfetch_manifest.json')
PATH_TAG = '# added by fsatfetch'
RC_POSIX = ['~/.bashrc', '~/.zshrc', '~/.profile']
RC_FISH  = '~/.config/fish/config.fish'


def all_perms():
    seen = set()
    for word in SOURCES:
        for p in permutations(word):
            seen.add(''.join(p))
    return seen


def add_to_path(install_dir):
    shell = os.environ.get('SHELL', '')
    rcs   = [os.path.expanduser(r) for r in RC_POSIX
             if os.path.exists(os.path.expanduser(r))]
    fish  = os.path.expanduser(RC_FISH)

    if 'fish' in shell and os.path.exists(fish):
        rcs.append(fish)

    if not rcs:
        rcs.append(os.path.expanduser('~/.profile'))

    for rc in rcs:
        try:
            content = open(rc).read() if os.path.exists(rc) else ''
            if install_dir in content:
                print(f"  {rc} already has PATH entry, skipping")
                continue
            line = (
                f'\nset -gx PATH "{install_dir}" $PATH  {PATH_TAG}\n'
                if 'fish' in rc else
                f'\nexport PATH="{install_dir}:$PATH"  {PATH_TAG}\n'
            )
            with open(rc, 'a') as f:
                f.write(line)
            print(f"  added to PATH in {rc}")
        except Exception as e:
            print(f"  warning: couldn't write {rc}: {e}")

    print(f"\n  restart shell or run:")
    print(f'    export PATH="{install_dir}:$PATH"')


def remove_from_path():
    for rc in RC_POSIX + [RC_FISH]:
        exp = os.path.expanduser(rc)
        if not os.path.exists(exp):
            continue
        try:
            lines    = open(exp).readlines()
            filtered = [l for l in lines if PATH_TAG not in l]
            if len(filtered) < len(lines):
                open(exp, 'w').writelines(filtered)
                print(f"  removed PATH entry from {rc}")
        except Exception as e:
            print(f"  warning: couldn't clean {rc}: {e}")


def cmd_install(binary, install_dir):
    install_dir = os.path.expanduser(install_dir)
    os.makedirs(install_dir, exist_ok=True)

    perms   = all_perms()
    created = []
    skipped = 0

    print(f"creating {len(perms):,} symlinks in {install_dir}...")
    for perm in perms:
        if perm == binary or perm in SOURCES:
            continue  # skip the actual binary AND the correctly spelled original commands
        link = os.path.join(install_dir, perm)
        try:
            if os.path.lexists(link):
                os.remove(link)
            os.symlink(binary, link)  # relative symlink to binary in same dir
            created.append(link)
        except Exception as e:
            print(f"  warning: {perm}: {e}")
            skipped += 1

    with open(MANIFEST, 'w') as f:
        json.dump({
            'binary':      binary,
            'install_dir': install_dir,
            'links':       created,
        }, f)

    print(f"  done — {len(created):,} created, {skipped} skipped")
    print("\nadding to PATH...")
    add_to_path(install_dir)


def cmd_uninstall():
    if not os.path.exists(MANIFEST):
        print("no manifest found — nothing to uninstall")
        sys.exit(1)

    data        = json.load(open(MANIFEST))
    install_dir = data.get('install_dir', '')
    links       = data.get('links', [])
    binary      = data.get('binary', '')
    removed     = 0

    print(f"removing {len(links):,} symlinks...")
    for link in links:
        try:
            if os.path.lexists(link):
                os.remove(link)
                removed += 1
        except Exception as e:
            print(f"  warning: {link}: {e}")

    # remove the binary itself
    if binary and install_dir:
        bin_path = os.path.join(install_dir, binary)
        if os.path.exists(bin_path):
            os.remove(bin_path)

    # remove dir if now empty
    if install_dir:
        try:
            os.rmdir(install_dir)
            print(f"  removed {install_dir}")
        except OSError:
            print(f"  note: {install_dir} not empty, left in place")

    os.remove(MANIFEST)
    print(f"  done — {removed:,} symlinks removed")
    print("\ncleaning PATH entries...")
    remove_from_path()


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''

    if cmd == 'install' and len(sys.argv) == 4:
        cmd_install(sys.argv[2], sys.argv[3])
    elif cmd == 'uninstall':
        cmd_uninstall()
    else:
        print("usage:")
        print(f"  {sys.argv[0]} install <binary> <install_dir>")
        print(f"  {sys.argv[0]} uninstall")
        sys.exit(1)