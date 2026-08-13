# SSSD (System Security Services Daemon)

The [System Security Services Daemon (SSSD)](https://sssd.io/) is a Linux system service that manages user authentication, authorization, and identity data by connecting local systems to remote providers like Active Directory, LDAP, or FreeIPA. It improves system performance by caching credentials for offline authentication and reducing network load.

## Helpful Debugging Commands

``` shell
sudo sssctl domain-status your-domain.com
```

``` shell
sudo sssctl config-check
```

<!--
# Authors Notes

**Helpful Commands**
``` shell
sudo sssctl domain-status JCOOK3701.COM
```

``` shell
sudo sssctl config-check
```

-->

<!--
# Authors Notes:

Helpful files:

``` shell

/etc/pam.d/common-auth
```

Check SUDO Users
``` shell
LDAPTLS_REQCERT=never ldapsearch -x -H ldaps://modern-times.jcook3701.com:636 -b "ou=SUDOers,dc=jcook3701,dc=com" "(objectClass=sudoRole)"
```

Check Samba Users
``` shell
LDAPTLS_REQCERT=never ldapsearch -x -H ldaps://modern-times.jcook3701.com:636 -b "ou=People,ou=Users,dc=jcook3701,dc=com" "(objectClass=sambaSAMAccount)"
-->
