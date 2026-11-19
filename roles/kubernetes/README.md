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
| `kubernetes_node_name` | str | Kubernetes node name; an empty value allows Kubernetes to use the system
