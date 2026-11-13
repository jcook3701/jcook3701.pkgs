# NAPS (Not Another PDF Scanner 2)

[NAPS2](https://www.naps2.com/) is free and open source scanning software for Windows, Mac and Linux.

Easily scan with devices from Canon, Brother, HP, Epson, Fujitsu, and more. Then save to PDF, TIFF, JPEG, or PNG with a single click.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `naps_state` | string | NAPS2 installation lifecycle. Choices: `present`, `absent`, `teardown`. | `present` |
| `naps_debug` | boolean | Enable debugging output during role execution. | `false` |
| `naps_users` | list[dict] | User accounts granted access to scanner devices. Each entry requires a `name` key. | `[{name: "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `naps_manage_group` | boolean | Manage the lifecycle of the `scanner` system group. | `true` |
| `naps_download_url` | string | Base URL of the official NAPS2 APT package repository. | `https://downloads.naps2.com` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
