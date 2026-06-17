# setupcon

## Introduction

[Setupcon](https://manpages.debian.org/testing/console-setup/setupcon.1.en.html) is a Linux utility used to quickly configure the keyboard layout and console font on the virtual terminal (TTY). It applies settings defined in /etc/default/keyboard and /etc/default/console-setup.

[keyboard-configuration](https://wiki.debian.org/Keyboard) package in Debian handles the setup of system-wide keyboard layouts and properties. It provides a unified way to configure keyboards for both the Linux text console and the X Window / Wayland graphical environments, storing these preferences in /etc/default/keyboard

The [console-setup](https://manpages.debian.org/testing/console-setup/console-setup.5.en.html) console-setup package is a utility suite that configures the font, screen encoding, and layout of the virtual text consoles (TTYs). It ensures the system displays characters correctly and provides a comfortable typing experience when working directly with the Linux system rather than a graphical desktop.

### Authors Notes

1. This will only work on debian based operating systems.
