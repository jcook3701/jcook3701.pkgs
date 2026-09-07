# CUPS (Common UNIX Printing System)

[CUPS](https://openprinting.github.io/cups/) is the current standards-based, open source printing system developed by OpenPrinting for Linux® and other Unix®-like operating systems. CUPS uses IPP Everywhere™ to support printing to local and network printers.

## Project Utilization

### CUPS Server

Install and configure **CUPS** Server.

``` shell
$ ansible-playbook jcook3701.pkgs.cups.yml -K
```

### CUPS Client

Install and configure **CUPS** Client.

``` shell
$ ansible-playbook jcook3701.pkgs.cups.yml -K -e "cups_server=false"
```

### Uninstall CUPS

Uninstall **CUPS** Server/Client and remove configuration.

``` shell
$ ansible-playbook jcook3701.pkgs.cups.yml -K -e "cups_state=absent"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
