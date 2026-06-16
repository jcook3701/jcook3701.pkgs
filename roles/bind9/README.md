# [Bind9](https://wiki.debian.org/Bind9) DNS (Domain Name System)

BIND (Berkeley Internet Name Domain) is a complete, highly portable implementation of the Domain Name System (DNS) protocol.

## Debugging

Test main bind9 configuration file with the following command.  

``` shell
$ sudo named-checkconf
```

Testing **zone** files with the following:  

``` shell
$ sudo named-checkzone example.com /etc/bind/zones/db.example.zone
```
