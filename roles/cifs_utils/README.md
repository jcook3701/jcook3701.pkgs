# Cifs-Utils

[cifs-utils](https://www.kali.org/tools/cifs-utils/) is a package of user-space tools for Linux used to mount and manage SMB/CIFS network shares (such as Windows shared folders or NAS devices). It supplies helper utilities like mount.cifs that work with the Linux kernel to handle modern SMB protocols (SMB2/SMB3).

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`cifs_utils_state`** | The installation, configuration, or structural removal state of the CIFS client software packages. | `"present"` |
| **`cifs_utils_use_gssproxy`** | Toggles whether the kernel upcall binary should bypass traditional lookups to utilize a GSSProxy interception socket. | `false` |
| **`cifs_utils_gssproxy_socket`** | Specialized IPC socket path used when GSS-Proxy manages Kerberos upcalls. | `"/var/lib/gssproxy/cifs.sock"` |
| **`cifs_utils_client_enable_mounts`** | Toggle client mount tasks on or off. | `false` |
| **`cifs_utils_client_mounts`** | A declarative array tracking active remote SMB/CIFS network share allocations managed on the target machine. | `[]` |

## Role Design

``` shell
                [ Playbook execution starts (tasks/main.yml) ]
                                      │
                                      ▼
                        Gather target host package facts
                    Load dynamic OS vars (*.yml) from vars/
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼ (cifs_utils_state == 'present')               ▼ (cifs_utils_state == 'absent')
    ┌───────────────────────────────┐               ┌───────────────────────────────┐
    │       state/install.yml       │               │      state/uninstall.yml      │
    ├───────────────────────────────┤               ├───────────────────────────────┤
    │ Installs cifs-utils and any   │               │ Cleans up fstab file records, │
    │ required keyutils dependencies│               │ unmounts live CIFS paths,     │
    │ based on the target OS vars.  │               │ and purges systemic binaries. │
    └───────────────┬───────────────┘               └───────────────────────────────┘
                    │
                    ▼
       [ Entry: tasks/configure/main.yml ]
                    │
                    ▼
┌───────────────────────────────────────────────────────────┐
│              tasks/configure/main.yml Tasks               │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ 1. Deploys dynamic cifs.spnego.conf.j2 layout into       │
│    the request-key.d/ snippet inclusion subdirectory.      │
│                                                           │
│ 2. Evaluates loop rules to match declarative mount arrays │
│    and mounts remote shares securely to filesystem paths. │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
               [ Bimodal Execution Layer ]
              Evaluates user toggle selections
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
[ cifs_utils_use_gssproxy: false ]    [ cifs_utils_use_gssproxy: true ]
┌───────────────────────────────┐   ┌───────────────────────────────┐
│          Native Mode          │   │      GSSProxy Intercept       │
├───────────────────────────────┤   ├───────────────────────────────┤
│ Configures upcall flags to "". │   │ Configures upcall flags to    │
│ Kernel checks environment and │   │ "-t". Kernel bypasses local   │
│ queries active local SSSD     │   │ files and routes handshakes   │
│ process caches dynamically.   │   │ straight into cifs.sock.      │
└───────────────────────────────┘   └───────────────────────────────┘
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

``` shell
[User: ls /media/...] ──► [Linux Kernel (cifs.ko)]
                                 │
                     (Environment Redirection)
                                 │
                                 ▼
                     [/etc/request-key.d/cifs.spnego.conf]
                                 │
                         (GSS_USE_PROXY=yes)
                                 │
                                 ▼
                     [GSS-Proxy: cifs.sock]
                                 │
                   (Impersonate Calling User UID)
                                 │
                                 ▼
                     [SSSD Local Socket Pipe]
                                 │
                       (Extract Ticket Cache)
                                 │
                                 ▼
                     [SSSD KCM Database Memory]
```

-->
