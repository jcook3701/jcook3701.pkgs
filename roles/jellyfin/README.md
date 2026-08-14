# Jellyfin

[Jellyfin](https://jellyfin.org/) is a free, open-source media server that is natively built for Linux. The most popular and recommended installation methods for Linux are Docker (containerized) for easy updates, or a native APT install for Debian-based distributions like Ubuntu.

<!--
# Author's Notes:

The "Arr stack" is a popular group of self-hosted Bytesized Hosting applications used to automate downloading, organizing, and managing personal media libraries like movies and TV shows. Prowlarr, Radarr, and Sonarr work together as a pipeline, communicating with a download client (like qBittorrent) and a media server (like Plex or Jellyfin)

``` shell
Prowlarr → finds releases on indexers/trackers
    ↓
Sonarr/Radarr → picks the best quality match
    ↓
Download client (rTorrent/Deluge/qBittorrent) → fetches the file
    ↓
Sonarr/Radarr → renames and moves to library folder
    ↓
Plex/Jellyfin → scans and adds to your library
    ↓
Bazarr → finds and downloads matching subtitles
```
-->
