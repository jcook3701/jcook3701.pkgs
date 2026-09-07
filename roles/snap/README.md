# Snap

[Snaps](https://snapcraft.io/) are containerized software packages for Linux, developed by Canonical, designed to work across distributions with all dependencies included. They provide automatic updates, security confinement, and easy installation of apps like Spotify or Nextcloud. Snaps are natively supported in Ubuntu and can be installed via snapd on other distributions.

## Role Variables

| Variable | Default Value | Type | Description |
| :--- | :--- | :--- | :--- |
| `snap_state` | `present` | String | Controls the lifecycle execution state for the package installation. Valid choices are `present` or `absent`. |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
