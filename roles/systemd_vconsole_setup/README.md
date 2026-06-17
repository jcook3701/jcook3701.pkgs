# systemd-vconsole-setup

[systemd-vconsole-setup](https://www.freedesktop.org/software/systemd/man/latest/systemd-vconsole-setup.service.html) is a systemd service and backend tool responsible for configuring and setting up the Linux virtual consoles (TTYs) during boot. It reads from the /etc/vconsole.conf file and applies your keyboard layouts (keymaps) and screen fonts by invoking loadkeys and setfont
