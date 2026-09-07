# SSSD (System Security Services Daemon)

The [System Security Services Daemon (SSSD)](https://sssd.io/) is a Linux system service that manages user authentication, authorization, and identity data by connecting local systems to remote providers like Active Directory, LDAP, or FreeIPA. It improves system performance by caching credentials for offline authentication and reducing network load.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `sssd_state` | The intended configuration state of the SSSD client infrastructure. Choices: `present`, `absent`, `teardown`. | `"present"` |
| `sssd_daemon_opts` | Additional runtime flags and arguments passed directly to the main sssd daemon startup process. Use "-D" to run as a daemon and "-f" to force interactive/interactive behavior configurations. | `"-D -f"` |
| `sssd_debug_logger` | Determines where the internal SSSD engine sends its operational logs and deep diagnostic matrices. Selecting 'files' routes output to /var/log/sssd/, while 'journald' integrates directly with the systemd event logging rings. <br>Choices: `files`, `journald`, `stderr` | `"journald"` |
| `sssd_responder_activation_method` | Controls the architecture style used to trigger SSSD sub-responders (autofs, ssh, sudo, kcm, pac). Set to 'socket' for modern on-demand systemd socket activation. Set to 'service' for high-frequency or legacy resident background daemons. <br>Choices: `socket`, `service` | `"socket"` |
| `sssd_enable_nss` | Toggles the Name Service Switch (NSS) responder loop for system identity maps (passwd, group, netgroup). | `true` |
| `sssd_enable_pam` | Toggles advanced SSSD responder loop configuration for system-wide Pluggable Authentication Modules (PAM). | `false` |
| `sssd_enable_autofs` | Toggles dynamic network storage mounting capabilities via the autofs daemon connection pipe. | `true` |
| `sssd_enable_ssh` | Toggles centralized key authorization retrieval filters for secure SSH access control rules. | `true` |
| `sssd_enable_sudo` | Toggles centralized directory-driven root authorization rule caching models. | `true` |
| `sssd_enable_kdc` | Enables or disables SSSD locator plugin integration to help clients dynamically find Kerberos Key Distribution Centers (KDCs). | `true` |
| `sssd_enable_pac` | Controls whether SSSD processes and validates Active Directory Privilege Attribute Certificate (PAC) data for Kerberos tickets. | `true` |
| `sssd_enable_ifp` | Enables the InfoPipe D-Bus interface responder to expose identities to external applications. | `true` |
| `sssd_id_provider` | The primary identity provider backend used for pulling user and group metadata. | `"ldap"` |
| `sssd_auth_provider` | The primary authentication provider backend used for validating user passwords. | `"krb5"` |
| `sssd_chpass_provider` | The backend provider used for handling user password change operations. | `"krb5"` |
| `sssd_access_provider` | The access control provider used for enforcing system login permissions. | `"ldap"` |
| `sssd_autofs_provider` | The provider backend used for retrieving automount maps and path locations. | `"ldap"` |
| `sssd_sudo_provider` | The provider backend used for fetching centralized sudoers security rules. | `"ldap"` |
| `sssd_krb5_validate` | Toggles mutual authentication routines against the KDC using local machine host keytabs. | `true` |
| `sssd_cache_credentials` | Toggles local offline caching capabilities for credential access during infrastructure drops. | `true` |
| `sssd_krb5_store_password_if_offline` | Enables secure localized caching of user passwords when the Active Directory or Kerberos KDC network is offline. | `true` |
| `sssd_top_level_domain` | The primary internet routing suffix component (e.g., net, org, com). | `"com"` |
| `sssd_second_level_domain` | The main company organizational domain text label string handle. | `"example"` |
| `sssd_domain_name` | The dynamically constructed full corporate domain name string. | `"{{ sssd_second_level_domain }}.{{ sssd_top_level_domain }}"` |
| `sssd_ldap_users_parent_ou` | The parent organizational unit branch container identifier for all directory users. | `"Users"` |
| `sssd_ldap_people_child_ou` | The precise nested sub-container tracking human user accounts. | `"People"` |
| `sssd_ldap_groups_ou` | The safety group container tracking group listings. | `"Group"` |
| `sssd_ldap_sudoers_ou` | The container storing centralized sudo permissions rules. | `"SUDOers"` |
| `sssd_ldap_automount_ou` | The container branch managing autofs network path shares maps. | `"AutoMount"` |
| `sssd_ldap_protocol` | The underlying transmission layer encryption architecture model deployed. Choices: `ldap`, `ldaps`. | `"ldaps"` |
| `sssd_ldap_tls` | Forces TLS validation routines over communication sockets. | `true` |
| `sssd_manage_ldap_keys` | Controls whether the role should actively collect, deploy and manage LDAP TLS certificates and private cryptographic keys on the system. | `false` |
| `sssd_ldap_servers` | **(Required)** An array of fully qualified domain names mapping to active identity directory cluster pools. | *Mandatory* |
| `sssd_krb5_servers` | **(Required)** An array of fully qualified domain names mapping to targeted verification realm key distribution centers. | *Mandatory* |
| `sssd_ldap_sasl_mech` | The Simple Authentication and Security Layer (SASL) mechanism used for secure GSSAPI Kerberos directory binding. | `"GSSAPI"` |
| `sssd_ldap_user_principal` | Controls User Principal Name (UPN) evaluation behavior, forcing raw string matches without string substitution. | `"nosubst"` |
| `sssd_debug_level` | Global diagnostics logging level for the primary SSSD daemon engine. | `7` |
| `sssd_pam_debug_level` | Diagnostics logging level for the PAM validation module responder subsystem. | `10` |
| `sssd_autofs_debug_level` | Diagnostics logging level for the Autofs storage map responder daemon socket. | `10` |
| `sssd_ldap_debug_level` | Diagnostics logging level for the back-end LDAP protocol handler layers. | `6` |
| `sssd_sudo_debug_level` | Diagnostics logging level for the centralized privilege escalation parser. | `5` |
| `sssd_ssh_debug_level` | Diagnostics logging level for the secure shell authorized key retrieval engine. | `5` |
| `sssd_kdc_debug_level` | Sets the diagnostic logging level for the Kerberos Key Distribution Center (KDC) locator proxy responder. Higher values yield more verbose output. | `7` |
| `sssd_pac_debug_level` | Sets the diagnostic logging level for the Privileged Attribute Certificate (PAC) responder subsystem. | `7` |
| `sssd_ifp_debug_level` | Sets the diagnostic logging level for the InfoPipe (IFP) D-Bus responder subsystem. | `7` |
| `sssd_ldap_tls_reqcert` | Strictness constraint controls for confirming the authority of the LDAP server SSL certificate. Choices: `never`, `allow`, `try`, `demand`, `hard`. | `"never"` |
| `sssd_ldap_tls_cacert` | The absolute file pathway point to the trusted Certificate Authority verification bundle. | `"/etc/ldap/certs/master_ca.pem"` |
| `sssd_ldap_tls_cert` | The absolute file path mapping to the local client system certificate file. | `"/etc/ldap/certs/cert.pem"` |
| `sssd_ldap_tls_key` | The absolute file path locating the unencrypted local system client private key. | `"/etc/ldap/certs/priv.pem"` |
| `sssd_ldap_schema` | The schema protocol architecture ruleset used for directory data parsing. Choices: `rfc2307`, `rfc2307bis`, `IPA`, `AD`. | `"rfc2307"` |
| `sssd_ldap_rfc2307_fallback_to_local_users` | Instructs the local SSSD engine to merge network-fetched account memberships cleanly into matching local files like `/etc/group`. | `true` |
| `sssd_ldap_group_object_class` | Defines the explicit LDAP database structural object type used to filter group container searches. | `"posixGroup"` |
| `sssd_ldap_group_name` | Sets the naming attribute key used to extract the human-readable identifier for network groups. | `"cn"` |
| `sssd_ldap_group_gid_number` | Maps the target structural field tracking numeric Linux Group IDs inside directory records. | `"gidNumber"` |
| `sssd_ldap_group_member` | Dictates the explicit member attribute token string used to process individual username accounts. | `"memberUid"` |
| `sssd_ldap_group_uuid` | Tracks the internal unique structural object identifier used by the provider backend for group indexing operations. | `"nsUniqueId"` |
| `sssd_ldap_user_uuid` | Tracks the internal unique structural object identifier used by the provider backend for user indexing operations. | `"nsUniqueId"` |
| `sssd_ldap_id_mapping` | Controls dynamic SID-to-UID calculation. Set to false to force SSSD to rely strictly on your explicitly declared directory uidNumber and gidNumber attributes. | `false` |
| `sssd_nss_homedir_substring` | The root fallback folder namespace handle for network user directory shells. | `"/home"` |
| `sssd_ldap_search_timeout` | The lifespan window boundary allowed for waiting on directory queries before aborting. | `90` |
| `sssd_ldap_network_timeout` | The communication buffer maximum wait state constraint for sluggish TCP socket channels. | `90` |
| `sssd_timeout` | The global operational baseline timer threshold parameter for cached records sweeps. | `30` |
| `sssd_ldap_autofs_map_object_class` | The target object class structural identity tracking root automount mount configurations. | `"automountMap"` |
| `sssd_ldap_autofs_entry_object_class` | The schema object identity matching active path configuration blocks records. | `"automount"` |
| `sssd_ldap_autofs_map_name` | The system attribute key string identifying the explicit mapping namespace. | `"automountMapName"` |
| `sssd_ldap_autofs_entry_key` | The attribute tracking the physical network share name location target. | `"automountKey"` |
| `sssd_ldap_autofs_entry_value` | The attribute holding the transmission flags and backend storage path mappings properties. | `"automountInformation"` |
| `sssd_ssh_hash_known_hosts` | Toggles cryptographic obfuscation processing parameters for cached SSH client identity tracking matrices. | `true` |
| `sssd_ldap_access_filter` | The exact search criteria token string mandatory for allowing an identity object to initialize system logins. | `"(objectClass=posixAccount)"` |

## Helpful Debugging Commands

``` shell
sudo /usr/sbin/automount -m
```

``` shell
sudo sssctl domain-status your-domain.com
```

``` shell
sudo sssctl config-check
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

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
