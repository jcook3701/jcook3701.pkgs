# Helm (Kubernetes Package Manager)

[Helm](https://helm.sh/) is the Kubernetes package manager. This Ansible role is
part of the `jcook3701.pkgs` collection and installs, verifies, uninstalls, and
decommissions the Helm CLI on Debian-family Linux systems.

Helm 4 is the current stable major release. This role installs Helm through the
community-maintained [Buildkite-hosted APT repository](https://helm.sh/docs/intro/install/).
It uses the existing `jcook3701.utils.repo_add` and `jcook3701.utils.pkg_manager`
roles rather than implementing a separate package/repository manager.

## Features

- Manage `present`, `absent`, and `teardown` lifecycle states.
- Configure a signed APT repository with fingerprint validation.
- Install Helm using the shared package-management role.
- Optionally select an exact Debian package revision.
- Verify installation using `helm version --short`.
- Optionally manage per-user Helm chart repositories (disabled by default).
- Leave users' kubeconfig, charts, releases, and Helm cache alone.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `helm_state` | str | `present`, `absent`, or `teardown`. | `present` |
| `helm_debug` | bool | Display non-sensitive role and version information. | `true` |
| `helm_package_version` | str | Exact **APT package version**, including Debian revision; empty selects the available package. | `""` |
| `helm_verify_installation` | bool | Verify `helm version --short` after installation. | `true` |
| `helm_manage_repository` | bool | Configure/remove Helm's APT repository using `repo_add`. | `true` |
| `helm_download_url` | str | Buildkite-hosted Helm APT repository URL. | `https://packages.buildkite.com/helm-linux/helm-debian/any/` |
| `helm_repo_signing_key_url` | str | URL of the APT repository signing key. | `https://packages.buildkite.com/helm-linux/helm-debian/gpgkey` |
| `helm_repo_signing_key_fingerprint` | str | Trusted full signing-key fingerprint. | `DDF78C3E6EBB2D2CC223C95C62BA89D07698DBC6` |
| `helm_manage_chart_repositories` | bool | Optionally manage per-user Helm chart repositories. | `false` |
| `helm_repository_user` | str | User whose Helm repository configuration is changed; empty uses the SSH/connection user. | `""` |
| `helm_chart_repositories` | list[dict] | List of chart repositories containing `name`, `url`, and optional `state` (`present`/`absent`). | `[]` |

### Internal Role Variables

| Variable | Type | Description / Default |
| :--- | :--- | :--- |
| `helm_pkg_names` | list[str] | Package names, default `['helm']`. |
| `helm_install_pkg_names` | list[str] | Installation names, optionally suffixed with exact APT version. |
| `helm_repo_id` | str | Package repository identifier, default `helm`. |
| `helm_repo_name` | str | Package repository display name, default `Helm CLI (Buildkite)` on Debian/Ubuntu. |
| `helm_os_pkg_names` | list[str] | OS-specific packages, default `['helm']`. |
| `helm_debian_uris` | str | `https://packages.buildkite.com/helm-linux/helm-debian/any/`. |
| `helm_debian_suites` | str | `any`. |
| `helm_debian_component` | str | `main`. |
| `helm_debian_signed_by` | str | Signing-key download URL. |

## Lifecycle States

| State | Behavior |
| :--- | :--- |
| `present` | Verify package signing key, create the APT repository, install Helm, verify CLI, and optionally manage chart repositories. |
| `absent` | Remove Helm package (including package configuration and unused dependencies through `pkg_manager`). |
| `teardown` | Perform `absent` and remove the managed APT source and key. |

Removal does **not** delete Kubernetes resources, Helm releases, kubeconfig, or
per-user Helm chart repository/cache data. This is intentional.

## Example Playbook

```yaml
---
- name: Install Helm CLI
  hosts: linux_hosts
  become: true
  roles:
    - role: jcook3701.pkgs.helm
      vars:
        helm_state: present
        helm_manage_repository: true
```

### Optional chart repositories

Chart repositories are different from the system's APT repository. Helm stores
them in the invoking user's configuration. By default, this role does not
change them.

```yaml
---
- name: Configure Helm CLI and chart repositories
  hosts: linux_hosts
  become: true
  roles:
    - role: jcook3701.pkgs.helm
      vars:
        helm_manage_chart_repositories: true
        helm_repository_user: jcook
        helm_chart_repositories:
          - name: bitnami
            url: https://charts.bitnami.com/bitnami
            state: present
          - name: deprecated
            state: absent
```

The selected Linux user must already exist. The role adds or updates chart
repositories only when their URLs differ, and removes only explicitly specified
repositories marked `absent`. It does not automatically run `helm repo update`.

### Version selection

By default, the role installs a Helm package from the configured APT source.
For an exact package revision, use `helm_package_version` with the complete
version shown by `apt-cache madison helm`; this is not necessarily identical
to the upstream release string (for example, `v4.3.2`).

## Authors Notes

- **Supported platforms:** Debian and Ubuntu (Debian OS family). Other Linux
  distributions intentionally fail with a clear message until packaging and
  repository handling are implemented for them.
- **APT key security:** the role compares the downloaded signing key to Helm's
  documented full fingerprint before passing the key to `repo_add`. The
  fingerprint can be updated explicitly when an official signing-key rotation
  is verified independently.
- **Repository management:** the APT repository is managed by
  `jcook3701.utils.repo_add`, not a locally managed template or script.
- **Idempotence:** repeated runs avoid adding unchanged chart repository URLs.
- **Helm configuration:** Helm is a client-side CLI; no system-wide Helm
  configuration template or service is required for installation.
- **Helm v4 compatibility:** plugins and charts should be checked for major
  version compatibility separately; this role only manages the Helm CLI.

### Helpful Links

1. [Helm Installation](https://helm.sh/docs/intro/install/)
2. [Helm Documentation](https://helm.sh/docs/)
3. [Helm GitHub Releases](https://github.com/helm/helm/releases)
4. [Helm Chart Repositories](https://helm.sh/docs/helm/helm_repo/)
5. [Helm CLI Reference](https://helm.sh/docs/helm/)
6. [Ansible `repo_add` utility role](https://github.com/jcook3701/jcook3701.utils/tree/main/roles/repo_add)
7. [Ansible `pkg_manager` utility role](https://github.com/jcook3701/jcook3701.utils/tree/main/roles/pkg_manager)

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container
management ecosystem.
