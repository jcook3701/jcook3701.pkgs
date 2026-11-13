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

## Role Variable Reference Matrix

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`kerberos_state`** | Targeted structural installation state (`present` or `absent`). | `"present"` |
| **`kerberos_node_type`** | Cluster infrastructure deployment profile (`master`, `replica`, or `client`). | `"client"` |
| **`kerberos_admin_servers`** | Topology inventory array defining primary KDC administrative master servers. | `[]` |
| **`kerberos_replica_servers`** | Topology inventory array defining backend incremental propagation replica servers. | `[]` |
| **`kerberos_client_nodes`** | Generic baseline fallback array for standard workstation client nodes. | `[]` |
| **`kerberos_samba_file_servers`** | Infrastructure array listing backend nodes running the active Samba file server daemons. | `[]` |
| **`kerberos_nfs_file_servers`** | Infrastructure array listing backend nodes running the active NFS storage server daemons. | `[]` |
| **`kerberos_http_servers`** | Infrastructure array listing backend nodes running secure HTTP web server processes. | `[]` |
| **`kerberos_ldap_servers`** | Infrastructure array listing backend nodes running structural directory services servers. | `[]` |
| **`kerberos_samba_client_nodes`** | Dedicated client deployment vector listing hostnames requiring isolated Samba service keytabs. | `[]` |
| **`kerberos_nfs_client_nodes`** | Dedicated client deployment vector listing hostnames requiring isolated NFS service keytabs. | `[]` |
| **`kerberos_http_client_nodes`** | Dedicated client deployment vector listing hostnames requiring isolated HTTP service keytabs. | `[]` |
| **`kerberos_ldap_client_nodes`** | Dedicated client deployment vector listing hostnames requiring isolated LDAP service keytabs. | `[]` |
| **`kerberos_port`** | Network daemon port binding for primary ticket granting service authentication exchanges. | `"88"` |
| **`kerberos_admin_port`** | Network daemon port binding for administrative database update traffic. | `"749"` |
| **`kerberos_admin_bind_all`** | Controls whether administrative interfaces listen on all network interfaces (`"true"` or `"false"`). | `"true"` |
| **`kerberos_iprop_enable`** | Toggles activation of the master-to-replica incremental database propagation system (`"true"` or `"false"`). | `"true"` |
| **`kerberos_iprop_port`** | Network daemon port binding for active backend database synchronization streams. | `"754"` |
| **`kerberos_iprop_replica_poll`** | Polling interval defining how often replicas query the master KDC for differential log serial numbers. | `"2m"` |
| **`kerberos_admin_user`** | Administrative superuser account identifier utilized to hook and adjust database principal layouts. | `"kadmin"` |
| **`kerberos_admin_password`** | Administrative superuser password token string utilized during cluster bootstrapping. | `"SecretPassword123"` |
| **`kerberos_use_stash_file`** | Instructs the KDC daemon whether to initialize and use a local master database encryption key stash file. | `true` |
| **`kerberos_policy_min_length`** | Minimum character constraint enforced across password structures created on the KDC. | `8` |
| **`kerberos_policy_min_classes`** | Minimum character composition class constraint enforced across generated passwords. | `3` |
| **`kerberos_policy_history_num`** | Total generation history depth tracking constraint enforced to prevent password reuse loops. | `5` |
| **`kerberos_top_level_domain`** | Top-level domain suffix marker utilized to establish core cluster identity. | `"com"` |
| **`kerberos_second_level_domain`** | Organizational domain string utilized to establish core cluster identity. | `"example"` |
| **`kerberos_domain_name`** | Dynamic compiled fully qualified organizational domain name string. | `"{{ kerberos_second_level_domain }}.{{ kerberos_top_level_domain }}"` |
| **`kerberos_realm`** | Dynamic compiled upper-case global Kerberos security structural administrative realm identity string. | `"{{ kerberos_domain_name \| upper }}"` |
| **`kerberos_dns_lookup_realm`** | Configures whether client processes fall back to DNS lookups to identify target realm spaces. | `"false"` |
| **`kerberos_dns_lookup_kdc`** | Configures whether client processes fall back to DNS SRV records to discover active KDC instances. | `"false"` |
| **`kerberos_ticket_lifetime`** | Default maximum active validity lifetime duration applied to generated ticket granting tickets. | `"24h"` |
| **`kerberos_renew_lifetime`** | Default maximum renewable extension duration limit allowed across active client user tickets. | `"7d"` |
| **`kerberos_forwardable`** | Dictates whether user ticket granting tickets can be forwarded to separate network client nodes natively. | `"true"` |
| **`kerberos_max_clock_skew`** | Maximum allowed execution time variance offset permitted during cryptographic packet evaluation loops. | `"5m"` |
| **`kerberos_dns_canonicalize_hostname`** | Directs clients whether to run reverse DNS queries to resolve canonical server host identities safely. | `"true"` |
| **`kerberos_rdns`** | Dictates whether reverse DNS lookups are preferred when building principal target headers over transport sockets. | `"true"` |
| **`kerberos_encryption_types`** | Cryptographic algorithm preference array utilized during local master KDC database initialization steps. | `["aes256-cts-hmac-sha1-96", "aes128-cts-hmac-sha1-96"]` |
| **`kerberos_permitted_enctypes`** | Allowed encryption type array permitted within incoming transmission payloads hitting the server. | `["aes256-cts-hmac-sha1-96", "aes128-cts-hmac-sha1-96"]` |
| **`kerberos_default_tgs_enctypes`** | Session key cryptography type selection defaults applied to standard Ticket Granting Server requests. | `["aes256-cts-hmac-sha1-96", "aes128-cts-hmac-sha1-96"]` |
| **`kerberos_default_tkt_enctypes`** | Session key cryptography type selection defaults applied to standard authentication service requests. | `["aes256-cts-hmac-sha1-96", "aes128-cts-hmac-sha1-96"]` |
| **`kerberos_client_auto_register_host`** | Controls whether individual client nodes execute an active self-registration sequence on the master KDC. | `"true"` |
| **`kerberos_bootstrap_users`** | Core seeding array structure utilized to register baseline user profiles into the database upon setup. | *(Complex User Definition Array)* |
| **`kerberos_domain_realms`** | Local domain-to-realm map rules utilized to direct network traffic into the appropriate security zone. | *(Dynamic Realm Mapping List)* |
| **`kerberos_realms`** | Fallback realm server tracking structure utilized when parent infrastructure variables collapse. | *(Dynamic Server Failover List)* |

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

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# Authors Notes Semi-Hidden:

Helpful Google AI chats:

-->
