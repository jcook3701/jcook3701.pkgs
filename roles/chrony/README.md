# NTP (Network Time Protocol) with Chrony

NTP (Network Time Protocol), a networking protocol used to synchronize the clocks of computers and other devices across a data network to within milliseconds of Coordinated Universal Time (UTC).  

## Role Variables

| Variable | Default Value | Type | Choices / Elements | Description |
| :--- | :--- | :--- | :--- | :--- |
| `chrony_state` | `present` | String | `present`, `absent`, `teardown` | Controls the lifecycle state of the Chrony service and package. |
| `chrony_is_server` | `false` | Boolean | `true`, `false` | Controls whether this host acts as an NTP server for other clients. |
| `chrony_enable_nts` | `false` | Boolean | `true`, `false` | Enables Network Time Security (NTS) for secure upstream time synchronization. |
| `chrony_upstream_servers` | `[]` | List | Strings (IPs / FQDNs) | A list of upstream NTP servers or NTS-enabled endpoints to sync time from. |
| `chrony_allow_networks` | `[]` | List | Strings (Subnets / CIDRs) | A list of subnets or IP ranges allowed to query this Chrony server (used when `chrony_is_server` is `true`). |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes:

## Playbook Utilization

Install and configure **Chrony** NTP server.

``` shell
$ ansible-playbook jcook3701.pkgs.chrony.yml -K
```

Uninstall **Chrony** Server and remove configuration.

``` shell
$ ansible-playbook jcook3701.pkgs.chrony.yml -K -e "chrony_state=absent"
```
-->
