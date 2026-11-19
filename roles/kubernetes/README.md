# Kubernetes (k8s)

[Kubernetes](https://kubernetes.io/) is an open-source container orchestration platform for automating the deployment, scaling, and management of containerized applications.

This Ansible role, part of the `jcook3701.pkgs` collection, manages the installation, configuration, and removal of Kubernetes packages and supporting command-line tools on supported Linux distributions.

The primary Kubernetes components include:

- **[kubectl](https://kubernetes.io/docs/reference/kubectl/)** — Command-line interface for communicating with Kubernetes clusters and managing cluster resources.
- **[kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)** — Tool for initializing Kubernetes clusters and joining additional nodes.
- **[kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)** — Node agent responsible for managing containers running in Kubernetes Pods.
- **[crictl](https://github.com/kubernetes-sigs/cri-tools)** — Command-line utility for inspecting and troubleshooting Container Runtime Interface (CRI) compatible runtimes.

Package repository management is delegated to `jcook3701.utils.repo_add`, while installation and removal operations are handled through `jcook3701.utils.pkg_manager`.

## Role Variables

### Lifecycle & System Access Management

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_state` | str | Desired lifecycle state. Choices: `present`, `absent`, `teardown`. | `present` |
| `kubernetes_debug` | bool | Enable debugging during role execution. | `true` |

### Kubernetes Repository Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_download_url` | str | Base URL for the official Kubernetes package repositories. | `https://pkgs.k8s.io/core` |

### Kubernetes Package Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_manage_engine` | bool | Flag reserved for managing the container engine; runtime provisioning is not yet implemented by this role. | `true` |
| `kubernetes_engine` | str | Selected container engine, used to determine the default CRI endpoint. Common values include `docker`, `containerd`, and `cri-o`. | `docker` |
| `kubernetes_kubernetes_version` | str | Target Kubernetes release, used to derive the package repository's minor version. | `1.37.0` |

### Kubernetes Configuration API

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_kubeadm_api_version` | str | Configuration API version used for kubeadm initialization and joining. | `kubeadm.k8s.io/v1beta4` |
| `kubernetes_kubelet_api_version` | str | Configuration API version used for kubelet configuration. | `kubelet.config.k8s.io/v1beta1` |

### Kubernetes Cluster Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_cluster_name` | str | Logical name assigned to the Kubernetes cluster. | `kubernetes` |
| `kubernetes_control_plane_endpoint` | str | Stable IP address or DNS endpoint for the Kubernetes control plane. | `""` |
| `kubernetes_api_advertise_address` | str | IP address advertised by the Kubernetes API server. An empty value allows kubeadm to determine the address. | `""` |
| `kubernetes_api_bind_port` | int | Port used by the Kubernetes API server. | `6443` |
| `kubernetes_pod_subnet` | str | CIDR subnet allocated to Kubernetes Pods; should match the selected CNI configuration. | `""` |
| `kubernetes_service_subnet` | str | CIDR subnet allocated to Kubernetes Services. | `10.96.0.0/12` |
| `kubernetes_dns_domain` | str | DNS domain used for Kubernetes cluster services. | `cluster.local` |

### Kubernetes Node Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_node_name` | str | Kubernetes node name; an empty value allows Kubernetes to use the system hostname. | `""` |
| `kubernetes_cri_socket` | str | Container Runtime Interface socket, optionally specified instead of automatic detection. | `""` |

### Kubernetes Kubelet Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_kubelet_cgroup_driver` | str | Cgroup driver used by kubelet. Choices: `systemd`, `cgroupfs`. | `systemd` |
| `kubernetes_kubelet_rotate_certificates` | bool | Enable automatic rotation of kubelet client certificates. | `true` |
| `kubernetes_kubelet_cluster_dns` | list[str] | DNS servers used by Kubernetes Pods. | `[]` |
| `kubernetes_kubelet_resolv_conf` | str | Path to the resolver configuration used by kubelet. | `""` |

### Kubernetes Node Joining Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_join_api_server_endpoint` | str | API server endpoint used when joining a Kubernetes cluster. | `""` |
| `kubernetes_join_token` | str | Bootstrap token used for cluster authentication. Store securely using Ansible Vault. | `""` |
| `kubernetes_join_ca_cert_hashes` | list[str] | Trusted SHA-256 CA public key hashes used during cluster discovery. | `[]` |
| `kubernetes_join_control_plane` | bool | Configure the joining node as an additional control-plane node instead of a worker. | `false` |
| `kubernetes_join_certificate_key` | str | Certificate decryption key used when joining additional control-plane nodes. Store securely using Ansible Vault. | `""` |
| `kubernetes_join_advertise_address` | str | Local API server advertise address for a joining control-plane node. | `""` |

### Kubernetes CRI Tools Configuration

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_manage_crictl_config` | bool | Manage the `/etc/crictl.yaml` configuration file. | `true` |
| `kubernetes_crictl_runtime_endpoint` | str | Explicit CRI runtime socket endpoint. When empty, derive from `kubernetes_cri_socket` or the selected container engine. | `""` |
| `kubernetes_crictl_image_endpoint` | str | CRI image service endpoint. When empty, use the effective runtime endpoint. | `""` |
| `kubernetes_crictl_timeout` | int | Timeout in seconds for crictl runtime requests. | `2` |
| `kubernetes_crictl_debug` | bool | Enable debugging for crictl commands. | `false` |

### Internal Role Variables

The following variables are defined in `vars/main.yml` and `vars/ubuntu.yml` and are used internally for operating-system-specific package management, repository configuration, and file paths.

| Variable | Type | Description / Default |
| :--- | :--- | :--- |
| `kubernetes_kubernetes_major_minor_version` | str | Derived Kubernetes major/minor version, e.g. `1.37`. |
| `kubernetes_pkg_names` | list[str] | Package list determined by OS-specific variables. |
| `kubernetes_os_pkg_names` | list[str] | Ubuntu packages: `kubelet`, `kubeadm`, `kubectl`, `cri-tools`. |
| `kubernetes_directory` | dict | Kubernetes configuration directory, default `/etc/kubernetes`. |
| `kubernetes_file` | dict | Destination paths for the Kubernetes configuration files. |
| `kubernetes_repo_id` | str | Repository identifier, default `kubernetes`. |
| `kubernetes_repo_name` | str | Human-readable repository description, default `Kubernetes (k8s) PPA`. |
| `kubernetes_os_directory` | dict | Ubuntu-specific configuration directory paths. |
| `kubernetes_os_repo_id` | str | Ubuntu repository identifier, default `kubernetes`. |
| `kubernetes_os_repo_name` | str | Ubuntu repository description, default `Kubernetes (k8s) PPA`. |
| `kubernetes_debian_uris` | str | Kubernetes minor-version-specific Debian repository URL. |
| `kubernetes_debian_suites` | str | Debian repository suite, default `/`. |
| `kubernetes_debian_component` | str | Debian repository component, default empty string. |
| `kubernetes_debian_signed_by` | str | Official Kubernetes repository signing key URL. |
| `kubernetes_crictl_runtime_endpoint_effective` | str | Derived CRI endpoint, resolved from explicit settings or the container engine. |

## Configuration Files

The role provides Jinja2 templates for Kubernetes cluster initialization, node joining, kubelet configuration, and CRI tooling.

| Template | Destination | Purpose |
| :--- | :--- | :--- |
| `kubeadm-init-config.yaml.j2` | `/etc/kubernetes/kubeadm-init-config.yaml` | Configuration for initializing a Kubernetes cluster. |
| `kubeadm-join-config.yaml.j2` | `/etc/kubernetes/kubeadm-join-config.yaml` | Configuration for joining worker or control-plane nodes. |
| `kubelet-config.yaml.j2` | `/etc/kubernetes/kubelet-config.yaml` | Kubelet configuration, including cgroup and networking settings. |
| `crictl.yaml.j2` | `/etc/crictl.yaml` | CRI endpoint, image service, timeout, and debugging configuration. |

Configuration templates are deployed through `tasks/configure/01_seed.yml`.

The cluster-joining configuration is generated only when the required API server endpoint, bootstrap token, and CA certificate hashes are provided.

**Note:** These templates generate configuration files; they do not automatically execute `kubeadm init` or `kubeadm join`. The standalone kubelet configuration is not automatically installed as kubeadm's live configuration.

## Container Runtime Configuration

Kubernetes requires a Container Runtime Interface (CRI) compatible runtime.

The role derives the default CRI endpoint from the selected `kubernetes_engine`, unless an explicit endpoint is supplied.

| Container Engine | Default CRI Endpoint |
| :--- | :--- |
| `docker` | `unix:///var/run/cri-dockerd.sock` |
| `containerd` | `unix:///run/containerd/containerd.sock` |
| `cri-o` | `unix:///var/run/crio/crio.sock` |

The endpoint selection follows this priority:

1. `kubernetes_crictl_runtime_endpoint`
2. `kubernetes_cri_socket`
3. Endpoint derived from `kubernetes_engine`

Docker Engine requires an additional CRI adapter, such as `cri-dockerd`, to function as a Kubernetes container runtime.

The role currently generates the configuration necessary to communicate with the selected runtime but does not automatically install or start that runtime.

## Authors Notes

The Kubernetes role separates package lifecycle management from repository configuration and cluster initialization.

Repository configuration is delegated to `jcook3701.utils.repo_add`, and package installation and removal are managed through `jcook3701.utils.pkg_manager`.

The role supports three lifecycle states:

- **present** — Install Kubernetes packages and generate the applicable configuration files.
- **absent** — Uninstall Kubernetes packages through the package manager.
- **teardown** — Uninstall Kubernetes packages and remove the configured package repository.

The current teardown workflow does not automatically delete the generated Kubernetes configuration files.

Kubernetes publishes separate package repositories for each minor release series. The `kubernetes_kubernetes_version` variable determines the appropriate repository series, but does not independently enforce an exact installed package patch version.

Cluster initialization, CNI installation, runtime provisioning, and node joining remain separate operations.

Sensitive credentials, including cluster bootstrap tokens and control-plane certificate keys, should be managed using Ansible Vault. Generated cluster-joining configuration files use restrictive `0600` permissions.

**List of helpful links:**

1. [Kubernetes Documentation](https://kubernetes.io/docs/home/)
2. [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
3. [Installing kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
4. [Creating a Cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
5. [Kubernetes Configuration API](https://kubernetes.io/docs/reference/config-api/)
6. [Kubernetes Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
7. [Debugging Kubernetes Nodes with crictl](https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/)
8. [Kubernetes Package Repositories](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/change-package-repository/)
9. [Kubernetes Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/)

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
