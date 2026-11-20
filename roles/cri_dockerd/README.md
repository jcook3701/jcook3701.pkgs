# cri-dockerd

Install [Mirantis cri-dockerd](https://github.com/Mirantis/cri-dockerd), the Docker Engine Container Runtime Interface (CRI) adapter for Kubernetes.

The role downloads an upstream `.deb` release artifact, delegates the package installation and removal to `jcook3701.utils.pkg_manager`, and manages the `cri-docker.socket` systemd unit. It does not create an APT repository, change Docker Engine settings, initialize Kubernetes, or modify `jcook3701.pkgs.kubernetes`.

## Supported Platforms

For the default release `v0.4.10`, upstream provides Ubuntu `focal`, `jammy`, and `noble`, and Debian `bullseye` and `bookworm` packages for `amd64` and `arm64`.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `cri_dockerd_state` | str | `present`, `absent`, `teardown` | `present` |
| `cri_dockerd_debug` | bool | Print installer configuration | `true` |
| `cri_dockerd_version` | str | Upstream release version | `0.4.10` |
| `cri_dockerd_package_revision` | str | Debian package build suffix | `3-0` |
| `cri_dockerd_download_url` | str | Mirantis release download base URL | `https://github.com/Mirantis/cri-dockerd/releases/download` |
| `cri_dockerd_package_cache_dir` | path | Downloaded package cache | `/var/cache/cri-dockerd` |
| `cri_dockerd_package_checksum` | str | Optional `get_url` checksum such as `sha256:...` | `""` |
| `cri_dockerd_manage_service` | bool | Manage systemd socket | `true` |
| `cri_dockerd_service` | str | Socket unit name | `cri-docker.socket` |
| `cri_dockerd_service_enabled` | bool | Enable socket at boot | `true` |
| `cri_dockerd_service_state` | str | `started`, `stopped` | `started` |

## Example

```yaml
- hosts: all
  roles:
    - role: jcook3701.pkgs.cri_dockerd
      vars:
        cri_dockerd_state: present
```

## Verification

```bash
systemctl is-enabled cri-docker.socket
systemctl is-active cri-docker.socket
sudo test -S /run/cri-dockerd.sock && echo 'CRI socket exists'
sudo crictl --runtime-endpoint unix:///run/cri-dockerd.sock info
```

A socket-activated `cri-docker.service` can be inactive until a client connects; inspect `cri-docker.socket` for readiness. Installing this adapter does not initialize a Kubernetes cluster or generate a kubeconfig.

## Notes

- `cri-dockerd` is separate from Docker CE. Docker Engine must already be installed and operational.
- The role uses upstream release assets rather than `repo_add`, because no APT repository is configured in this installation method.
- `absent` removes the package; `teardown` also deletes the role-owned package cache.
- Release artifact names and supported distributions can change in later versions; update the package revision and verify the published assets when changing the version.
- Supply `cri_dockerd_package_checksum` if pinning and verifying a known release artifact. The default trusts the HTTPS download without a separately pinned checksum.
