# tailscale

[Tailscale](https://tailscale.com/) is a zero-config, mesh VPN service that simplifies secure connectivity between devices, regardless of their physical location or network complexity. It is built on the WireGuard protocol for high-performance, end-to-end encryption.

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
