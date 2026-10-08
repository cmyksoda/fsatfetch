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


# Hooks use shell builtins only: a helper missing from PATH would re-enter
# the hook for itself and fork-bomb the shell.
def posix_body(binary):
    words = ' '.join(SOURCES)
    return f'''    local src rest i
    for src in {words}; do
        [ "$1" = "$src" ] && continue
        [ "${{#1}}" -eq "${{#src}}" ] || continue
        rest=$1
        for (( i = 0; i < ${{#src}}; i++ )); do
            rest=${{rest/"${{src:i:1}}"/}}
        done
        if [ -z "$rest" ] && [ -x {binary} ]; then
            exec {binary}
        fi
    done
    printf '%s: command not found\\n' "$1" >&2
    return 127'''


def bash_block(binary):
    return f'''{MARK_BEGIN}
command_not_found_handle() {{
{posix_body(binary)}
}}
{MARK_END}
'''


def zsh_block(binary):
    return f'''{MARK_BEGIN}
command_not_found_handler() {{
{posix_body(binary)}
}}
{MARK_END}
'''


def fish_block(binary):
    words = ' '.join(SOURCES)
    return f'''{MARK_BEGIN}
function fish_command_not_found
    for src in {words}
        if test "$argv[1]" = "$src"; or test (string length -- "$argv[1]") -ne (string length -- $src)
            continue
        end
        set -l rest "$argv[1]"
        for c in (string split '' -- $src)
            set rest (string replace -- $c '' "$rest")
        end
        if test -z "$rest"; and test -x {binary}
            exec {binary}
        end
    end
    echo "$argv[1]: command not found" >&2
end
{MARK_END}
'''


def without_block(lines, replacement=''):
    out = []
    inside = False
    changed = False
    for line in lines:
        if MARK_BEGIN in line:
            inside = True
            changed = True
            out.append(replacement)
            continue
        if MARK_END in line:
            inside = False
            continue
        if not inside:
            out.append(line)
    return out, changed


def install_block(rc_path, block_text):
    rc_path = os.path.expanduser(rc_path)
    os.makedirs(os.path.dirname(rc_path), exist_ok=True)
    content = open(rc_path).read() if os.path.exists(rc_path) else ''
    if MARK_BEGIN in content:
        # Replacing in place lets a reinstall upgrade older, unsafe hooks.
        lines, _ = without_block(content.splitlines(keepends=True), block_text)
        open(rc_path, 'w').writelines(lines)
        print(f"  updated hook in {rc_path}")
        return
    with open(rc_path, 'a') as f:
        f.write('\n' + block_text)
    print(f"  installed hook in {rc_path}")


def remove_block(rc_path):
    rc_path = os.path.expanduser(rc_path)
    if not os.path.exists(rc_path):
        return
    lines, changed = without_block(open(rc_path).readlines())
    if changed:
        open(rc_path, 'w').writelines(lines)
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
