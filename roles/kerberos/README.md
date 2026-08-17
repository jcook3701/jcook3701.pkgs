# MIT Kerberos

[Kerberos](https://web.mit.edu/kerberos/) is a powerful network authentication protocol developed by MIT that uses secret-key cryptography to securely verify a user's or host's identity across an insecure network. It completely eliminates the need to send passwords over the wire, making it a foundational component of Single Sign-On (SSO) systems.

``` shell
  ┌────────────────────────────────────────────────────────┐
  │                   MASTER KDC SERVER                    │
  │                                                        │
  │   ┌───────────────────┐        ┌───────────────────┐   │
  │   │     krb5-kdc      │        │    krb5-init /    │   │
  │   │ (Authentication)  │        │   cron database   │   │
  │   └─────────▲─────────┘        └─────────┬─────────┘   │
  │             │                            │             │
  │             │ Reads                      │ Runs kprop  │
  │             │                            ▼             │
  │      ┌──────┴────────────────────────────┴──────┐      │
  │      │       Master Kerberos Database           │      │
  │      │       (/var/lib/krb5kdc/principal)       │      │
  │      └──────▲───────────────────────────────────┘      │
  │             │                                          │
  │             │ Modifies                                 │
  │   ┌─────────┴─────────┐                                │
  │   │    krb5-admin     │                                │
  │   │    (kadmind)      │                                │
  │   └─────────▲─────────┘                                │
  └─────────────┼────────────────────────────┼─────────────┘
                │                            │
  Admin Request │ (kadmin)                   │ Database Push
                │                            │ (Port 754)
                │                            ▼
  ┌─────────────┴─────────┐    ┌───────────────────────────┐
  │     CLIENT NODE       │    │    REPLICA KDC SERVER     │
  │                       │    │                           │
  │  Runs: kinit / sssd   │    │   ┌───────────────────┐   │
  │  Requests Auth Tickets│    │   │    krb5-kpropd    │   │
  │  From Port 88         │    │   │ (Listens for Master)  │   │
  │                       │    │   └─────────┬─────────┘   │
  └─────────────┬─────────┘    │             │             │
                │              │             ▼ Writes      │
                └──────────────┼────────►┌───────────────┐ │
                 Auth Request  │         │ Read-Only DB  │ │
                 (Port 88)     │         └───────────────┘ │
                               │         ┌───────────────┐ │
                               │         │   krb5-kdc    │ │
                               │         │(Auth Fallback)│ │
                               │         └───────────────┘ │
                               └───────────────────────────┘
```

## Authors Notes

### Roadmap

Potential **default/main.yml** additions:

* TODO: Add feature in mit kerberos setup for **krb5-kdc-ldap**
  * This will require update to to ldap role to add kerberos ldif schema injection.
  * Different ldap schemas are required depending on backend selection (mit, heimdal)

``` yml
kerberos_implementation: "mit" # Options: "mit" or "heimdal"

# Database storage choice: "file" or "ldap"
# Controls whether MIT installs its plugin, and which schema file gets selected
kerberos_database_backend: "file"

# OpenLDAP configuration parameters (Only parsed if backend == "ldap")
kerberos_ldap_server_uri: "ldaps://://example.com"
kerberos_ldap_base_dn: "dc=example,dc=com"

# Password synchronization helper toggle
# (Only valid if kerberos_implementation == "heimdal" AND kerberos_database_backend == "ldap")
kerberos_enable_smbk5pwd_overlay: false
```

Future Package definitions update within **vars/debian.yml**:

``` yml
# MIT Package Declarations
kerberos_os_mit_client_pkgs:
  - krb5-user
kerberos_os_mit_server_pkgs:
  - krb5-kdc
  - krb5-admin-server
kerberos_os_mit_replica_pkgs:
  - krb5-kdc
  - krb5-kpropd
kerberos_os_mit_ldap_pkgs:
  - krb5-kdc-ldap

# Heimdal Package Declarations
kerberos_os_heimdal_client_pkgs:
  - heimdal-clients
  - heimdal-kcm
  - libkrb5-25-heimdal
kerberos_os_heimdal_server_pkgs:
  - heimdal-kdc
kerberos_os_heimdal_replica_pkgs:
  - heimdal-kdc
kerberos_os_heimdal_ldap_pkgs: []


```

future package switch in **vars/main.yml**:

``` yml
# The primary list evaluated by future package installation tasks
kerberos_pkg_names: >-
  {{
    _kerberos_pkg_names_override | default(
      (vars['kerberos_os_' ~ kerberos_implementation ~ '_server_pkgs'] + vars['kerberos_os_' ~ kerberos_implementation ~ '_client_pkgs'] + (vars['kerberos_os_' ~ kerberos_implementation ~ '_ldap_pkgs'] if kerberos_database_backend == 'ldap' else [])) if kerberos_node_type == 'master' else
      (vars['kerberos_os_' ~ kerberos_implementation ~ '_replica_pkgs'] + vars['kerberos_os_' ~ kerberos_implementation ~ '_client_pkgs'] + (vars['kerberos_os_' ~ kerberos_implementation ~ '_ldap_pkgs'] if kerberos_database_backend == 'ldap' else [])) if kerberos_node_type == 'replica' else
      vars['kerberos_os_' ~ kerberos_implementation ~ '_client_pkgs']
    )
  }}

# Maybe use this to call ldap role to inject correct schema.  otherwise this should be handled
#   in the openldap role with the info passed in correctly via the orchestration layer.
# Dynamic Schema Path Selector
# Points to the exact schema path required based on user configuration
kerberos_ldap_schema_source: >-
  {{
    'files/schemas/mit-kerberos.ldif' if kerberos_implementation == 'mit' else
    'files/schemas/heimdal-kerberos.ldif'
  }}


```

<!--
# Authors Notes Semi-Hidden:

Helpful Google AI chats:

-->
