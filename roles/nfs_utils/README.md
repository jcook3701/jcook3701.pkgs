# NFS-Utils

The [nfs-utils](https://www.kali.org/tools/nfs-utils/) package provides essential user-space daemons and administrative tools to manage Network File System (NFS) connections on Linux, supporting both NFS clients and servers. You install it using package managers like sudo dnf install nfs-utils or sudo apt install nfs-common / nfs-kernel-server

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`nfs_utils_state`** | The installation, configuration, or structural removal state of the NFS ecosystem software packages. | `"present"` |
| **`nfs_utils_node_type`** | Selects the deployment topology mode for the target host machine (`client` or `master`). | `"client"` |
| **`nfs_utils_use_gssproxy`** | Toggles whether kernel RPC upcalls should be rerouted through a local GSSProxy interception socket. | `false` |
| **`nfs_utils_gssproxy_socket_name`** | The specific filename of the GSSProxy socket mapped within the runtime directory tracking structures. | `"gssproxy.sock"` |
| **`nfs_utils_top_level_domain`** | The top-level domain identifier (TLD) suffix utilized for environment identity resolution. | `"com"` |
| **`nfs_utils_second_level_domain`** | The core enterprise organizational or second-level domain name used for identity matching. | `"example"` |
| **`nfs_utils_domain_name`** | The fully qualified NFSv4 idmapd domain used to synchronize and map user UIDs/GIDs across different nodes. | `"example.com"` |
| **`nfs_utils_server_threads`** | The total number of kernel space daemon execution threads allocated to spin up for handling incoming traffic. | `8` |
| **`nfs_utils_server_protocols`** | A dictionary map used to explicitly enable or disable specific operational NFS protocol versions. | *(See Details)* |
| **`nfs_utils_server_exports`** | A declarative array tracking local directory paths and authorized client ACLs exported by this server. | `[]` |
| **`nfs_utils_client_enable_mounts`** | Master configuration toggle to enable or disable client-side NFS mount processing tasks. | `false` |
| **`nfs_utils_client_mounts`** | A declarative array tracking remote NFS resource URLs and local client target directories. | `[]` |
| **`nfs_utils_enable_debug_logging`** | Controls whether verbose debug logging and runtime trace loops are enabled across the system NFS core utilities. | `true` |

## Role Design

```shell
                [ Playbook execution starts (tasks/main.yml) ]
                                      │
                                      ▼
                        Gather target host package facts
                    Load dynamic OS vars (*.yml) from vars/
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼ (nfs_utils_state == 'present')                ▼ (nfs_utils_state == 'absent')
    ┌───────────────────────────────┐               ┌───────────────────────────────┐
    │       state/install.yml       │               │      state/uninstall.yml      │
    ├───────────────────────────────┤               ├───────────────────────────────┤
    │ Combines & purges duplicate   │               │ Queries systemd_facts, loops  │
    │ client + server packages using│               │ and stops all 3 services,     │
    │ unique concatenation filter.  │               │ then triggers complete purge. │
    └───────────────┬───────────────┘               └───────────────────────────────┘
                    │
                    ▼
       [ Entry: tasks/configure/main.yml ]
     Ensures base configuration directories exist
    Deploys global shared templates (nfs.conf, idmapd.conf)
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
[ nfs_utils_node_type == 'client' ]   [ nfs_utils_node_type == 'master' ]
┌───────────────────────────────┐   ┌───────────────────────────────┐
│     configure/client/         │   │     configure/server/         │
├───────────────────────────────┤   ├───────────────────────────────┤
│ ├── seed.yml                  │   │ ├── seed.yml                  │
│ │   Configures nfs.idmap.conf │   │ │   Generates exports_d and   │
│ │   upcall line.              │   │ │   deploys primary exports.  │
│ │                             │   │ │                             │
│ ├── service.yml               │   │ ├── service.yml               │
│ │   Stops server service.     │   │ │   Starts server daemon.     │
│ │   Ensures rpc-gssd is ready │   │ │   Disables deprecated       │
│ │   for interception.         │   │ │   rpc-svcgssd crypt helper. │
│ │                             │   └───────────────────────────────┘
│ └── mount.yml                 │
│     Parses declarative client │
│     mount list arrays into    │
│     system /etc/fstab file.   │
└───────────────────────────────┘
                    │
                    ▼
     [ Bimodal Execution Layer ]
    If nfs_utils_use_gssproxy == true:
    - Bypasses traditional authentication loops
    - Rewrites nfs.conf [gssd] flags to 1
    - Routes user-space contexts into nfs.sock
```

## Testing

``` shell
ansible-playbook -i "localhost," -c local tests/test.yml --check
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

``` shell
[User: ls /mnt/nfs_share] ──► [Linux Kernel (sunrpc.ko)]
                                    │
                         (Direct Kernel Socket Pipe)
                                    │
                                    ▼
                        [GSS-Proxy: /run/gssproxy.sock]
                                    │
                      (Impersonate Calling User UID)
                                    │
                                    ▼
                        [SSSD KCM Database Memory]
```

- hosts: storage_clients
  roles:
    - role: gss_proxy
    - role: cifs_utils
    - role: nfs_utils
-->
