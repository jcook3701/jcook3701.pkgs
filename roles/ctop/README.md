# ctop

Top-like interface for container metrics

[`ctop`](https://github.com/bcicen/ctop) provides a concise and condensed overview of real-time metrics for multiple containers.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `ctop_state` | Lifecycle execution state for package installation or removal. Choices: `present`, `absent`, `teardown`. | `"present"` |
| `ctop_version` | The target deployment version for the ctop binary. | `"0.7.7"` |
| `ctop_base_bin_url` | Base repository endpoint URL used for ctop release asset lookups. | `"https://github.com/bcicen/ctop/releases/download/v{{ ctop_version }}"` |

## Example Configurations

### Example 1: Standard Cross-Platform Onboarding

This role automatically detects host CPU architecture via system facts (`x86_64`, `aarch64`, `armv7l`). This allows a single playbook configuration to provision `ctop` seamlessly across target x86 cloud instances and Raspberry Pi bare-metal clusters alike.

```yaml
# playbook.yml or host_vars/all.yml context
---
ctop_state: present
ctop_version: "0.7.7"
```

### Example 2: Target Version Pin Tuning

To step back or test against a different upstream release footprint without refactoring the role paths:

```yaml
# playbook.yml context
---
ctop_state: present
ctop_version: "0.7.6"
```

### Example 3: Absolute System Purge

To cleanly uninstall the container tracker binary and erase local cached deployment structures from target nodes:

```yaml
# playbook.yml context
---
ctop_state: teardown
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--

## Authors Notes:
Future install correct version based on system architecture.

defaults/main.yml:

``` yaml
ctop_version: 0.7.7 #('0.7.7', '0.7.6', '0.7.5', etc)
ctop_base_bin_url: https://github.com/bcicen/ctop/releases/download/v0.7.7/
```

vars/main.yml:

then use the correct package based on host system architecture.

``` yaml
ctop_pkg_name:
  amd64: ctop-0.7.7-linux-amd64
  arm: ctop-0.7.7-linux-arm
  arm64: ctop-0.7.7-linux-arm64
  ppc64le: ctop-0.7.7-linux-ppc64le
```

``` yaml
ctop_bin_url: "{{ ctop_base_bin_url }}/v{{ ctop_version }}/{{  }}"
```

-->
