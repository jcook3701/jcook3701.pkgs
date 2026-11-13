# Wireguard VPN

[`WireGuard`](https://www.wireguard.com/) is an extremely simple yet fast and modern VPN that utilizes state-of-the-art cryptography. It aims to be faster, simpler, leaner, and more useful than IPsec, while avoiding the massive headache. It intends to be considerably more performant than OpenVPN. WireGuard is designed as a general purpose VPN for running on embedded interfaces and super computers alike, fit for many different circumstances. Initially released for the Linux kernel, it is now cross-platform (Windows, macOS, BSD, iOS, Android) and widely deployable. It is currently under heavy development, but already it might be regarded as the most secure, easiest to use, and simplest VPN solution in the industry.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `wireguard_state` | The desired deployment state of WireGuard configuration files and services. Choices: `present`, `absent`. | `"present"` |
| `wireguard_interface` | The name of the WireGuard interface configuration file (maps to `/etc/wireguard/{{ wireguard_interface }}.conf`). | `"wg0"` |
| `wireguard_address` | The local IP address and subnet mask assigned to this host's tunnel interface (e.g., `10.0.0.1/24`). | `""` |
| `wireguard_port` | The UDP port WireGuard will listen on for incoming VPN connections. | `51820` |
| `wireguard_private_key` | The local private key for this node. If left empty, tasks will automatically generate a persistent key inside `/etc/wireguard/keys/`. | `null` |
| `wireguard_ip_forward` | Controls whether to configure kernel IP forwarding (`sysctl`) to route traffic between peers. | `false` |
| `wireguard_post_up` | PostUp shell commands executed when bringing the interface up (often used for iptables NAT routing). | `[]` |
| `wireguard_post_down` | PostDown shell commands executed when bringing the interface down. | `[]` |
| `wireguard_peers` | A list of remote peers connected to this host. Each item is a dictionary containing:<br>• **`name`** *(str, required)*: Descriptive identifier for the peer.<br>• **`public_key`** *(str, required)*: WireGuard public key of the remote peer.<br>• **`preshared_key`** *(str, optional)*: Pre-shared key for extra symmetric encryption.<br>• **`allowed_ips`** *(list of str, required)*: Subnets routed through this specific peer connection.<br>• **`endpoint`** *(str, optional)*: Public WAN IP and port if the peer sits on a static address.<br>• **`persistent_keepalive`** *(int, optional)*: Keepalive interval in seconds to punch through restrictive NATs. | `[]` |

## Example Configurations

### Example 1: Centralized VPN Server (Hub with NAT Routing)
This setup configures the target machine as a central VPN server. It enables kernel IP forwarding and automatically injects dynamically evaluated `iptables` rules to masquerade outbound client traffic through the host's primary public internet interface.

```yaml
wireguard_state: present
wireguard_interface: wg0
wireguard_address: 10.8.0.1/24
wireguard_port: 51820
wireguard_ip_forward: true

# Dynamic interface translation prevents broken paths across varying cloud platforms
wireguard_post_up:
  - "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o {{ ansible_default_ipv4.interface }} -j MASQUERADE"

wireguard_post_down:
  - "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o {{ ansible_default_ipv4.interface }} -j MASQUERADE"

wireguard_peers:
  - name: "site-b-router"
    public_key: "base64_encoded_public_key_string_for_site_b="
    allowed_ips:
      - "10.8.0.2/32"
  - name: "ops-laptop"
    public_key: "base64_encoded_public_key_string_for_laptop="
    allowed_ips:
      - "10.8.0.3/32"
```

### Example 2: Client Node Configuration (Spoke)
This setup configures a remote node or branch gateway connecting back to the central server. It forces all outbound network traffic safely through the encrypted tunnel (`0.0.0.0/0`) and leverages keepalives to prevent restrictive local network firewalls from timing out the connection state.

```yaml
wireguard_state: present
wireguard_interface: wg0
wireguard_address: 10.8.0.2/24

wireguard_peers:
  - name: "primary-hq-server"
    public_key: "base64_encoded_public_key_string_for_server_hq="
    endpoint: "://example.com"
    persistent_keepalive: 25
    allowed_ips:
      - "0.0.0.0/0"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
