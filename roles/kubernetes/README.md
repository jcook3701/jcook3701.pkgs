# Kubernetes (k8s)

[Kubernetes](https://kubernetes.io/) is an open-source container orchestration platform for automating the deployment, scaling, and management of containerized applications.

This Ansible role, part of the `jcook3701.pkgs` collection, manages Kubernetes package installation, removal, and related configuration on supported Linux distributions.

Core Kubernetes components include:

- **[kubectl](https://kubernetes.io/docs/reference/kubectl/)** — Command-line interface for managing Kubernetes clusters.
- **[kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)** — Tool for initializing Kubernetes clusters and joining nodes.
- **[kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)** — Node agent responsible for managing Kubernetes Pods.

APT repository management is delegated to `jcook3701.utils.repo_adder`.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_state` | str | Desired lifecycle state of the Kubernetes installation. | `present` |
| `kubernetes_debug` | bool | Enable debugging during role execution. | `true` |
| `kubernetes_download_url` | str | Base URL for the official Kubernetes package repositories. | `https://pkgs.k8s.io/core` |
| `kubernetes_manage_engine` | bool | Control whether the role manages the selected container engine. | `true` |
| `kubernetes_engine` | str | Selected container engine. | `docker` |
| `kubernetes_kubernetes_version` | str | Target Kubernetes release version used to derive the repository series. | `1.37.0` |

### Internal Role Variables

The following variables are defined in `vars/main.yml` and `vars/ubuntu.yml`.

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `kubernetes_kubernetes_major_minor_version` | str | Major and minor version derived from the configured Kubernetes version. | `1.37` |
| `kubernetes_pkg_names` | list | Package list determined by OS-specific variables. | `['kubernetes']` |
| `kubernetes_directory` | dict | Kubernetes configuration directory paths. | `config: /etc/kubernetes` |
| `kubernetes_file` | dict | Kubernetes configuration file paths. | `config: /etc/kubernetes/config.toml` |
| `kubernetes_repo_id` | str | Repository identifier. | `kubernetes` |
| `kubernetes_repo_name` | str | Human-readable repository description. | `Kubernetes (k8s) PPA` |
| `kubernetes_os_pkg_names` | list | Ubuntu-specific package selection. | `['kubernetes']` |
| `kubernetes_os_directory` | dict | Ubuntu-specific configuration directory paths. | `config: /etc/kubernetes` |
| `kubernetes_os_repo_id` | str | Ubuntu repository identifier. | `kubernetes` |
| `kubernetes_os_repo_name` | str | Ubuntu repository description. | `Kubernetes (k8s) PPA` |
| `kubernetes_debian_uris` | str | Version-specific Kubernetes Debian repository URL. | `https://pkgs.k8s.io/core:/stable:/v1.37/deb/` |
| `kubernetes_debian_suites` | str | Debian repository suite. | `/` |
| `kubernetes_debian_component` | str | Debian repository component. | Empty string |
| `kubernetes_debian_signed_by` | str | URL of the official Kubernetes repository signing key. | `https://pkgs.k8s.io/core:/stable:/v1.37/deb/Release.key` |

## Authors Notes

The Kubernetes role separates package management from repository configuration.

Repository configuration is managed through `jcook3701.utils.repo_adder`, allowing the same repository management system to be reused across other Ansible roles.

Kubernetes publishes separate package repositories for each minor release series. The configured version determines the appropriate repository URL.

Selecting a repository series does not independently pin the installed package to an exact patch version. Kubernetes upgrades should be coordinated with cluster version compatibility requirements.

Installing Kubernetes packages does not automatically initialize a Kubernetes cluster. Additional configuration is required for container runtimes, networking, and cluster initialization.

**List of helpful links:**

1. [Kubernetes Documentation](https://kubernetes.io/docs/home/)
2. [Installation Guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
3. [Installing kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
4. [Kubernetes Package Repositories](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/change-package-repository/)
5. [Kubernetes Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
6. [Kubernetes Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/)

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
