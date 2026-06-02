# NTP (Network Time Protocol) with Chrony

NTP (Network Time Protocol), a networking protocol used to synchronize the clocks of computers and other devices across a data network to within milliseconds of Coordinated Universal Time (UTC).  

Install and configure **Chrony** NTP server.

``` shell
$ ansible-playbook jcook3701.pkgs.chrony.yml -K
```

Uninstall **Chrony** Server and remove configuration.

``` shell
$ ansible-playbook jcook3701.pkgs.chrony.yml -K -e "chrony_state=absent"
```
