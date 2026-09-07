# Webmin

[Webmin](https://webmin.com/) is an open-source, web-based control panel designed for the system administration of Unix-like systems, such as Linux, FreeBSD, and Solaris. It allows you to manage server internals through a browser-based interface, eliminating the need to manually edit configuration files via the command line.

## Role Variables

| Variable | Default Value | Type | Description |
| :--- | :--- | :--- | :--- |
| `webmin_state` | `present` | String | Controls the lifecycle execution state for Webmin. Valid choices are `present` or `absent`. |
| `webmin_repo_url` | `https://raw.githubusercontent.com/webmin/webmin/master/webmin-setup-repos.sh` | String | The remote endpoint used to download the official Webmin repository configuration script. |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
Helpful links:
    * https://reintech.io/blog/configure-secure-ftp-server-vsftpd-debian-12
-->
