# Samaba

[Samba](https://www.samba.org/) is the most feature-rich Open Source implementation of the SMB and Active Directory protocols for Linux and UNIX-like systems.

``` shell
$ sudo apt install samba samba-common-bin
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# Authors Notes:

sudo tail -n 50 /var/log/samba/log.localhost
sudo journalctl -u smbd --no-pager -n 50

**Helpful commands** for testing **samba** configuration files.

``` shell
$ testparm /etc/samba/smb.conf
```

``` shell
$ smbclient -L <hostname> -k
```
```
wbinfo --name-to-sid "JCOOK3701\Domain Users"
```

``` shell
wbinfo --sid-to-gid $(wbinfo --name-to-sid "JCOOK3701\Domain Users"
```

``` shell
sudo net sam show "jcook3701\pxeuser"
```


TODO:
If you need multiple Active Directory servers for redundancy or scale, you use one of these two standard configurations:

    * Additional/Secondary Domain Controller: You provision a second Samba machine using samba_deployment_mode: "addc", but instead of provisioning a fresh domain, you join it to your existing domain as an Additional DC. Both machines will replicate the database, and if one dies, the other keeps the network alive.  
    * Domain Member File/Print Server: You provision a machine using samba_deployment_mode: "member_sssd". It joins the AD domain managed by your addc and acts as a dedicated file share worker, offloading resource traffic from your domain controllers.  

TODO: Test Samba Client code.  Using autofs for samba mounts so it's on the back burner.

    Planning for the future now by locking down a clean, modern SSSD + Kerberos Member Server.

    Since there are no Windows clients yet, setting this up as a flexible third option gives full architecture options later. If future Windows clients use tools like MIT Kerberos for Windows or we set up a Cross-Forest Trust down the road, they will get seamless Single Sign-On (SSO) directly through this pipeline

    # 1. Establish Server Role (Not a DC)
    server role = member server
    security = user

    # 2. Bind to external Kerberos Realm
    realm = YOUR-KERBEROS-REALM.COM
    kerberos method = system keytab

    # 3. Connect to your OpenLDAP Server
    passdb backend = ldapsam:ldap://://yourdomain.com
    ldap suffix = dc=yourdomain,dc=com
    ldap user suffix = ou=People
    ldap group suffix = ou=Groups
    ldap admin dn = cn=admin,dc=yourdomain,dc=com

    # 4. ID Mapping for Linux/Windows compatibility
    idmap config * : backend = tdb
    idmap config * : range = 3000-7999
    idmap config YOURDOMAIN : backend = ldap
    idmap config YOURDOMAIN : range = 10000-99999

    {% if share.comment is defined %}comment = {{ share.comment }}{% endif %}
    path = {{ share.path }}
    {% if share.public is defined %}public = {{ share.public }}{% endif %}
    {% if share.valid_users is defined %}valid users = {{ share.valid_users }}{% endif %}
    {% if share.force_user is defined %}force user = {{ share.force_user }}{% endif %}
    {% if share.force_group is defined %}force group = {{ share.force_group }}{% endif %}
    {% if share.read_only is defined %}read only = {{ share.read_only }}{% endif %}
    {% if share.writable is defined %}writable = {{ share.writable }}{% endif %}
    {% if share.browsable is defined %}browseable = {{ share.browsable }}{% endif %}
    {% if share.guest_ok is defined %}guest ok = {{ share.guest_ok }}{% endif %}
    {% if share.create_mask is defined %}create mask = {{ share.create_mask }}{% endif %}
    {% if share.force_create_mode is defined %}force create mode = {{ share.force_create_mode }}{% endif %}
    {% if share.directory_mask is defined %}directory mask = {{ share.directory_mask }}{% endif %}
    {% if share.force_directory_mode is defined %}force directory mode = {{ share.force_directory_mode }}{% endif %}

    old smb cfg settings for nt4_pdc:

    winbind max domain connections = 10
    winbind enum users = yes
    winbind enum groups = yes
    winbind use default domain = yes
    winbind nested groups = yes
-->
