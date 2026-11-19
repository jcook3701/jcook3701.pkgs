# Flatpak

[Flatpak](https://flatpak.org/) changes app distribution for the better. Advantages include: Build for every distro, Create one app and distribute it to the entire Linux desktop.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `flatpak_state` | string | Desired lifecycle state of Flatpak. Choices: `present`, `absent`, `teardown`. | `present` |
| `flatpak_debug` | boolean | Enable additional debugging output during role execution. | `true` |
| `flatpak_manage_group` | boolean | Manage the Flatpak system group. | `true` |
| `flatpak_users` | list[dict] | List of local users and groups granted Flatpak runtime access. Each entry contains `name` (required) and `group` (optional). | `[{name: "{{ ansible_user \| default(ansible_user_id) }}", group: "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `flatpak_use_upstream_repo` | boolean | Configure the upstream Flatpak package repository, such as the stable PPA on Ubuntu. | `true` |
| `flatpak_download_url` | string | Base URL for the upstream Flatpak package repository. | `https://ppa.launchpadcontent.net` |
| `flatpak_key_download_url` | string | URL used to retrieve the upstream Flatpak repository GPG signing key. | `https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x5C6D153A17C02C337EF6C663B8B9D41229DFA5F5` |
| `flatpak_manage_repos` | boolean | Enable management of Flatpak remote repositories. | `true` |
| `flatpak_repos` | list[dict] | List of Flatpak remote repositories. Each entry requires `name` and `url` pointing to a `.flatpakrepo` file. | `[{name: "flathub", url: "https://dl.flathub.org/repo/flathub.flatpakrepo"}]` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
