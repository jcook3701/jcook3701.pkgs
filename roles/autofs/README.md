# Autofs

[Autofs](https://docs.kernel.org/filesystems/autofs.html) is a system tool for Unix and Linux that automatically mounts and unmounts filesystems on demand. Key components include the autofs kernel module, the automount daemon, and configuration maps. It saves system resources by only connecting to network shares or drives when you try to use them, and disconnecting them after a set time of no activity.

## Authors Notes

### Helpful Debugging Commands

``` shell
sudo /usr/sbin/automount -m
```

``` shell
sudo mount -t cifs //hostname.example.com /mnt -o sec=krb5,vers=3.11,multiuser
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# Authors Notes:

-->
