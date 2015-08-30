# Gedit Plugin: Open Friends
A gedit 3 plugin that opens the respective header for a C/C++ source file and vice versa

---

## Installation

*For your account only:*

Copy `OpenFriends.p*` to
- `~/.local/share/gedit/plugins/` (create directory if necessary)


*For all accounts:*

Depending on your system, copy `OpenFriends.p*` to
- `/usr/lib/gedit/plugins/` or
- `/usr/lib/i386-linux-gnu/gedit/plugins/` or
- `/usr/lib/x86_64-linux-gnu/gedit/plugins/`


Depending on the version of gedit, subfolders are also taken into account.
Thus, you can clone this repository directly into one of the above folders...


## Usage

Activate in `Edit->Preferences->Plugins`

Use from menu entry in `Tools` or via the keyboard shortcut Ctrl+Alt+O.


## Troubleshooting

In case activating the plugin in the preferences leads to the `Plugin loader 'python3' was not found` error (the icon changes, hovering the cursor over it shows the error), open `OpenFriends.plugin`, change the `Loader` line from `python3` to `python`, and retry.

