# OpenLDAP

OpenLDAP Software is an open source implementation of the Lightweight Directory Access Protocol.

## Acronyms

* Online Configuration (OLC)

## Authors Notes

### Roadmap

Look into updating project to utilize **slapd-smbk5pwd** as an option for system password management.
Currently kerberos is completely separate from ldap server and utilizes its own principal (database)
to store user keys.

``` shell
[ User ] ---> ( Changes Password via LDAP )
                     |
                     v
             [ OpenLDAP Server ]
                     |
         ( smbk5pwd Overlay Intercepts )
          /          |          \
         v           v           v
  [ Linux Hash ]  [ Samba Hash ]  [ Kerberos Keys ]
  (SSHA/Argon2)   (NTLM Hash)    (AES/DES Keys)
```

<!--

Authors Notes:

Phase 1: Server and Engine Configuration (The Settings Tier)01_config_bootstrap.ldif.j2 (Old: bootstrap_config.ldif.j2)Instantiates the blank cn=config offline engine schema skeleton.01_config_database.ldif.j2 (Old: db_config.ldif.j2)Provisions the active backend data store engine layout, root passwords, indices, and ACL rules.Phase 2: Directory Directory Initialization (The Core Data Tier)02_data_structure.ldif.j2 (Old: base_structure.ldif.j2)Deploys the static parent organizational containers (ou=Users, ou=Groups, ou=Computers).02_data_seed.ldif.j2 (Old: bootstrap_data.ldif.j2)Seeds the active structural network objects (bootstrap groups and human user profiles).Phase 3: Ecosystem Extensions and Node Integration (The Active Features Tier)03_feature_replication.ldif.j2 (Old: replication.ldif.j2)Sets node IDs and establishes consumer syncrepl sync pipelines.features/Holds the runtime plugin modules (sudo, ppolicy, samba) processed sequentially by your dynamic loop engine.ldap.conf.j2Kept exactly as it is. It maps cleanly as a standard client-side configuration file wrapper, separating itself from database manipulation actions.

Helpful commands:

``` shell
sudo sssctl domain-status jcook3701.com
```
-->
