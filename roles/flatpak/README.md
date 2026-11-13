# Flatpak

[Flatpak](https://flatpak.org/) changes app distribution for the better. Advantages include: Build for every distro, Create one app and distribute it to the entire Linux desktop.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`flatpak_state`** | The desired state of the Flatpak package and configuration. Choices: `present`, `absent`, `teardown`. | `"present"` |
| **`flatpak_users`** | A declarative array of local system accounts to append to the `_flatpak` system group. Each item is a dictionary containing:<br>• **`name`** *(str, required)*: The exact local username string to grant Flatpak application management permissions. | `[]` |
| **`flatpak_manage_group`** | Toggles whether the role ensures the foundational `flatpak` system group is actively declared and maintained. | `true` |
| **`flatpak_repos`** | A list of Flatpak remote repositories to configure. Each item is a dictionary containing:<br>• **`name`** *(str, required)*: The internal name for the repository (e.g., `flathub`).<br>• **`url`** *(str, required)*: The full URL pointing to the `.flatpakrepo` file. | `[]` |
| `flatpak_manage_repos` | Controls whether the role should actively manage Flatpak remote repositories. | `true` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
