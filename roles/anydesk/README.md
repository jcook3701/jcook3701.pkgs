# AnyDesk

[AnyDesk](https://anydesk.com/en), the secure and intuitive remote desktop app with innovative features, perfect for seamless remote desktop application across devices.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `anydesk_state` | string | Desired lifecycle state of AnyDesk. Choices: `present`, `absent`, `teardown`. | `present` |
| `anydesk_debug` | boolean | Enable additional debugging output during role execution. | `true` |
| `anydesk_download_url` | string | Base URL of the official AnyDesk APT package repository. | `http://deb.anydesk.com` |
| `anydesk_key_download_url` | string | URL used to retrieve the official AnyDesk repository GPG signing key. | `https://keys.anydesk.com/repos/DEB-GPG-KEY` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and package management ecosystem.

<!--
## Authors Notes

-->
