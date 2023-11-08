#!/usr/bin/env python3


print('''
This script is no longer required, since Apple provided a sudo_local file in
Sonoma which allows custom entries to survive upgrades. There is even a
template file which has the required entry for TouchID sudo.

See:
https://sixcolors.com/post/2023/08/in-macos-sonoma-touch-id-for-sudo-can-survive-updates/

Note: if you use tmux, you may still want/need
https://github.com/fabianishere/pam_reattach
''')
