#!/usr/bin/env python3
"""
hooks.py — install/uninstall fsatfetch via shell "command not found" hooks
no symlinks, no PATH changes.
"""

import os, sys

SOURCES  = ['fastfetch', 'neofetch', 'pfetch', 'qwqfetch', 'hyfetch']
MARK_BEGIN = '# fsatfetch hook >>>'
MARK_END   = '# fsatfetch hook <<<'

RC_BASH = '~/.bashrc'
RC_ZSH  = '~/.zshrc'
RC_FISH = '~/.config/fish/config.fish'


def bash_block(binary):
    words = ' '.join(SOURCES)
    return f'''{MARK_BEGIN}
command_not_found_handle() {{
    local word sorted src ssorted
    word=$(printf '%s' "$1" | fold -w1 | sort | tr -d '\\n')
    for src in {words}; do
        [ "$1" = "$src" ] && continue
        ssorted=$(printf '%s' "$src" | fold -w1 | sort | tr -d '\\n')
        if [ "$word" = "$ssorted" ]; then
            exec {binary}
        fi
    done
    printf '%s: command not found\\n' "$1" >&2
    return 127
}}
{MARK_END}
'''


def zsh_block(binary):
    words = ' '.join(SOURCES)
    return f'''{MARK_BEGIN}
command_not_found_handler() {{
    local word sorted src ssorted
    word=$(printf '%s' "$1" | fold -w1 | sort | tr -d '\\n')
    for src in {words}; do
        [ "$1" = "$src" ] && continue
        ssorted=$(printf '%s' "$src" | fold -w1 | sort | tr -d '\\n')
        if [ "$word" = "$ssorted" ]; then
            exec {binary}
        fi
    done
    printf '%s: command not found\\n' "$1" >&2
    return 127
}}
{MARK_END}
'''


def fish_block(binary):
    words = ' '.join(SOURCES)
    return f'''{MARK_BEGIN}
function fish_command_not_found
    set -l word (string split '' -- $argv[1] | sort | string join '')
    for src in {words}
        if test "$argv[1]" = "$src"
            continue
        end
        set -l ssrc (string split '' -- $src | sort | string join '')
        if test "$word" = "$ssrc"
            exec {binary}
        end
    end
    echo "$argv[1]: command not found" >&2
end
{MARK_END}
'''


def install_block(rc_path, block_text):
    rc_path = os.path.expanduser(rc_path)
    os.makedirs(os.path.dirname(rc_path), exist_ok=True)
    content = open(rc_path).read() if os.path.exists(rc_path) else ''
    if MARK_BEGIN in content:
        print(f"  {rc_path} already has a hook, skipping")
        return
    with open(rc_path, 'a') as f:
        f.write('\n' + block_text)
    print(f"  installed hook in {rc_path}")


def remove_block(rc_path):
    rc_path = os.path.expanduser(rc_path)
    if not os.path.exists(rc_path):
        return
    lines = open(rc_path).readlines()
    out = []
    inside = False
    changed = False
    for line in lines:
        if MARK_BEGIN in line:
            inside = True
            changed = True
            continue
        if MARK_END in line:
            inside = False
            continue
        if not inside:
            out.append(line)
    if changed:
        open(rc_path, 'w').writelines(out)
        print(f"  removed hook from {rc_path}")


def cmd_install(binary):
    binary = os.path.expanduser(binary)
    if not os.path.isfile(binary):
        print(f"  warning: {binary} doesn't exist (installing hook anyway)")

    print("installing shell hooks...")
    install_block(RC_BASH, bash_block(binary))
    install_block(RC_ZSH, zsh_block(binary))
    install_block(RC_FISH, fish_block(binary))

    print("\nrestart your shell, or source the relevant rc file, to activate.")
    print("no PATH changes, no symlinks — misspelled commands are caught")
    print("by your shell's command-not-found hook.")


def cmd_uninstall():
    print("removing shell hooks...")
    for rc in (RC_BASH, RC_ZSH, RC_FISH):
        remove_block(rc)
    print("  done")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''

    if cmd == 'install' and len(sys.argv) == 3:
        cmd_install(sys.argv[2])
    elif cmd == 'uninstall':
        cmd_uninstall()
    else:
        print("usage:")
        print(f"  {sys.argv[0]} install <path-to-binary>")
        print(f"  {sys.argv[0]} uninstall")
        sys.exit(1)