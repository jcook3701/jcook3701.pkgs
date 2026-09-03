# GSS-Proxy

[Gssproxy](https://github.com/gssapi/gssproxy/tree/master/docs) is a system daemon that manages GSSAPI (Generic Security Services API) credentials and Kerberos authentication. It improves security by allowing applications to handle secure network logins without having direct access to sensitive secret keys or keytab files.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`gssproxy_state`** | The installation or operational state of the GSSProxy packages and configuration profiles. | `"present"` |
| **`gssproxy_manage_service`** | Toggles whether the role should actively enforce systemd service runtime states and reloads. | `true` |
| **`gssproxy_debug_level`** | Global diagnostics logging level for the primary GSSProxy daemon service. | `"3"` |
| **`gssproxy_services`** | A comprehensive array tracking application configuration templates, sockets, and credential parameters. | *See structured defaults* |

## Architectural Flow

$$\text{Application/Kernel} \xrightarrow{\text{GSSAPI Calls}} \textbf{gssproxy} \xrightarrow{\text{libkrb5 / SSSD}} \textbf{KDC}$$

1. **The Application Needs Auth:** An application (like Apache or an NFS server) makes a standard GSSAPI security request.
2. **gssproxy Intercepts It:** Instead of the application accessing a private keytab file, gssproxy securely handles the cryptographic operations in its isolated process.
3. **SSSD Manages the Cache:** SSSD interacts with the KDC to acquire, refresh, and cache the Kerberos Tickets (TGTs). gssproxy can pull credentials directly from the caches that SSSD manages.

``` shell
 ┌────────────────────────────────────────────────────────────────────────┐
 │                           SECURE USER SPACE                            │
 │                                                                        │
 │   ┌──────────────┐       Reads Master Keys      ┌───────────────────┐  │
 │   │ SSSD Service │ ◄──────────────────────────► │ /etc/krb5.keytab  │  │
 │   └──────┬───────┘                              └───────────────────┘  │
 │          │ Generates & Routes                                          │
 │          ▼ User Tokens                                                 │
 │   ┌──────────────┐         Routes Contexts      ┌───────────────────┐  │
 │   │   GSSProxy   │ ◄──────────────────────────► │ clients/%U.keytab │  │
 │   │   (Router)   │                              └───────────────────┘  │
 └───────▲──┬──▲────┘                                                     │
         │  │  │                                                          │
 ┌───────┼──┼──┼──────────────────────────────────────────────────────────┘
 │       │  │  └───────────────┐ (Private Unix Domain Sockets)
 │       │  │                  │
 │   ┌───┴──┴───────┐   ┌──────┴───────┐   ┌──────────────┐
 │   │  Kernel NFS  │   │  cifs-utils  │   │ OpenSSH/Web  │
 │   │ (nfs.sock)   │   │ (cifs.sock)  │   │ (sshd.sock)  │
 │   └──────────────┘   └──────────────┘   └──────────────┘
 │                         UNTRUSTED SPACE                        │
 └────────────────────────────────────────────────────────────────┘
 ```

## Role Design

``` shell
                     [ Playbook execution starts ]
                                   │
                                   ▼
          ┌──────────────────────────────────────────────────┐
          │                  gssproxy role                   │
          │                                                  │
          │  - Installs core daemon & keyutils utilities     │
          │  - Generates master unix domain sockets          │
          │  - Sets up global Kerberos/privilege policies    │
          └────────────────────────┬─────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼ (CURRENTLY ACTIVE)         ▼ (CURRENTLY ACTIVE)         ▼ (FUTURE GROWTH)
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│  cifs_client  │            │  nfs_client   │            │  sshd_server  │
│     role      │            │     role      │            │     role      │
├───────────────┤            ├───────────────┤            ├───────────────┤
│ use_gssproxy: │            │ use_gssproxy: │            │ use_gssproxy: │
│     true      │            │     true      │            │     true      │
└───────────────┘            └───────────────┘            └───────────────┘
  Alters cifs.spnego           Injects nfs.conf             Isolates sshd
  to route kernel              gss-proxy flags;             privileges;
  upcalls to socket.           bypasses rpc.gssd.           proxies GSSAPI.
                                                                │
                                                                ▼
                                                          ┌───────────────┐
                                                          │  web_servers  │
                                                          │     role      │
                                                          ├───────────────┤
                                                          │ use_gssproxy: │
                                                          │     true      │
                                                          └───────────────┘
                                                            Allows Apache/
                                                            Nginx to validate
                                                            SPNEGO without
                                                            reading keytabs.
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

# Helpful Debugging Commands

``` shell
$ sudo lsof /var/lib/gssproxy/default.sock

``` shell
$ sudo ss -ax | grep gssproxy
```

- name: Clean up remaining persistent GSSProxy configuration path data
  ansible.builtin.file:
    path: "{{ item }}"
    state: "absent"
  become: true
  loop:
    - "{{ gss_proxy_directory.conf | default('/etc/gssproxy') }}"

-->
