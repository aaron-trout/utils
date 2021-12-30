#!/usr/bin/env python3

'''
This script detects if there are missing entries in /etc/pam.d/sudo, as
defined in REQUIRED_ENTRIES. By default it will add pam_reattach and pam_tid
such that TouchID can be used for sudo authentication.

The pam_reattach module allows use of TouchID inside tmux, install it with:

    brew install fabianishere/personal/pam_reattach

The script will only detect if changes are required, unless the '--patch' flag
is passed. Call it from your .bashrc/.zshrc with no args and it will let you
know if changes are required.

Requires Python 3.6+ (tested on Python 3.9.9).
'''

from collections import OrderedDict
from pathlib import Path
import sys

PAM_FILE = Path('/etc/pam.d/sudo')
PAM_MODULES_DIR = Path('/usr/lib/pam')

# Entries must be ordered correctly (monotonic line numbers)
REQUIRED_ENTRIES = OrderedDict([  # ( line number, line contents )
    (1, 'auth       optional       /opt/homebrew/lib/pam/pam_reattach.so'),
    (2, 'auth       sufficient     pam_tid.so'),
])


def pam_needs_patching(contents):
    lines = contents.splitlines()
    for line_number, line_content in REQUIRED_ENTRIES.items():
        if lines[line_number] != line_content:
            return True
    return False


def patch(contents):
    lines = contents.splitlines()
    for line_number, line_content in REQUIRED_ENTRIES.items():
        if lines[line_number] != line_content:
            lines.insert(line_number, line_content)
    return '\n'.join(lines) + '\n'


def print_indented(string, n=1):
    for line in string.splitlines():
        print('\t' * n, line)


def print_changes(old, new):
    print('Old contents:')
    print_indented(old)
    print()
    print('New contents:')
    print_indented(new_contents)
    print()


def check_module(module):
    'Returns True if the given PAM module exists, else False.'
    if module.startswith('/'):
        return Path(module).exists()

    return (PAM_MODULES_DIR / f'{module}.2').exists()


def check_modules(contents):
    ok = True
    for line in contents.splitlines():
        if line.strip().startswith('#'):
            continue

        module = line.split()[2]
        if not check_module(module):
            print(f'ERROR: {module} not found')
            ok = False
    return ok


if __name__ == '__main__':
    with open(PAM_FILE) as f:
        contents = f.read()

    needs_patching = pam_needs_patching(contents)
    if needs_patching:
        print(f'{PAM_FILE!s} needs patching, run:')
        print_indented('sudo ' + ' '.join(sys.argv) + ' --patch')

    if (not needs_patching) or (len(sys.argv) < 2 or sys.argv[1] != '--patch'):
        sys.exit(0)

    print(f'Patching {PAM_FILE!s}...')

    new_contents = patch(contents)
    ok = check_modules(new_contents)
    print_changes(contents, new_contents)

    if not ok:
        print('Aborting: one or modules not found')
        sys.exit(1)

    if input('Enter "yes" to continue: ') != 'yes':
        sys.exit(1)

    with open(PAM_FILE, 'w') as f:
        f.write(new_contents)
