# PAM (Pluggable Authentication Modules)

**PAM** is a system of libraries that handles user authentication and session management for applications across a Linux operating system.

## Role Variables

| Variable | Default Value | Type | Choices | Description |
| :--- | :--- | :--- | :--- | :--- |
| `pam_state` | `present` | String | `present`, `absent`, `teardown` | Controls the target module suite package and engine state. |
| `pam_enable_network_authentication` | `true` | Boolean | `true`, `false` | Controls session keyring security isolation behaviors. |
| `pam_enable_keyinit` | `true` | Boolean | `true`, `false` | Handles key management generation bindings upon shell creation. |
| `pam_enable_sssd` | `true` | Boolean | `true`, `false` | Configures structural lookup mappings using Active Directory/LDAP SSSD networks. |
| `pam_enable_mkhomedir` | `true` | Boolean | `true`, `false` | Instructs the stack to create missing user landing paths at connection. |
| `pam_mkhomedir_options` | `"skel=/etc/skel umask=0022"` | String | *Custom Flags* | Precise options parsing down directly into the `pam_mkhomedir.so` engine line. |
| `pam_enable_systemd` | `true` | Boolean | `true`, `false` | Enforces active login auditing registration metrics via `systemd-logind`. |
| `pam_enable_biometrics` | `false` | Boolean | `true`, `false` | Enables local workstation finger scanner interaction hooks. |
| `pam_enable_duo` | `false` | Boolean | `true`, `false` | Hooks Duo Security validation demands into ssh and tty profiles. |
| `pam_enable_u2f` | `false` | Boolean | `true`, `false` | Grants security token validation access controls on hardware keys. |
| `pam_enable_yubico` | `false` | Boolean | `true`, `false` | Activates verification support pathways using Yubikey infrastructure matrices. |

### Operational States Explained

* **`present`**: Ensures targeted security modules are installed and safely registers active profile lines into standard stack configurations.
* **`absent` & `teardown`**: Reverts core authorization rules back to clean native OS stack shapes and strips active MFA custom constraints.

## Configuration Examples

### Example 1: Secure Corporate Network Client (SSSD + Home Directory Provisioning)

Perfect for network-attached enterprise systems joining active directory domains.

```yaml
pam_state: present
pam_enable_sssd: true
pam_enable_mkhomedir: true
pam_mkhomedir_options: "skel=/etc/skel umask=0027"
```

### Example 2: Hardened Multi-Factor Authentication Bastion

Applies strict MFA constraints alongside standard system session handlers.

```yaml
pam_state: present
pam_enable_duo: true
pam_enable_u2f: true
pam_enable_network_authentication: false
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
