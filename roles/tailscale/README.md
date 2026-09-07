# Tailscale

[Tailscale](https://tailscale.com/) is a zero-config, mesh VPN service that simplifies secure connectivity between devices, regardless of their physical location or network complexity. It is built on the WireGuard protocol for high-performance, end-to-end encryption.

## Role Variables

| Variable | Default Value | Type | Choices | Description |
| :--- | :--- | :--- | :--- | :--- |
| `tailscale_state` | `present` | String | `present`, `absent`, `teardown` | Controls the target package and engine state. |
| `tailscale_repo_url` | `https://tailscale.com/install.sh` | String | *Valid URL* | Remote endpoint utilized for fetching the official shell installation helper. |
| `tailscale_port` | `41641` | Integer | *Any Valid UDP* | The port used for direct, encrypted peer-to-peer communication. |
| `tailscale_daemon_extra_flags` | `""` | String | *Custom Arguments* | Configurations inserted directly into the system `/etc/default/tailscaled` file. |
| `tailscale_accept_dns` | `false` | Boolean | `true`, `false` | Accepts or rejects split-horizon Tailscale MagicDNS rules. Keeping this `false` prevents broken internal Kerberos SPN lookups. |
| `tailscale_hostname` | `""` | String | *Custom String* | Overrides the hostname listed inside your Tailscale account machines list. |
| `tailscale_advertise_exit_node` | `false` | Boolean | `true`, `false` | When true, enables this machine to act as a public exit proxy gateway. |
| `tailscale_advertise_routes` | `[]` | List | Strings (CIDR Blocks) | Instructs Tailscale to behave as a subnet router for the specified private local networks. |
| `tailscale_auth_key` | `null` | String | *Auth Token* | Secret cryptographic token passed to authorize the system state implicitly. |
| `tailscale_up_extra_flags` | `""` | String | *Custom Arguments* | Additional runtime flags appended directly onto `tailscale up`. |
| `tailscale_no_logs` | `false` | Boolean | `true`, `false` | Disables sending diagnostic logs and metrics up to corporate central collection nodes. |
| `tailscale_enable_ssh` | `false` | Boolean | `true`, `false` | Runs a production-hardened Tailscale SSH service controlled by your main Tailnet ACL. |

### Configuration Examples

#### Example 1: Automated Node Join (Exit Node enabled)

```yaml
tailscale_state: present
tailscale_auth_key: "tskey-auth-k123456CNTRL-abcdefg"
tailscale_up_extra_flags: "--advertise-exit-node --accept-routes"
```

#### Example 2: Subnet Router & Bastion Node

```yaml
tailscale_state: present
tailscale_auth_key: "tskey-auth-k123456CNTRL-abcdefg"
tailscale_hostname: "prod-us-east-gateway"
tailscale_enable_ssh: true
tailscale_advertise_routes:
  - "10.100.0.0/16"
  - "192.168.50.0/24"
```

#### Example 3: Disables MagicDNS handling explicitly so target machines don't lose local domain controller record tracking

```yaml
tailscale_state: present
tailscale_auth_key: "tskey-auth-k123456CNTRL-abcdefg"
tailscale_accept_dns: false
tailscale_no_logs: true
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
Authors Notes:

# TODO: Look into these for future server client setup.
server: --advertise-exit-node --advertise-routes=192.168.1.0/24
client: --accept-routes=true

``` shell
# 2. Server-specific execution rules
- name: Configure Server Specifics (Exit Node & Subnet Routing)
    ansible.builtin.command: >
    tailscale up
    --auth-key={{ tailscale_authkey }}
    --advertise-exit-node
    --advertise-routes=192.168.1.0/24
    --reset
    when: "'servers' in group_names"
    notify: Save tailscale state

# 3. Client-specific execution rules
- name: Configure Client Specifics
    ansible.builtin.command: >
    tailscale up
    --auth-key={{ tailscale_authkey }}
    --accept-routes=true
    --reset
    when: "'clients' in group_names"
```

-->
