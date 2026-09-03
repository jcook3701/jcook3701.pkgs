# [Docker-CE](https://docs.docker.com/engine/install/debian/) (`docker_ce`)

Docker Engine is an open source containerization technology for building and containerizing your applications. Docker Engine acts as a client-server application with:

* A server with a long-running daemon process dockerd.
* APIs which specify interfaces that programs can use to talk to and instruct the Docker daemon.
* A command line interface (CLI) client docker.

## Features

* **Complete Lifecycle Management:** Supports both provisioning (`present`) and clean structural removal (`absent`) of the Docker runtime and storage roots.
* **Granular Access Control:** Automatically manages the `docker` system group and safely appends designated non-root users.
* **Modern CLI Tooling:** Includes options to deploy official Docker Compose V2 and Docker Buildx plugins.
* **Defensive Runtime Defaults:** Provisions log rotation caps (`max-size: 50m`, `max-file: 3`), enables `live-restore` for uninterrupted daemon upgrades, and disables the high-latency `userland-proxy`.
* **Deep Dictionary Extensibility:** Provides a `docker_ce_config_custom` dictionary hook to recursively inject custom `daemon.json` settings without requiring template changes.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`docker_ce_state`** | Structural installation state (`present` or `absent`). Setting this to `absent` purges packages and storage assets. | `"present"` |
| **`docker_ce_users`** | A declarative list of local system accounts that will be added to the managed `docker` system group. | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| **`docker_ce_manage_group`** | Toggles whether the role ensures the foundational `docker` system group is actively declared and maintained. | `true` |
| **`docker_ce_download_url`** | The primary upstream URL base path used to fetch docker repository files. | `https://download.docker.com` |
| **`docker_ce_install_compose`** | Controls whether the modern Docker Compose v2 CLI plugin package is included in the installation. | `true` |
| **`docker_ce_install_buildx`** | Controls whether the next-generation Docker Buildx CLI extension plugin package is deployed. | `true` |
| **`docker_ce_manage_config`** | Master switch to determine if the role renders and manages the main `/etc/docker/daemon.json` configuration file. | `true` |
| **`docker_ce_data_root`** | Absolute directory path on the host node where images, containers, and volumes persist. | `"/var/lib/docker"` |
| **`docker_ce_storage_driver`** | Storage execution driver utilized by the kernel to stitch container root filesystems. | `"overlay2"` |
| **`docker_ce_storage_opts`** | Custom parameter flags passed directly to backing file storage layers. | `[]` |
| **`docker_ce_log_driver`** | Target standard stdout/stderr logging driver used to intercept and persist container outputs. | `"json-file"` |
| **`docker_ce_log_opts`** | Key-value options enforcing log rotation caps to block container log disk exhaustion. | `{"max-size": "50m", "max-file": "3"}` |
| **`docker_ce_live_restore`** | Keeps running containers alive and responsive during Docker daemon updates and service restarts. | `true` |
| **`docker_ce_iptables`** | Enables automatic injection of Docker netfilter firewall routing rules into kernel tables. | `true` |
| **`docker_ce_ip_forward`** | Enforces Linux sysctl packet forwarding rules to bridge network traffic cleanly. | `true` |
| **`docker_ce_userland_proxy`** | Toggles user-space proxy routing. Disabling optimizes network latency and throughput. | `false` |
| **`docker_ce_default_address_pools`** | Subnet pools allocated dynamically when creating user-defined bridge networks. | `[]` |
| **`docker_ce_dns_servers`** | Static upstream DNS nameservers provided to newly spawned containers. | `[]` |
| **`docker_ce_dns_search`** | DNS search domains appended to container name resolution queries. | `[]` |
| **`docker_ce_registry_mirrors`** | Upstream registry mirrors queried prior to hitting default public registries. | `[]` |
| **`docker_ce_insecure_registries`** | Custom private registry endpoints exempt from strict TLS verification. | `[]` |
| **`docker_ce_metrics_addr`** | Network host/socket address exposing Prometheus-compatible runtime metrics. | `""` |
| **`docker_ce_experimental`** | Enables experimental daemon features and command sets. | `false` |
| **`docker_ce_config_custom`** | Free-form dictionary merged recursively into the generated `daemon.json` file. | `{}` |

## Example Playbooks

### 1. Standard Production Deployment

Installs Docker CE, enables Buildx and Compose plugins, adds the deployment user to the `docker` group, and applies standard log-capping defaults.

```yaml
- name: Deploy Docker CE Container Runtime
  hosts: container_hosts
  become: true
  roles:
    - role: jcook3701.pkgs.docker_ce
      vars:
        docker_ce_users:
          - name: "deploy"
          - name: "admin"
        docker_ce_dns_servers:
          - "1.1.1.1"
          - "8.8.8.8"
```

### 2. Custom Data Path with Registry Mirror & Metrics

Configures Docker to run its storage root on a dedicated NVMe array, connects to an internal harbor registry, and exposes Prometheus metrics.

```yaml
- name: Deploy Docker CE with Custom Storage and Monitoring
  hosts: compute_nodes
  become: true
  roles:
    - role: jcook3701.pkgs.docker_ce
      vars:
        docker_ce_data_root: "/mnt/fast-storage/docker"
        docker_ce_metrics_addr: "127.0.0.1:9323"
        docker_ce_experimental: true
        docker_ce_registry_mirrors:
          - "https://domain.com"
        docker_ce_config_custom:
          features:
            containerd-snapshotter: true
```

### 3. Decommissioning / Clean Purge

Stops services, cleans up systemd unit files, and completely removes Docker CE packages.

```yaml
- name: Remove Docker Runtime
  hosts: legacy_hosts
  become: true
  roles:
    - role: jcook3701.pkgs.docker_ce
      vars:
        docker_ce_state: "absent"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
helpful links:
[download](https://download.docker.com/linux/)
-->
