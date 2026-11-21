# Kubernetes — `jcook3701.pkgs.kubernetes`

Ansible Galaxy role that installs Kubernetes with operating-system package managers and
configures an operational **kubeadm** cluster. Its optional CNI integrations are managed
inside this role, matching `tasks/plugins/` with `vars/plugins/`. The independent
`jcook3701.pkgs.helm` role runs first via `meta/main.yml` when managed CNI plugins are enabled.

## Lifecycle

- `present`: install packages through `jcook3701.utils.repo_add` and
  `jcook3701.utils.pkg_manager`, write kubeadm/kubelet/crictl configuration, validate
  running **containerd** CRI, bootstrap the control plane (or join an existing cluster),
  set up the user's kubeconfig, install exactly one CNI through Helm, and verify readiness.
- `absent`: remove Kubernetes packages while preserving cluster PKI and data.
- `teardown`: remove packages and the package repository. **No cluster reset unless**
  `kubernetes_reset_cluster_on_teardown: true` is set explicitly.

This role **does not install or replace Docker CE/containerd**. Docker CE's existing
containerd.io runtime must already be running and have its CRI plugin active with a
compatible systemd cgroup driver. If the runtime check fails, fix the existing
Docker CE/containerd configuration first. There is no kind, `cri-dockerd`, Podman, or
Flannel installation in this role.

## Supported Helm CNI providers

| `kubernetes_cni_provider` | Chart | Version default | Notes |
| --- | --- | --- | --- |
| `calico` | `projectcalico/tigera-operator` plus separately applied Calico CRDs | `v3.33.0` | Default; Kubernetes 1.37 tested |
| `cilium` | `oci://quay.io/cilium/charts/cilium` | `1.20.5` | Confirm upstream compatibility with Kubernetes 1.37 before production use |
| `external` | None | — | Requires `kubernetes_manage_plugins: false` and user-managed networking |

Calico 3.33 CRDs are rendered with the `admissionregistration.k8s.io/v1/MutatingAdmissionPolicy`
API compatibility flag for Kubernetes >=1.36 before installing the Tigera operator.
Cilium defaults to Kubernetes IPAM and **retains kube-proxy** rather than silently
changing cluster networking fundamentals. Both default to VXLAN encapsulation.

The role refuses to install a conflicting CNI Helm release or overwrite an existing
unmanaged Kubernetes CNI configuration. **Changing a live CNI is a migration**, not a
simple switch of a variable. It intentionally never uninstalls the other provider.

## Configuration and task organization

```text
roles/kubernetes/
├── README.md
├── defaults/main.yml
├── meta/{main.yml,argument_specs.yml}
├── tasks/
│   ├── main.yml
│   ├── state/{install.yml,uninstall.yml,teardown.yml}
│   ├── configure/{main.yml,01_seed.yml}
│   ├── cluster/{main.yml,preflight.yml,kubeadm.yml,join.yml,kubeconfig.yml,scheduling.yml,verify.yml}
│   └── plugins/{main.yml,calico.yml,cilium.yml}
├── vars/{main.yml,debian.yml,ubuntu.yml,redhat.yml}
│   └── plugins/{calico.yml,cilium.yml}
└── templates/{kubeadm-init-config.yaml.j2,kubeadm-join-config.yaml.j2,kubelet-config.yaml.j2,crictl.yaml.j2}
    └── plugins/{calico-values.yml.j2,cilium-values.yml.j2}
```

## Important public variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `kubernetes_state` | `present` | `present`, `absent`, `teardown` |
| `kubernetes_kubernetes_version` | `1.37.2` | Version used for target repo series and kubeadm config |
| `kubernetes_manage_cluster` | `true` | Run kubeadm and cluster tasks |
| `kubernetes_engine` | `containerd` | Use existing containerd CRI socket |
| `kubernetes_manage_engine` | `true` | Verify containerd runtime rather than install it |
| `kubernetes_cni_provider` | `calico` | `calico`, `cilium`, `external` |
| `kubernetes_manage_plugins` | `true` | Enable Helm-managed CNI install |
| `kubernetes_calico_chart_version` | `v3.33.0` | Pin Calico chart + CRD versions |
| `kubernetes_cilium_chart_version` | `1.20.5` | Pin Cilium OCI chart |
| `kubernetes_calico_custom_values` | `{}` | Merge optional Calico Helm values |
| `kubernetes_cilium_custom_values` | `{}` | Merge optional Cilium Helm values |
| `kubernetes_pod_subnet` | `""` | Empty selects `10.244.0.0/16` for managed CNIs |
| `kubernetes_manage_user_kubeconfig` | `true` | Install regular user's `~/.kube/config` |
| `kubernetes_kubeconfig_user` | `{{ ansible_user ... }}` | Regular Linux user for kubeconfig |
| `kubernetes_allow_control_plane_workloads` | `true` | Allow Pods on a single-node control plane |
| `kubernetes_manage_join` | `false` | Run `kubeadm join` instead of init |
| `kubernetes_reset_cluster_on_teardown` | `false` | Protect existing cluster state |

Other existing kubeadm, joining, CRI, and service-related variables remain in
`defaults/main.yml`, with their Ansible argument definitions in `meta/argument_specs.yml`.

## Example use

```yaml
---
- name: Install Kubernetes with Calico
  hosts: second-chance
  become: true
  roles:
    - role: jcook3701.pkgs.kubernetes
      vars:
        kubernetes_state: present
        kubernetes_cni_provider: calico
        kubernetes_kubeconfig_user: jcook
```

To use Cilium instead, select `kubernetes_cni_provider: cilium` **only on a new
cluster or after a planned network migration**. The switch is deliberately rejected
when another CNI is already installed.

## Verification

```bash
sudo crictl --runtime-endpoint unix:///run/containerd/containerd.sock info
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
helm list -A
```

The role's `meta/main.yml` declares Helm as a conditional Ansible role dependency so
it runs before Kubernetes cluster tasks on Debian/Ubuntu. This is the Ansible role
dependency, not a requirement to configure Helm release deployments in the Helm role.
The chart releases are owned solely by the Kubernetes role.

**Red Hat caveat:** Kubernetes package repo handling is present for Red Hat, but
`jcook3701.pkgs.helm` currently supports only Debian/Ubuntu. Managed CNI plugins
fail clearly on Red Hat until the Helm role is extended through package-management
conventions.

## Upstream docs

- [Calico Helm](https://docs.tigera.io/calico/latest/getting-started/kubernetes/helm)
- [Cilium kubeadm](https://docs.cilium.io/en/stable/installation/k8s-install-kubeadm/)
- [Kubernetes kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
